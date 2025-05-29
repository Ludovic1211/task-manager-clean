
from tache import Tache
from planificateur import Planificateur

def test_ajout_tache_simple():
    t1 = Tache("Fondations", 10)  # ✅ préalables est optionnel
    p = Planificateur()
    p.ajouter_tache(t1)
    assert "Fondations" in p.graphe


