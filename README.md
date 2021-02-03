# Interface-de-collecte-et-presentation-d-informations-systeme

Tâches (fait = [x] , à faire = [ ]):

Agent:
- [x] Récupérer les caractéristiques suivantes : le nom de l'host, l'os, l'uptime, le noyau Linux
- [ ] Récupérer le type et la fréquence du CPU (ou des CPUs)
- [x] Récupérer les métriques suivantes : informations sur l'espace disques de chaque partitions, la charge CPU, la mémoire (totale, libre, occupée -dont buffers/cache)
- [ ] Vérifier qu'un ou plusieurs service(s) tourne(nt) sur la machine par l'intermédiaire d'un fichier de configuration
- [ ] [OPTIONNEL] Collecter également les taux de transferts réseaux, par interface
- [ ] [OPTIONNEL] Collecter les nombres de lectures/écritures disques
- [x] Envoyer les données de l'agent au serveur
- [ ] Formater les données envoyé de l'agent au serveur

Serveur:

- [ ] Interface http pour la collecte des données transmises par les agents
- [ ] Stockage des données dans une BD
- [ ] Interface de consultation des résultats
- [ ] [OPTIONNEL] Ajouter le choix de l'hôte sur l'interface graphique

Documentation:
- [ ] Indiquer toutes les dépendances du projet dans un fichier requirement.txt
- [ ] Faire des copies d'écrans de l'interface réalisé
- [ ] Mise à jour du document de clarification
