import tkinter as tk
from tkinter import messagebox
from taskmanager.planificateur import Planificateur
from taskmanager.tache import Tache
from taskmanager.exemple_donnees import donnees_taches

class InterfacePlanificateur:
    def __init__(self, root):
        """
        commence l’interface, crée un Planificateur
        et ajoute les tâches
        """
        self.root = root
        self.root.title("Planificateur de tâches")
        self.plan = Planificateur()

        for t in donnees_taches:
            self.plan.ajouter_tache(t)

        self.build_ui() 
        """
        Construit les éléments de l'interface utilisateur :
        champs de saisie, boutons, liste des dépendances et zone de texte pour les résultats.
        """
    def build_ui(self):
        frame_form = tk.Frame(self.root)
        frame_form.pack(padx=10, pady=10, fill="x")

        tk.Label(frame_form, text="Nom de la tâche:").grid(row=0, column=0, sticky="w")
        self.entry_nom = tk.Entry(frame_form)
        self.entry_nom.grid(row=0, column=1, sticky="ew")

        tk.Label(frame_form, text="Durée (jours):").grid(row=1, column=0, sticky="w")
        self.entry_duree = tk.Entry(frame_form)
        self.entry_duree.grid(row=1, column=1, sticky="ew")

        self.var_livraison = tk.BooleanVar()
        chk_livraison = tk.Checkbutton(frame_form, text="Livraison", variable=self.var_livraison)
        chk_livraison.grid(row=2, column=0, columnspan=2, sticky="w")

        tk.Label(frame_form, text="Dépendances:").grid(row=3, column=0, sticky="nw")
        self.lst_dependances = tk.Listbox(frame_form, selectmode=tk.MULTIPLE, height=6)
        self.lst_dependances.grid(row=3, column=1, sticky="ew")
        self.update_dependance_list()

        btn_ajouter = tk.Button(frame_form, text="Ajouter tâche", command=self.ajouter_tache)
        btn_ajouter.grid(row=4, column=0, columnspan=2, pady=5)

        btn_generer = tk.Button(self.root, text="Générer le planning", command=self.generer_planning)
        btn_generer.pack(pady=10)

        self.txt_resultat = tk.Text(self.root, height=20, width=80)
        self.txt_resultat.pack(padx=10, pady=10)

    def update_dependance_list(self):
        """
        Met à jour la liste des dépendances par rapport à celles
        actuellement tâches  présentes dans le planificateur.
        """
        self.lst_dependances.delete(0, tk.END)
        for nom in self.plan.taches:
            self.lst_dependances.insert(tk.END, nom)

    def ajouter_tache(self):
        """
        Récupère les données saisies dans le formulaire, crée une nouvelle tâche,
        ajoute au planificateur et met à jour la liste des dépendances.
        Affiche un message si les entrées sont invalides ou si il y a des doublons.
        """
        nom = self.entry_nom.get().strip()
        duree = self.entry_duree.get().strip()
        livraison = self.var_livraison.get()

        if not nom or not duree.isdigit():
            messagebox.showerror("Erreur", "Nom ou durée invalide.")
            return

        duree = int(duree)
        dependances = [self.lst_dependances.get(i) for i in self.lst_dependances.curselection()]

        if nom in self.plan.taches:
            messagebox.showerror("Erreur", f"La tâche '{nom}' existe déjà.")
            return

        try:
            t = Tache(nom, duree, dependances, livraison)
            self.plan.ajouter_tache(t)
            self.update_dependance_list()
            messagebox.showinfo("Succès", f"Tâche '{nom}' ajoutée.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def generer_planning(self):
        """
        Génère l’ordre des tâches et un planning à partir des données du planificateur.
        Affiche les résultats dans la zone de texte, avec la durée totale du projet en jour.
        """
        try:
            ordre = self.plan.generer_planning()
            planning = self.plan.ordonner_taches()
            duree = self.plan.duree_totale()

            self.txt_resultat.delete("1.0", tk.END)
            self.txt_resultat.insert(tk.END, "Ordre des tâches :\n")
            self.txt_resultat.insert(tk.END, " → ".join(ordre) + "\n\n")

            self.txt_resultat.insert(tk.END, "Planning détaillé :\n")
            for t in ordre:
                debut, fin = planning[t]
                tache = self.plan.taches[t]
                ligne = f"{t} : début = {debut}, fin = {fin} ({'livraison' if tache.livraison else 'tâche'})\n"
                self.txt_resultat.insert(tk.END, ligne)

            self.txt_resultat.insert(tk.END, f"\nDurée totale du projet : {duree} jours\n")

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfacePlanificateur(root)
    root.mainloop()