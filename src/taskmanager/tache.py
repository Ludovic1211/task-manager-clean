from typing import List, Optional


class Tache:
    def __init__(self, nom: str, duree: int, prealables: Optional[List[str]] = None, livraison: bool = False) -> None:
        """
        Initialise une tâche avec un nom, une durée, une liste de tâches préalables (dépendances),
        et un indicateur précisant s'il s'agit d'une tâche de type 'livraison'.

        :parametre nom: Le nom de la tâche.
        :parametre duree: La durée de la tâche (en jours par exemple).
        :parametre prealables: Liste des noms de tâches qui doivent être réalisées avant celle-ci.
        :parametre livraison: Indique si la tâche est une livraison finale.
        """
        self.nom: str = nom
        self.duree: int = duree
        self.dependances: List[str] = prealables if prealables is not None else []
        self.livraison: bool = livraison

    def __repr__(self) -> str:
        return (
            f"Tache(nom='{self.nom}', duree={self.duree}, "
            f"dependances={self.dependances}, livraison={self.livraison})"
        )
