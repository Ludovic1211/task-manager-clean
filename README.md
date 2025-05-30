
-------------------Structure Du Projet---------------------
taskmanager/
├── __init__.py
├── tache.py               # Classe Tache
├── planificateur.py       # Classe Planificateur
├── exemple_donnees.py     # Les Tâches du projet actuel
interface_planificateur.py # Interface graphique principale (Tkinter)
├
main.py

<3-------------pour lancer le main.py---------------<3--
uv run main.py en étant dans "task-manager-clean"

<3------<3-------pour lancer l'interface--<3-------------
python interface_planificateur.py

----<3--------------Interface:------------------------------
Ajout de tâches avec : nom, durée (en jours), livraison (oui/non), dépendances vers d'autres tâches

-Visualisation de l’ordre des tâches à effectuer 
-Génération automatique du planning avec dates de début et de fin
-Calcul de la durée totale du projet

-------------------Contenu du Taskmanager-------------------
 Exemple de données
  -liste des taches pour le projet actuel ( maison)

 Planificateur
  -création du planificateur
  -réalisation du tri topologique

 Tache.py
   -Création de la classe tache avec les facteurs qui la composent
   -Préparation de la facon dont la classe s'affiche 

-----------explication d'un tri topologique-----------------------
   -représenter le nombre de fois qu'un sommet peut etre parcouru
   -tester chaque sommet puis numéroté
   -inverser l'ordre obtenu pour avoir un des ordres possibles
   -considérer une tache comme un sommet sur un graphique orienté 



