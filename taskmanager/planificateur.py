import networkx as nx
from taskmanager.tache import Tache


class Planificateur:
    """
    Classe planificateur qui va regrouper les de tâches et leurs dépendances.
    ----------
    - taches : dictionnaire contenant les objets Tache .
    - graphe : graphe orienté en fonction des dépendances et pour faire untri topologique.
    """
    def __init__(self):
    
        self.taches: dict[str, Tache] = {}
        self.graphe: nx.DiGraph = nx.DiGraph()

    def ajouter_tache(self, tache: Tache):
        """
        Ajoute une tâche au dictionnaire et au graphe.
        Les dépendances sont représentées par des arêtes dans le graphe.
        ----------
        - tache : Tache à ajouter au planificateur.
        """
        
        self.taches[tache.nom] = tache
        self.graphe.add_node(tache.nom)
        for dep in tache.dependances:
            self.graphe.add_edge(dep, tache.nom)

    def generer_planning(self) -> list[str]:
        """
        Retourne un ordre valide des tâches grace  à un tri topologique du graphe.
        Met un message d'erreur si un cycle est détecté dans le graphe.
        """
        
        try:
            return list(nx.topological_sort(self.graphe))
        except nx.NetworkXUnfeasible:
            raise ValueError("Le graphe contient un cycle : planning pas possible.")

    def ordonner_taches(self) -> dict[str, tuple[int, int]]:
        """
        Calcule le planning  : pour chaque tâche, Trouve son jour de début et de fin,
        en tenant compte des dépendances et de si il y a livraison ou non.

        Retour :
        -------
        - Dictionnaire associant à chaque tâche un tuple (début, fin).
        """
        
        planning: dict[str, tuple[int, int]] = {}
        livraisons_occupees: dict[int, str] = {}

        for tache_nom in nx.topological_sort(self.graphe):
            tache = self.taches[tache_nom]

            # Calcul du début au plus tôt
            if not tache.dependances:
                debut = 0
            else:
                debut = max(planning[dep][1] for dep in tache.dependances)

            # Si c'est une livraison, vérifier les créneaux déjà occupés
            if tache.livraison:
                while any(jour in livraisons_occupees for jour in range(debut, debut + tache.duree)):
                    debut += 1  # Décaler jusqu'à trouver un créneau libre
                # Marquer les jours occupés
                for jour in range(debut, debut + tache.duree):
                    livraisons_occupees[jour] = tache.nom

            fin = debut + tache.duree
            planning[tache_nom] = (debut, fin)

        return planning

    def duree_totale(self) -> int:
        """
        Calcule la durée totale du projet en fonction de la dernière tache teminée et donne la durée totale en jours.
        """
        dates = self.ordonner_taches()
        return max(fin for _, fin in dates.values())
