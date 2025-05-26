class Tache:
    def __init__(self, nom: str, duree: int, prealables=None, livraison: bool = False):
        """
        Initialise une tâche avec un nom, une durée, une liste de tâches préalables (dépendances),
        et un indicateur précisant s'il s'agit d'une tâche de type 'livraison'.
        """
        self.nom = nom
        self.duree = duree
        self.dependances = prealables if prealables is not None else []
        self.livraison = livraison  # Nouvel attribut

    def __repr__(self):
        return (
            f"Tache(nom='{self.nom}', duree={self.duree}, "
            f"dependances={self.dependances}, livraison={self.livraison})"
        )
        #er#
