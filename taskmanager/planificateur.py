import networkx as nx
from taskmanager.tache import Tache
from typing import Dict, Tuple, List


class Planificateur:
    """
    Planificateur de tâches avec gestion des dépendances via un graphe orienté.

    Attributs :
    ----------
    - taches : Dictionnaire contenant les tâches avec leur nom comme clé.
    - graphe : Graphe orienté représentant les dépendances entre les tâches.
    """
    def __init__(self) -> None:
        self.taches: Dict[str, Tache] = {}
        self.graphe: nx.DiGraph = nx.DiGraph()

    def ajouter_tache(self, tache: Tache) -> None:
        """
        Ajoute une tâche au planificateur et met à jour le graphe avec ses dépendances.

        Paramètres :
        -----------
        - tache : La tâche à ajouter.
        """
        self.taches[tache.nom] = tache
        self.graphe.add_node(tache.nom)
        for dep in tache.dependances:
            self.graphe.add_edge(dep, tache.nom)

    def generer_planning(self) -> List[str]:
        """
        Génère un ordre de traitement des tâches via un tri topologique du graphe.

        Retour :
        -------
        - Une liste ordonnée de noms de tâches.
        """
        try:
            return list(nx.topological_sort(self.graphe))
        except nx.NetworkXUnfeasible:
            raise ValueError("Le graphe contient un cycle : planning pas possible.")

    def ordonner_taches(self) -> Dict[str, Tuple[int, int]]:
        """
        Calcule un planning : associe à chaque tâche son jour de début et de fin,
        en tenant compte des dépendances et des contraintes de livraison.

        Retour :
        -------
        - Un dictionnaire {nom_tache: (début, fin)}.
        """
        planning: Dict[str, Tuple[int, int]] = {}
        livraisons_occupees: Dict[int, str] = {}

        for tache_nom in nx.topological_sort(self.graphe):
            tache = self.taches[tache_nom]

            if not tache.dependances:
                debut = 0
            else:
                debut = max(planning[dep][1] for dep in tache.dependances)

            if tache.livraison:
                while any(jour in livraisons_occupees for jour in range(debut, debut + tache.duree)):
                    debut += 1
                for jour in range(debut, debut + tache.duree):
                    livraisons_occupees[jour] = tache.nom

            fin = debut + tache.duree
            planning[tache_nom] = (debut, fin)

        return planning

    def duree_totale(self) -> int:
        """
        Retourne la durée totale du projet (dernier jour de fin d'une tâche).
        """
        dates = self.ordonner_taches()
        return max(fin for _, fin in dates.values())
