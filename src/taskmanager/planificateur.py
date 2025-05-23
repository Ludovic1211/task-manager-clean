def ordonner_taches(self) -> dict[str, tuple[int, int]]:
    """
    Calcule les dates de début et de fin au plus tôt de chaque tâche.
    Retourne un dictionnaire {nom_tache: (debut, fin)}.
    Tient compte de la contrainte que deux livraisons ne peuvent être simultanées.
    """
    planning = {}
    livraisons_occupees = []  # Liste de tuples (début, fin) des livraisons déjà placées

    for tache_nom in nx.topological_sort(self.graphe):
        tache = self.taches[tache_nom]

        # Date de début minimale basée sur les dépendances
        if not tache.dependances:
            debut = 0
        else:
            debut = max(planning[dep][1] for dep in tache.dependances)

        if tache.livraison:
            # Éviter le chevauchement avec d'autres livraisons
            while any(
                not (debut + tache.duree <= d or debut >= f)
                for d, f in livraisons_occupees
            ):
                debut += 1  # Décaler jusqu'à ce qu'il n'y ait plus de conflit

            # Ajouter cette livraison à la liste des plages occupées
            livraisons_occupees.append((debut, debut + tache.duree))

        fin = debut + tache.duree
        planning[tache_nom] = (debut, fin)

    return planning
