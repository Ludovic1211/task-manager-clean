import networkx as nx
from taskmanager.tache import Tache

class Planificateur:
    def __init__(self):
        """
        Initialise un planificateur avec un graphe dirigé pour gérer les dépendances.
        """
        self.taches: dict[str, Tache] = {}
        self.graphe: nx.DiGraph = nx.DiGraph()

    def ajouter_tache(self, tache: Tache):
        """
        Ajoute une tâche et ses dépendances dans le graphe.
        """
        self.taches[tache.nom] = tache
        self.graphe.add_node(tache.nom)  # <- plus d'erreur ici
        for dep in tache.dependances:
            self.graphe.add_edge(dep, tache.nom)

    def generer_planning(self) -> list[str]:
        """
        Génère un ordre d'exécution des tâches respectant les dépendances.
        Retourne une liste de noms de tâches triées topologiquement.
        """
        try:
            return list(nx.topological_sort(self.graphe))
        except nx.NetworkXUnfeasible:
            raise ValueError("Le graphe contient un cycle : impossible de générer un planning.")

    def ordonner_taches(self) -> dict[str, tuple[int, int]]:
        """
        Calcule les dates de début et de fin au plus tôt de chaque tâche.
        Retourne un dictionnaire {nom_tache: (debut, fin)}.
        """
        planning = {}
        for tache_nom in nx.topological_sort(self.graphe):
            tache = self.taches[tache_nom]
            if not tache.dependances:
                debut = 0
            else:
                debut = max(planning[dep][1] for dep in tache.dependances)
            fin = debut + tache.duree
            planning[tache_nom] = (debut, fin)
        return planning
