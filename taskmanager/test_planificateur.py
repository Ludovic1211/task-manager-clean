
from taskmanager.tache import Tache
from taskmanager.planificateur import Planificateur

def test_ajout_tache_simple():
    """
    Teste l'ajout d'une tâche sans dépendance au planificateur.
    Vérifie que la tâche est bien enregistrée dans le graphe.
    """
    t1 = Tache("Fondations", 10)
    p = Planificateur()
    p.ajouter_tache(t1)
    assert "Fondations" in p.graphe


def test_ajout_taches_avec_dependances():
    """
    Teste l'ajout de tâches avec dépendances.
    Vérifie que l'ordre dans le planning respecte les dépendances imposées.
    """
    t1 = Tache("A", 2)
    t2 = Tache("B", 3, ["A"])
    t3 = Tache("C", 1, ["A", "B"])

    p = Planificateur()
    for t in [t1, t2, t3]:
        p.ajouter_tache(t)

    ordre = p.generer_planning()
    assert ordre.index("A") < ordre.index("B") < ordre.index("C")


def test_detection_cycle():
    """
    Teste la détection de cycle dans les dépendances.
    Le planificateur doit lever une exception si un cycle est présent.
    """
    t1 = Tache("A", 1, ["B"])
    t2 = Tache("B", 1, ["A"])

    p = Planificateur()
    for t in [t1, t2]:
        p.ajouter_tache(t)

    try:
        p.generer_planning()
        assert False, "Un cycle aurait dû être détecté"
    except ValueError:
        assert True


def test_dates_debut_fin():
    """
    Vérifie que les dates de début et de fin calculées sont correctes
    pour une suite de tâches avec dépendances.
    """
    t1 = Tache("A", 2)
    t2 = Tache("B", 3, ["A"])
    t3 = Tache("C", 1, ["A", "B"])

    p = Planificateur()
    for t in [t1, t2, t3]:
        p.ajouter_tache(t)

    resultats = p.ordonner_taches()

    assert resultats["A"] == (0, 2)
    assert resultats["B"] == (2, 5)
    assert resultats["C"] == (5, 6)


def test_duree_totale_projet():
    """
    Vérifie que la durée totale du projet correspond bien au chemin critique.
    Ici, le chemin le plus long est A → B → C → E.
    """
    t1 = Tache("A", 1)
    t2 = Tache("B", 2, ["A"])
    t3 = Tache("C", 3, ["B"])
    t4 = Tache("D", 2, ["A"])
    t5 = Tache("E", 1, ["D", "C"])

    p = Planificateur()
    for t in [t1, t2, t3, t4, t5]:
        p.ajouter_tache(t)

    duree = p.duree_totale()
    assert duree == 7  # A(1) → B(2) → C(3) → E(1)
