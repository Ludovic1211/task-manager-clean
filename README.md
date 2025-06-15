**Task Manager Clean** est une application Python avec interface graphique permettant de :

- Définir des tâches à planifier (durée, dépendances, livraison)
- Générer un planning sous contraintes (tâches/livraisons simultanées)
- Visualiser la planification sous forme de liste et de diagramme de Gantt
- Sauvegarder et recharger des projets facilement

## Interface graphique

L’interface utilisateur permet :

- L’ajout manuel ou multiple de tâches
- La suppression et l’affichage en tableau
- Le réglage du nombre maximal de tâches et de livraisons simultanées
- L’affichage du planning détaillé et de sa durée totale
- Une visualisation Gantt interactive (via matplotlib)

## Contraintes prises en compte

Lors de la génération du planning :

- Une tâche ne peut commencer que si toutes ses dépendances sont terminées
- Un nombre maximal de tâches peut être exécuté en parallèle (`max_taches`)
- Un nombre maximal de livraisons peut avoir lieu simultanément (`max_livraisons`)

## Tests

Les modules sont testés avec `pytest`, avec suivi de la couverture :

## particularitées
Lors du mancement de l'interface, une fenetre souvrira pour vous expliquer son fonctionnement 


il peut y avoir un problème d'environnement que nos n'avons pas pu régler directement. Pour exécuter l'interface par "python interface.py" il n'y a pas besoin d'etre dans taskmanager. Ce probleème d'environnement bloque aussi le fichier test de l'interface graphique et c'est pour cela que ce dernier a été retiré et placé dans "loupé"

