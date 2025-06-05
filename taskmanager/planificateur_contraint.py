from taskmanager.tache import Tache
import networkx as nx

class PlanificateurContraint:
    def __init__(self, taches: dict[str, Tache], max_taches: int = 1, max_livraisons: int = 1):
        self.taches = taches
        self.graphe = nx.DiGraph()
        self.max_taches = max_taches
        self.max_livraisons = max_livraisons
        for tache in taches.values():
            self.graphe.add_node(tache.nom)
            for dep in tache.dependances:
                self.graphe.add_edge(dep, tache.nom)

    def generer_planning(self) -> dict[str, tuple[int, int]]:
        try:
            ordre_topologique = list(nx.topological_sort(self.graphe))
        except nx.NetworkXUnfeasible:
            raise ValueError("Cycle détecté : planning impossible.")

        en_attente = set(ordre_topologique)
        planning = {}
        jour = 0
        en_cours = []  # (nom, jour_fin)
        livraisons_occupees = []  # (nom, jour_fin)

        while en_attente:
            # Nettoyage des tâches terminées
            en_cours = [(nom, fin) for nom, fin in en_cours if fin > jour]
            livraisons_occupees = [(nom, fin) for nom, fin in livraisons_occupees if fin > jour]

            nb_taches = len(en_cours)
            nb_livraisons = len([1 for nom, _ in livraisons_occupees if self.taches[nom].livraison])

            # Trouver les tâches prêtes à être lancées
            disponibles = [nom for nom in en_attente if all(dep in planning for dep in self.taches[nom].dependances)]

            # Choisir celles qui peuvent commencer aujourd’hui
            for nom in disponibles:
                if nb_taches >= self.max_taches:
                    break
                if self.taches[nom].livraison and nb_livraisons >= self.max_livraisons:
                    continue

                debut = jour
                fin = jour + self.taches[nom].duree
                planning[nom] = (debut, fin)
                en_cours.append((nom, fin))
                if self.taches[nom].livraison:
                    livraisons_occupees.append((nom, fin))
                en_attente.remove(nom)
                nb_taches += 1
                if self.taches[nom].livraison:
                    nb_livraisons += 1

            jour += 1

        return planning

    def duree_totale(self) -> int:
        planning = self.generer_planning()
        return max(fin for _, fin in planning.values())
