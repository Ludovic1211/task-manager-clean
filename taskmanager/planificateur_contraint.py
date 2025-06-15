from taskmanager.tache import Tache
import networkx as nx
from typing import Dict, Tuple, List, Set


class PlanificateurContraint:
    """
    Planificateur avec contraintes sur le nombre de tâches et de livraisons simultanées.

    Ce planificateur utilise un graphe orienté acyclique (DAG) pour organiser les tâches selon leurs dépendances.
    Il respecte des contraintes sur le nombre de tâches pouvant être exécutées simultanément
    ainsi que sur le nombre de livraisons simultanées.
    """

    def __init__(self, taches: Dict[str, Tache], max_taches: int = 1, max_livraisons: int = 1) -> None:
        """
        Initialise le planificateur avec les tâches et les contraintes de parallélisme.

        Aves:
            taches (Dict[str, Tache]): Dictionnaire des tâches.
            max_taches (int): Nombre maximal de tâches pouvant être exécutées en parallèle.
            max_livraisons (int): Nombre maximal de livraisons pouvant avoir lieu en meme temps.
        """
        self.taches: Dict[str, Tache] = taches
        self.graphe: nx.DiGraph = nx.DiGraph()
        self.max_taches: int = max_taches
        self.max_livraisons: int = max_livraisons

        for tache in taches.values():
            self.graphe.add_node(tache.nom)
            for dep in tache.dependances:
                self.graphe.add_edge(dep, tache.nom)

    def generer_planning(self) -> Dict[str, Tuple[int, int]]:
        """
        Génère un planning tenant compte des contraintes puis rend un dictionnaire associant à chaque tâche son intervalle (début, fin).
        Il y a une erreur si un cycle est détecté.
        """
        try:
            ordre_topologique: List[str] = list(nx.topological_sort(self.graphe))
        except nx.NetworkXUnfeasible:
            raise ValueError("Cycle détecté : planning impossible.")

        en_attente: Set[str] = set(ordre_topologique)
        planning: Dict[str, Tuple[int, int]] = {}
        jour: int = 0
        en_cours: List[Tuple[str, int]] = []  # (nom, jour_fin)
        livraisons_occupees: List[Tuple[str, int]] = []  # (nom, jour_fin)

        while en_attente:
            # Nettoyer les tâches terminées
            en_cours = [(nom, fin) for nom, fin in en_cours if fin > jour]
            livraisons_occupees = [(nom, fin) for nom, fin in livraisons_occupees if fin > jour]

            nb_taches = len(en_cours)
            nb_livraisons = len([1 for nom, _ in livraisons_occupees if self.taches[nom].livraison])

            # Identifier les tâches prêtes à être exécutées
            disponibles: List[str] = [
                nom for nom in en_attente
                if all(dep in planning for dep in self.taches[nom].dependances)
            ]

            # Lancer les tâches dans les limites des contraintes
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
        """
        Calcule la durée totale du projet en tenant compte des contraintes et renvoie le nombre total de jours nécessaires pour exécuter toutes les tâches.
        """
        planning = self.generer_planning()
        return max(fin for _, fin in planning.values())
