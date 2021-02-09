# Interface-de-collecte-et-presentation-d-informations-systeme

Tâches (fait = [x] , à faire = [ ]):

Agent:
- [x] Récupérer les caractéristiques suivantes : le nom de l'host, l'os, l'uptime, le noyau Linux
- [x] Récupérer le type et la fréquence du CPU (ou des CPUs)
- [x] Récupérer les métriques suivantes : informations sur l'espace disques de chaque partitions, la charge CPU, la mémoire (totale, libre, occupée -dont buffers/cache)
- [x] Vérifier qu'un ou plusieurs service(s) tourne(nt) sur la machine par l'intermédiaire d'un fichier de configuration
- [ ] [OPTIONNEL] Collecter également les taux de transferts réseaux, par interface
- [x] [OPTIONNEL] Collecter les nombres de lectures/écritures disques [ ! Récupère pour les boucles, toutes les partitions de tous les disques et toutes appareils branchés exemple : clefs USB]
- [x] Envoyer les données de l'agent au serveur
- [x] Formater les données envoyé de l'agent au serveur

Serveur:
- [x] Récupération des informations transmisses par l'agent sur un port dans un serveur python
- [x] Vérification de l'existence de l'hôte
- [x] Vérifier l'existence de la BDD sinon la créer et préparer les tables 
- [x] Insertion des informations reçus des agents dans la BDD (mysqli)
- [x] Creation d'une redirection vers une page web sur un port spécifique avec l'implémentation du JS (google charts)  
- [x] [OPTIONNEL] Gèrer les do_GET pour ajouter quelques fonctionnalitée (supprimer BDD,fermer le site http, voir autres...)
- [ ] Mise en forme de la page web présentent les informations sur les clients
- [ ] [OPTIONNEL] Ajouter le choix de l'hôte sur l'interface graphique

Documentation:
- [ ] Indiquer toutes les dépendances du projet dans un fichier requirement.txt
- [ ] Faire des copies d'écrans de l'interface réalisé
- [ ] Mise à jour du document de clarification
