from src.taskmanager.planificateur import Planificateur
from src.taskmanager.exemple_donnees import donnees_taches


def demo_maison():
    plan = Planificateur()
    
    # Créer et ajouter toutes les tâches
    for tache in donnees_taches:
        plan.ajouter_tache(tache)


    # Afficher le planning dans l'ordre topologique
    ordre = plan.generer_planning()
    print("Planning optimal (ordre des tâches) :")
    print(" → ".join(ordre))

    # Afficher les dates de début/fin
    print("\nDates de début et de fin (au plus tôt) :")
    planning = plan.ordonner_taches()
    for tache in ordre:
        debut, fin = planning[tache]
        print(f"Tâche {tache} : début = {debut}, fin = {fin}")

    # Afficher la durée totale
    duree_totale = max(fin for _, fin in planning.values())
    print(f"\nDurée totale minimale du projet : {duree_totale} jours")


if __name__ == "__main__":
    demo_maison()

