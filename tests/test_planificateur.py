import pytest
from taskmanager.tache import Tache
from taskmanager.planificateur_contraint import PlanificateurContraint

def test_planning_simple_sans_contraintes():
    """
    Vérifie qu'un planning basique sans contraintes sévères est généré correctement.
    Les tâches B et C doivent démarrer après A.
    """
    taches = {
        "A": Tache("A", 2),
        "B": Tache("B", 3, prealables=["A"]),
        "C": Tache("C", 1, prealables=["A"]),
    }
    planificateur = PlanificateurContraint(taches, max_taches=2, max_livraisons=2)
    planning = planificateur.generer_planning()

    assert planning["A"] == (0, 2)
    assert planning["B"][0] >= 2
    assert planning["C"][0] >= 2
    assert planning["B"][1] - planning["B"][0] == 3
    assert planning["C"][1] - planning["C"][0] == 1

def test_planning_avec_livraison_limitee():
    """
    Vérifie que les contraintes sur le nombre de livraisons simultanées sont respectées.
    Pas plus d'une livraison ne doit être active au même moment.
    """
    taches = {
        "A": Tache("A", 1, livraison=True),
        "B": Tache("B", 1, livraison=True),
        "C": Tache("C", 1),
    }
    planificateur = PlanificateurContraint(taches, max_taches=3, max_livraisons=1)
    planning = planificateur.generer_planning()

    jours_livraisons = [debut for nom, (debut, _) in planning.items() if taches[nom].livraison]
    # Vérifie qu'aucune livraison ne se superpose
    assert len(set(jours_livraisons)) == len(jours_livraisons)

def test_cycle_detecte():
    """
    Vérifie que le planificateur détecte bien un cycle dans les dépendances.
    """
    taches = {
        "A": Tache("A", 1, prealables=["B"]),
        "B": Tache("B", 1, prealables=["A"]),
    }
    planificateur = PlanificateurContraint(taches)

    with pytest.raises(ValueError, match="Cycle détecté"):
        planificateur.generer_planning()

def test_duree_totale():
    """
    Vérifie que la durée totale est correcte lorsque les tâches sont enchaînées.
    """
    taches = {
        "A": Tache("A", 2),
        "B": Tache("B", 2, prealables=["A"]),
        "C": Tache("C", 2, prealables=["B"]),
    }
    planificateur = PlanificateurContraint(taches, max_taches=1)
    duree = planificateur.duree_totale()

    assert duree == 6
