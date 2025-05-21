"""
Module de planification des tâches via un graphe de dépendances et tri topologique.
"""

from taskmanager.tache import Tache


from typing import List
import networkx as nx
from networkx import DiGraph
from tache import Tache

class Planificateur:
    def __init__(self, taches: List[Tache]): # Liste de tâches
        self.taches = {t.id: t for t in taches} # Dictionnaire de tâches
        self.graphe: DiGraph = DiGraph() # Graphe orienté
        self._construire_graphe() # Construction du graphe

    def _construire_graphe(self):
        for t in self.taches.values():
            self.graphe.add_node(t.id, duree=t.duree) # Ajout des nœuds
            for pre in t.prealables:
                self.graphe.add_edge(pre, t.id) # Ajout des arêtes

    def est_acyclique(self):
        return nx.is_directed_acyclic_graph(self.graphe) # Vérification de l'absence de cycles, exemple: A -> B -> C, A -> C

    def tri_topologique(self):
        if not self.est_acyclique(): # Vérification de l'absence de cycles
            raise ValueError("Le graphe contient un cycle.")
        return list(nx.topological_sort(self.graphe)) # Tri topologique
