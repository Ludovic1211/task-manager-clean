from .tache import Tache

donnees_taches = [
    Tache("A", 3, livraison=True),                     # Livraison des câblages
    Tache("B", 4, ["A"]),                              # Pose des câblages
    Tache("C", 1, ["B"]),                              # Inspection des câblages
    Tache("D", 4, livraison=True),                     # Livraison du matériel de plomberie
    Tache("E", 2, ["D", "H"]),                         # Travaux de plomberie extérieure
    Tache("F", 5, ["E", "I"]),                         # Travaux de plomberie intérieure
    Tache("G", 1),                                     # Terrassement
    Tache("H", 3, ["G"]),                              # Fondations
    Tache("I", 5, ["H"]),                              # Construction de l'ossature
    Tache("J", 6, livraison=True),                     # Livraison des briques
    Tache("K", 3, ["J", "I"]),                         # Briquetage
    Tache("L", 14, ["I"], livraison=True),             # Livraison des tuiles
    Tache("M", 2, ["L", "I"]),                         # Construction de la charpente
    Tache("N", 2, ["M", "L"]),                         # Pose de la couverture
    Tache("O", 3, ["M", "F", "C"]),                    # Revêtements intérieurs
    Tache("P", 3, ["O", "N"]),                         # Revêtements extérieurs
    Tache("Q", 2, ["P"]),                              # Inspection générale
    Tache("R", 1, ["N", "K", "O"]),                    # Nettoyage extérieur
    Tache("S", 3, ["R"])                               # Aménagements extérieurs
]
