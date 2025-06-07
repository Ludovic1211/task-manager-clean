from taskmanager.tache import Tache
import networkx as nx
from typing import Dict, Tuple, List, Set


class PlanificateurContraint:
    """
    Planificateur avec contraintes sur le nombre de tâches et de livraisons simultanées.
    """

    def __init__(self, taches: Dict[str, Tache], max_taches: int = 1, max_livraisons: int = 1) -> None:
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
        Génère un planning contraint par un nombre maximal de tâches et de livraisons simultanées.
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

            # Tâches prêtes
            disponibles: List[str] = [
                nom for nom in en_attente
                if all(dep in planning for dep in self.taches[nom].dependances)
            ]

            # Lancer les tâches possibles
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
        Retourne la durée totale du projet avec les contraintes appliquées.
        """
        planning = self.generer_planning()
        return max(fin for _, fin in planning.values())
