from typing import List, Optional


class Tache:
    def __init__(
        self,
        nom: str,
        duree: int,
        prealables: Optional[List[str]] = None,
        livraison: bool = False
    ) -> None:
        self.nom: str = nom
        self.duree: int = duree
        self.dependances: List[str] = prealables if prealables is not None else []
        self.livraison: bool = livraison

    def __repr__(self) -> str:
        return (
            f"Tache(nom='{self.nom}', duree={self.duree}, "
            f"dependances={self.dependances}, livraison={self.livraison})"
        )
