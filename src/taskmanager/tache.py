"""
Module de définition de la classe Tache pour la gestion de tâches planifiées.
"""

from typing import List

class Tache:
    def __init__(self, id: str, duree: int, prealables: List[str]):
        self.id = id                          # ID de la tâche
        self.duree = duree                    # Durée en semaines
        self.prealables = prealables          # Liste des ID des tâches préalables
        self.debut = None                     # Calculé par l’algorithme
        self.fin = None                       # Calculé par l’algorithme


    def set_debut(self, debut: int): 
        self.debut = debut
        self.fin = debut + self.duree 

