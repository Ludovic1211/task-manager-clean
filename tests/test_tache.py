import pytest
from taskmanager.tache import Tache

def test_tache_initialisation_sans_dependances():
    tache = Tache(nom="T1", duree=3)
    assert tache.nom == "T1"
    assert tache.duree == 3
    assert tache.dependances == []
    assert tache.livraison is False

def test_tache_initialisation_avec_dependances_et_livraison():
    tache = Tache(nom="T2", duree=2, prealables=["T1"], livraison=True)
    assert tache.nom == "T2"
    assert tache.duree == 2
    assert tache.dependances == ["T1"]
    assert tache.livraison is True

def test_repr():
    tache = Tache(nom="T3", duree=4, prealables=["T1", "T2"])
    expected = "Tache(nom='T3', duree=4, dependances=['T1', 'T2'], livraison=False)"
    assert repr(tache) == expected
