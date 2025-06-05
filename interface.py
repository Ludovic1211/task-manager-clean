import tkinter as tk
from tkinter import ttk, messagebox
from taskmanager.tache import Tache
from taskmanager.planificateur_contraint import PlanificateurContraint
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import json
import os

SAUVEGARDE_PATH = "taches_sauvegardees.json"
INTRO_PATH = "intro.txt"

class InterfacePlanificateur:
    def __init__(self, root):
        self.root = root
        self.root.title("Planificateur de tâches")
        self.taches_temp = {}
        self.frame_main = None
        self.frame_planning = None

        self.max_taches_simultanées = tk.IntVar(value=1)
        self.max_livraisons_simultanées = tk.IntVar(value=1)

        self.afficher_intro()
        self.build_ui()
        self.charger_taches_sauvegardees()

    def afficher_intro(self):
        if os.path.exists(INTRO_PATH):
            with open(INTRO_PATH, "r", encoding="utf-8") as f:
                contenu = f.read()
            intro_window = tk.Toplevel(self.root)
            intro_window.title("Introduction")
            txt = tk.Text(intro_window, wrap="word")
            txt.insert("1.0", contenu)
            txt.config(state="disabled")
            txt.pack(padx=10, pady=10, fill="both", expand=True)
            btn_ok = tk.Button(intro_window, text="Fermer", command=intro_window.destroy)
            btn_ok.pack(pady=5)

    def build_ui(self):
        self.frame_main = tk.Frame(self.root)
        self.frame_main.pack(fill="both", expand=True)

        frame_form = tk.Frame(self.frame_main)
        frame_form.pack(padx=10, pady=10, fill="x")

        tk.Label(frame_form, text="Nom:").grid(row=0, column=0)
        self.entry_nom = tk.Entry(frame_form)
        self.entry_nom.grid(row=0, column=1)

        tk.Label(frame_form, text="Durée:").grid(row=1, column=0)
        self.entry_duree = tk.Entry(frame_form)
        self.entry_duree.grid(row=1, column=1)

        self.var_livraison = tk.BooleanVar()
        chk = tk.Checkbutton(frame_form, text="Livraison", variable=self.var_livraison)
        chk.grid(row=2, column=0, columnspan=2)

        tk.Label(frame_form, text="Dépendances (séparées par des virgules):").grid(row=3, column=0)
        self.entry_dependances = tk.Entry(frame_form)
        self.entry_dependances.grid(row=3, column=1)

        tk.Label(frame_form, text="Tâches simultanées max:").grid(row=4, column=0)
        tk.Entry(frame_form, textvariable=self.max_taches_simultanées).grid(row=4, column=1)

        tk.Label(frame_form, text="Livraisons simultanées max:").grid(row=5, column=0)
        tk.Entry(frame_form, textvariable=self.max_livraisons_simultanées).grid(row=5, column=1)

        btn_add = tk.Button(frame_form, text="Ajouter tâche", command=self.ajouter_tache)
        btn_add.grid(row=6, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(self.frame_main, columns=("Nom", "Durée", "Dépendances", "Livraison"), show="headings")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Durée", text="Durée")
        self.tree.heading("Dépendances", text="Dépendances")
        self.tree.heading("Livraison", text="Livraison")
        self.tree.pack(fill="both", expand=True, padx=10)

        frame_btn = tk.Frame(self.frame_main)
        frame_btn.pack(pady=5)

        btn_del = tk.Button(frame_btn, text="Supprimer tâche", command=self.supprimer_tache)
        btn_del.pack(side="left", padx=5)

        btn_save = tk.Button(frame_btn, text="Sauvegarder tâches", command=self.sauvegarder_taches)
        btn_save.pack(side="left", padx=5)

        btn_load = tk.Button(frame_btn, text="Charger tâches sauvegardées", command=self.charger_taches_sauvegardees)
        btn_load.pack(side="left", padx=5)

        btn_gen = tk.Button(frame_btn, text="Générer planning", command=self.afficher_planning)
        btn_gen.pack(side="left", padx=5)

    def charger_taches_sauvegardees(self):
        self.taches_temp.clear()
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not os.path.exists(SAUVEGARDE_PATH):
            return

        with open(SAUVEGARDE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        for t in data:
            tache = Tache(t["nom"], t["duree"], t["dependances"], t["livraison"])
            self.taches_temp[tache.nom] = tache
            self.tree.insert("", tk.END, iid=tache.nom, values=(tache.nom, tache.duree, ", ".join(tache.dependances), "Oui" if tache.livraison else "Non"))

    def ajouter_tache(self):
        nom = self.entry_nom.get().strip()
        duree = self.entry_duree.get().strip()
        livraison = self.var_livraison.get()
        dependances = [d.strip() for d in self.entry_dependances.get().split(",") if d.strip()]

        if not nom or not duree.isdigit():
            messagebox.showerror("Erreur", "Nom ou durée invalide.")
            return

        if nom in self.taches_temp:
            messagebox.showerror("Erreur", "Tâche déjà existante.")
            return

        tache = Tache(nom, int(duree), dependances, livraison)
        self.taches_temp[nom] = tache
        self.tree.insert("", tk.END, iid=nom, values=(nom, duree, ", ".join(dependances), "Oui" if livraison else "Non"))

    def supprimer_tache(self):
        sel = self.tree.selection()
        for item in sel:
            if item in self.taches_temp:
                del self.taches_temp[item]
            self.tree.delete(item)

    def sauvegarder_taches(self):
        data = [t.__dict__ for t in self.taches_temp.values()]
        with open(SAUVEGARDE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Succès", "Tâches sauvegardées avec succès.")

    def afficher_planning(self):
        planificateur = PlanificateurContraint(self.taches_temp, self.max_taches_simultanées.get(), self.max_livraisons_simultanées.get())

        try:
            planning = planificateur.generer_planning()
            ordre = list(nx.topological_sort(planificateur.graphe))
            duree = planificateur.duree_totale()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.frame_main.pack_forget()
        self.frame_planning = tk.Frame(self.root)
        self.frame_planning.pack(fill="both", expand=True)

        text = tk.Text(self.frame_planning, height=15)
        text.pack(fill="x", padx=10, pady=10)

        text.insert(tk.END, "Ordre des tâches :\n")
        text.insert(tk.END, " → ".join(ordre) + "\n\n")

        text.insert(tk.END, "Planning détaillé :\n")
        for nom in ordre:
            debut, fin = planning[nom]
            text.insert(tk.END, f"{nom} : début = {debut}, fin = {fin}\n")

        text.insert(tk.END, f"\nDurée totale : {duree} jours\n")

        fig, ax = plt.subplots(figsize=(8, 4))
        for i, nom in enumerate(ordre):
            debut, fin = planning[nom]
            ax.barh(y=nom, width=fin - debut, left=debut)
        ax.set_xlabel("Jours")
        ax.set_title("Diagramme de Gantt")

        canvas = FigureCanvasTkAgg(fig, master=self.frame_planning)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        btn_retour = tk.Button(self.frame_planning, text="Retour", command=self.retour_interface_principale)
        btn_retour.pack(pady=10)

    def retour_interface_principale(self):
        self.frame_planning.pack_forget()
        self.build_ui()
        for t in self.taches_temp.values():
            self.tree.insert("", tk.END, iid=t.nom, values=(t.nom, t.duree, ", ".join(t.dependances), "Oui" if t.livraison else "Non"))

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfacePlanificateur(root)
    root.mainloop()
