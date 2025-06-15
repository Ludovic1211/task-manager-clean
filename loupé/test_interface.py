import pytest
import tkinter as tk
from unittest import mock
from taskmanager.interface import InterfacePlanificateur
from taskmanager.tache import Tache

@pytest.fixture
def app():
    """
    Fixture qui crée une instance de l'interface sans afficher la fenêtre principale.
    car cela va tout bloquer
    """
    root = tk.Tk()
    root.withdraw()  # Empêche l'affichage de la fenêtre pendant les tests
    interface = InterfacePlanificateur(root)
    yield interface
    root.destroy()

def test_ajout_tache_simple(app):
    """
    Teste l'ajout d'une tâche valide via les champs de l'interface principale.
    Vérifie que la tâche est bien enregistrée dans le dictionnaire temporaire.
    """
    app.entry_nom.insert(0, "T1")
    app.entry_duree.insert(0, "3")
    app.entry_dependances.insert(0, "")
    app.var_livraison.set(True)

    app.ajouter_tache()

    assert "T1" in app.taches_temp
    t = app.taches_temp["T1"]
    assert t.nom == "T1"
    assert t.duree == 3
    assert t.dependances == []
    assert t.livraison is True

def test_ajout_tache_invalide(app):
    """
    Teste le comportement lorsque l'utilisateur entre des données invalides
    (nom vide ou durée non numérique). Vérifie qu'une erreur est levée via `messagebox`.
    """
    app.entry_nom.insert(0, "")
    app.entry_duree.insert(0, "abc")  # Non numérique

    with mock.patch("tkinter.messagebox.showerror") as mocked_error:
        app.ajouter_tache()
        mocked_error.assert_called_once()

    assert app.taches_temp == {}

def test_suppression_tache(app):
    """
    Teste la suppression d'une tâche ajoutée manuellement à l'interface et au dictionnaire.
    Vérifie qu'elle est bien retirée des deux.
    """
    t = Tache("T2", 2)
    app.taches_temp["T2"] = t
    app.tree.insert("", tk.END, iid="T2", values=("T2", 2, "", "Non"))

    app.tree.selection_set("T2")
    app.supprimer_tache()

    assert "T2" not in app.taches_temp
    assert not app.tree.exists("T2")
