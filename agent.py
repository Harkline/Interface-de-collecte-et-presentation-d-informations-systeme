#coding utf-8

import platform,socket,psutil,requests,json,csv,os,subprocess

# Conversion octets en Gigaoctets
def octetsAGigaoctets(bytes):
    go = bytes/(1024*1024*1024)
    go = round(go, 2)
    return go
    
#Structure principal ou toutes les informations sont stockés
info={}

################################################Caractéristiques########################################################################
info['nomHote']=socket.gethostname() #Nom de l'hôte 
info['platforme']=platform.system() #Système d'exploitation
# Obtient le temps d'activité en regardant dans le fichier /proc/uptime
with open("/proc/uptime", "r") as f:
    tempsActif = f.read().split(" ")[0].strip()
tempsActif = int(float(tempsActif))
tempsActifHeures = tempsActif // 3600
tempsActifMinutes = (tempsActif % 3600) // 60
info['tempsActif'] = str(tempsActifHeures) + ":" + str(tempsActifMinutes) + " heures" #temps d'activité (uptime)
info['noyau']=platform.release() #Noyau

# Lit les information du fichier cpuinfo pour afficher le nom du processeur
with open("/proc/cpuinfo", "r") as f:
    infoFichier = f.readlines()

nbreProc=0 #Permet de différencier les processeurs s'il y en a plusieurs
itemTampon="" #Permet de vérifier pendant le traitement si le thread vient du même processeur
cpuinfo = [x.strip().split(":")[1] for x in infoFichier if "model name"  in x]
for index, item in enumerate(cpuinfo):
    #Alternative vu que la fréquence récupéré n'est celle que du premier processeur
    if nbreProc == 0:
        frequenceProcesseur = psutil.cpu_freq()
        #Nom du processeur, fréquence max, fréquence min, fréquence actuelle
        info["Processeur" + str(nbreProc)] = item, frequenceProcesseur.max, frequenceProcesseur.min, frequenceProcesseur.current
        itemTampon = item
        nbreProc+=1
    #Si un autre processeur est détecté
    elif item != itemTampon:
        info["Processeur" + str(nbreProc)] = item
        itemTampon = item
        nbreProc+=1



################################################Métriques########################################################################

informationDisque = []
partitionsDisque = psutil.disk_partitions()
compteur = 0 #Compteur pour différencier les partitions

#Permet d'afficher pour chaque partition les infos qu'on veut
for partition in partitionsDisque:
    tamponInfoPartition = {}
    compteur += 1
    usagePartitionStr = "usagePartition" + str(compteur) #Permet de différencier les partitions à l'aide d'un simple compteur
    tamponInfoPartition[usagePartitionStr] = psutil.disk_usage(partition.mountpoint)
    informationDisque.append(tamponInfoPartition)

info['informationsPartitions'] = informationDisque #Les informations des partitions
info['chargeCPU'] = psutil.cpu_percent() #En pourcentage


######Mémoire

memoireVirtuel = psutil.virtual_memory()
memoireVirtuel.buffers #octetsAGigaoctets(virtual_memory.buffers) Fonction utile, mais valeur trop faible pour être utile

info['memoireTotal'] = memoireVirtuel.total
info['memoireFree'] = memoireVirtuel.free
info['memoireOccupée']= memoireVirtuel.used
info['memoireBuffer'] = memoireVirtuel.buffers #7 buffers, 8 cache (mémoire) EN BYTES PENSER A CONVERTIR
info['memoireCache'] = memoireVirtuel.cached

######Services (CSV reader)
servicesliste = []
serviceActifInactif = {}
nomFichier = "config.csv"
#On ouvre le fichier en mode lecture seule "r"
fichierCSV = csv.reader(open(nomFichier,"r"))
#Pour chaque ligne du fichier CSV
for ligne in fichierCSV:
    #On récupère les services à chaque ligne du fichier CSV
    for service in ligne: 

        #On vérifie son statut (en cachant le résultat de la commande dans le terminal)
        with open(os.devnull, 'wb') as cacheSortie:
            estEnMarche = subprocess.Popen(['service', service, 'status'], stdout=cacheSortie, stderr=cacheSortie).wait()

        if estEnMarche == 0:
            serviceActifInactif[service] = 'Actif'
        #Code 768 signifie qu'il est arrêté, mais si le code est différent cela veut dire que le service n'existe pas, donc il est inactif
        else:
            serviceActifInactif[service] = 'Inactif'

servicesliste.append(serviceActifInactif)
info["Services"] = servicesliste

#testYL
######Nombre Lectures/Ecritures
#Obtient le nombre de lectures/écritures disque pour l'ensemble des boucle (/dev/loop(numéro)) l'ensemble des partitions du/des disques (exemple : /dev/sda(numéro)) et tous les appareils montés (exemple clef USB : /dev/sdf(numéro)

disqueEcritureLecture = psutil.disk_io_counters()

info['lectureDisques'] = disqueEcritureLecture.read_count
info['ecritureDisques'] = disqueEcritureLecture.write_count

#Debug
print (info)#affichage des informations listés

################################################Envoie de données (POST)########################################################
port = "8097"
url = "http://192.168.3.25:"+port

info = json.dumps(info)
#r = requests.post(url, data = info) #192.168.3.25  8097
