from typing import Dict, List, Tuple
import networkx as nx
from taskmanager.tache import Tache


class Planificateur:
    def __init__(self) -> None:
        """
        Initialise un planificateur avec un graphe dirigé pour gérer les dépendances.
        """
        self.taches: Dict[str, Tache] = {}
        self.graphe: nx.DiGraph = nx.DiGraph()

    def ajouter_tache(self, tache: Tache) -> None:
        """
        Ajoute une tâche et ses dépendances dans le graphe.
        """
        self.taches[tache.nom] = tache
        self.graphe.add_node(tache.nom)
        for dep in tache.dependances:
            self.graphe.add_edge(dep, tache.nom)

    def generer_planning(self) -> List[str]:
        """
        Génère un ordre d'exécution des tâches respectant les dépendances.
        Retourne une liste de noms de tâches triées topologiquement.
        """
        try:
            return list(nx.topological_sort(self.graphe))
        except nx.NetworkXUnfeasible:
            raise ValueError("Le graphe contient un cycle : impossible de générer un planning.")

    def ordonner_taches(self) -> Dict[str, Tuple[int, int]]:
        """
        Calcule les dates de début et de fin au plus tôt de chaque tâche,
        en tenant compte de la contrainte : pas de livraisons simultanées.
        Retourne un dictionnaire {nom_tache: (debut, fin)}.
        """
        planning: Dict[str, Tuple[int, int]] = {}
        livraisons_occupees: Dict[int, str] = {}

        for tache_nom in nx.topological_sort(self.graphe):
            tache = self.taches[tache_nom]

            if not tache.dependances:
                debut: int = 0
            else:
                debut = max(planning[dep][1] for dep in tache.dependances)

            if tache.livraison:
                while any(jour in livraisons_occupees for jour in range(debut, debut + tache.duree)):
                    debut += 1
                for jour in range(debut, debut + tache.duree):
                    livraisons_occupees[jour] = tache.nom

            fin: int = debut + tache.duree
            planning[tache_nom] = (debut, fin)

        return planning

    def duree_totale(self) -> int:
        """
        Calcule et retourne la durée minimale totale du projet (en jours).
        """
        dates = self.ordonner_taches()
        return max(fin for _, fin in dates.values())
