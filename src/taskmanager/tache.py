class Tache:
    def __init__(self, nom: str, duree: int, prealables=None):
        """
        Initialise une tâche avec un nom, une durée, et une liste de tâches préalables (dépendances).
        """
        self.nom = nom
        self.duree = duree
        self.dependances = prealables if prealables is not None else []

    def __repr__(self):
        return f"Tache(nom='{self.nom}', duree={self.duree}, dependances={self.dependances})"

