#coding utf-8

import platform,socket,psutil

# writing a function to convert bytes to GigaByte
def bytes_to_GB(bytes):
    gb = bytes/(1024*1024*1024)
    gb = round(gb, 2)
    return gb
    
#On récup
info={}


################################################Caractéristiques########################################################################
info['nomHote']=socket.gethostname() #Nom de l'hôte 
info['platforme']=platform.system() #Système d'exploitation
# getting the system up time from the uptime file at proc directory
with open("/proc/uptime", "r") as f:
    tempsActif = f.read().split(" ")[0].strip()
tempsActif = int(float(tempsActif))
uptime_heures = tempsActif // 3600
uptime_minutes = (tempsActif % 3600) // 60
info['tempsActif'] = str(uptime_heures) + ":" + str(uptime_minutes) + " heures" #temps d'activité (uptime)
info['Noyau']=platform.release() #Noyau

#info['CPU']=(str(psutil.cpu_percent()) + ", " + str(psutil.virtual_memory()), psutil.cpu_freq())



"""
# Displaying The CPU information

print("\n\t\t\t CPU Information\n")

# This code will print the number of CPU cores present
info['CpuNbrCoeursPhysiques'] = psutil.cpu_count(logical=False)
info['CpuNbrCoeursTotal'] = psutil.cpu_count(logical=True)
print ("FREQUENCE : " + str(psutil.cpu_freq()))


# This will print the maximum, minimum and current CPU frequency
cpu_frequency = psutil.cpu_freq()
print(f"[+] Max Frequency : {cpu_frequency.max:.2f}Mhz")
print(f"[+] Min Frequency : {cpu_frequency.min:.2f}Mhz")
print(f"[+] Current Frequency : {cpu_frequency.current:.2f}Mhz")
print("\n")

# This will print the usage of CPU per core
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"[+] CPU Usage of Core {i} : {percentage}%")
print(f"[+] Total CPU Usage : {psutil.cpu_percent()}%")


# reading the cpuinfo file to print the name of
# the CPU present
with open("/proc/cpuinfo", "r") as f:
    file_info = f.readlines()

cpuinfo = [x.strip().split(":")[1] for x in file_info if "model name"  in x]
for index, item in enumerate(cpuinfo):
    print("[+] Processor " + str(index) + " : " + item)

    #Processeurs
#info['platformeVersion']=platform.version()
#info['architecture']=platform.machine()

"""

################################################Métriques########################################################################

partitionsDisque = psutil.disk_partitions()
print(partitionsDisque)

#Permet d'afficher pour chaque partition les infos qu'on veut
#TO DO, créer une liste avec toute les infos pour une partition, une liste par partition !
for partition in partitionsDisque:
    print(partition.mountpoint)

info['ChargeCPU'] = psutil.cpu_percent() #En pourcentage


####Mémoire

virtual_memory = psutil.virtual_memory()
virtual_memory.buffers #bytes_to_GB(virtual_memory.buffers) Fonction utile, mais valeur trop faible pour être utile

info['MemoireTotal'] =virtual_memory.total
info['MemoireFree'] =virtual_memory.free
info['MemoireOccupée']=virtual_memory.used
info['MemoireBuffer'] =virtual_memory.buffers #7 buffers, 8 cache (mémoire) EN BYTES PENSER A CONVERTIR
info['MemoireCache'] =virtual_memory.cached

print (info)#affichage des informations listés

