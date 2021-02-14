#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# installer pip install gviz_api      --> c'est l'api google charts
import gviz_api
import sqlite3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler


ip ='192.168.1.101'
port =8003

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        conn = sqlite3.connect('ma_base2.db')
        cursor = conn.cursor()
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        #content_len = int(self.headers.get('Content-Length'))
        #post_body = self.rfile.read(content_len).decode('utf-8')
        #print(message)
        #print('USAGGEEEEE',message['informationsPartitions'][1])
        iii=0
        nom_dhote=message['nomHote']
        
        cursor.execute('SELECT EXISTS(SELECT 1 FROM T_HOTE WHERE nom_hote="%s" LIMIT 1)' % nom_dhote)
        hote_exists = cursor.fetchone()
        #cursor.execute("""SELECT EXISTS(SELECT 1 FROM T_HOTE WHERE nom_hote=(?))""", (message['nomHote']))
        
            ######################EXEMPLE DE DONNEES RECUS #########################################
#{'nomHote': 'rt-s111-pc',
 #'platforme': 'Linux',
 #'tempsActif': '0:40 heures',
 #'noyau': '4.15.0-135-generic',
 #'Processeur0': [' Intel(R) Core(TM) i7-7700 CPU @ 3.60GHz', 4200.0, 800.0, 3601.954875],
#'informationsPartitions': [{'usagePartition1': [78205652992, 22735433728, 51453468672, 30.6]},
 #                           {'usagePartition2': [91226112, 91226112, 0, 100.0]},
 #                           {'usagePartition3': [15204352, 15204352, 0, 100.0]},
 #                           {'usagePartition4': [13631488, 13631488, 0, 100.0]},
 #                           {'usagePartition5': [3932160, 3932160, 0, 100.0]},
 #                           {'usagePartition6': [36438016, 36438016, 0, 100.0]},
 #                           {'usagePartition7': [2490368, 2490368, 0, 100.0]},
 #                           {'usagePartition8': [147849216, 147849216, 0, 100.0]},
 #                           {'usagePartition9': [100663296, 32528384, 68134912, 32.3]},
 #                           {'usagePartition10': [15467544576, 8578719744, 6888824832, 55.5]}],
 # 'chargeCPU': 1.5,
 # 'memoireTotal': 16705232896,
 # 'memoireFree': 11619442688,
 # 'memoireOccupée': 2377269248,
 # 'memoireBuffer': 300761088,
 # 'memoireCache': 2407759872,
 # 'Services': [{'apache2': 'Actif', 'ssh': 'Inactif'}]}
        
        #print('L hote :',hote_exists[0])
        
        if(hote_exists[0] != 0):
            cursor.execute('SELECT id_hote,nom_hote FROM T_HOTE WHERE nom_hote="%s"' % nom_dhote)
            id_hote = cursor.fetchone()
            #print('L hote existe !',id_hote)
        else :
            cursor.execute('INSERT INTO T_HOTE(nom_hote) VALUES("%s")' % nom_dhote)
            conn.commit()
            cursor.execute('SELECT id_hote FROM T_HOTE WHERE nom_hote="%s"' % nom_dhote)
            id_hote = cursor.fetchone()
            #print('id_hote:',id_hote)
            id_hote=int(id_hote[0])
            #print('id:',id_hote)
            cursor.execute("""INSERT INTO T_SYSTEM(id_hote,plateforme_system,tempsactif_system,noyau_system) VALUES(?,?,?,?)""",
                           (id_hote,message['platforme'],message['tempsActif'],message['noyau']))
            conn.commit()
            cursor.execute("""INSERT INTO T_MEMOIRE(id_hote,total_memoire,free_memoire,used_memoire,buffer_memoire,cache_memoire) VALUES(?,?,?,?,?,?)""",
                           (id_hote,message['memoireTotal'],message['memoireFree'],message['memoireOccupée'],message['memoireBuffer'],message['memoireCache']))
            conn.commit()
            cursor.execute("""INSERT INTO T_CHARGE_CPU(id_hote,charge_cpu) VALUES(?,?)""",
                           (id_hote,message['chargeCPU']))
            conn.commit()
            
            for services in message['Services']:
                for noms in services:
                    #print(noms,services[noms])
                    cursor.execute("""INSERT INTO T_SERVICES(id_hote,nom_service,etat_service) VALUES(?,?,?)""",
                           (id_hote,noms,services[noms]))
                    conn.commit()
                
                
                
            cursor.execute("""INSERT INTO T_PROCESSEUR(id_hote,nom_processeur,max_processeur,min_processeur,actuel_processeur) VALUES(?,?,?,?,?)""",
                           (id_hote,message['Processeur0'][0],message['Processeur0'][1],message['Processeur0'][2],message['Processeur0'][3]))
            conn.commit()    
            for i in message['informationsPartitions']: #Dans les partitions
            
                for ii in message['informationsPartitions'][iii]:
                    #print('ii',iii,' :',ii)
                    iiiii=0
                    for iiii in i[ii]: 
                        #print('iiii',iiii)
                        if (iiiii==0):
                            total=iiii #memoire
                        if (iiiii==1):
                            used=iiii #memoire
                        if (iiiii==2):
                            free=iiii #memoire
                        if (iiiii==3):
                            percent=iiii #memoire
                        iiiii+=1
                iii+=1
                cursor.execute("""
                                       INSERT INTO T_PARTITION(id_hote,numero_partition,total_partition,used_partition,free_partition,percent_partition)
                                       VALUES(?,?,?,?,?,?)""", (id_hote,iii,total,used,free,percent))
                conn.commit()
            
        
                 
        self.send_response(200)
        self.end_headers()
        
    def do_GET(self):
        if self.path=="/index.html":
            self.send_response(301)
            self.send_header('Location','http://www.example.com')
            self.end_headers()
        elif self.path=="/stop":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Fermeture du serveur</title></head><body>Vous venez d eteindre le serveur.</body></html>","utf-8")) 
            httpd.server_close()
        elif self.path=="/createdb":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>CREATE DB</title></head><body>Vous venez de creer la base de donnee si elle n existait pas.</body></html>","utf-8")) 
            conn = sqlite3.connect('ma_base2.db')

#Fermer la connection à la base


#Créer une table avec SQLite
            cursor = conn.cursor()
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS T_HOTE(
                                   nom_hote TEXT,
                                   id_hote INTEGER PRIMARY KEY AUTOINCREMENT
                                   
                            );
                           """)
            
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS T_MEMOIRE(
                                   id_hote INTEGER ,
                                   total_memoire BIGINT,
                                   used_memoire BIGINT,
                                   free_memoire BIGINT,
                                   buffer_memoire BIGINT,
                                   cache_memoire BIGINT,
                                   FOREIGN KEY(id_hote) REFERENCES T_HOTE(id_hote)
                                   
                                   
                            );
                           """)
                           
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS T_CHARGE_CPU(
                                   id_hote INTEGER ,
                                   charge_cpu FLOAT,
                                   FOREIGN KEY(id_hote) REFERENCES T_HOTE(id_hote)
                                   
                            );
                           """)
                           
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS T_SERVICES(
                                   id_hote INTEGER,
                                   nom_service TEXT,
                                   etat_service TEXT,
                                   FOREIGN KEY(id_hote) REFERENCES T_HOTE(id_hote)
                                   
                            );
                           """)
                          
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS T_SYSTEM(
                                   id_hote INTEGER ,
                                   
                                   plateforme_system TEXT,
                                   tempsactif_system TEXT,
                                   noyau_system TEXT,
                                   FOREIGN KEY(id_hote) REFERENCES T_HOTE(id_hote)
                                   
                            );
                           """)
                           
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS T_PARTITION(
                                   id_hote INTEGER ,
                                   
                                   numero_partition INT,
                                   total_partition BIGINT,
                                   used_partition BIGINT,
                                   free_partition BIGINT,
                                   percent_partition FLOAT,
                                   FOREIGN KEY(id_hote) REFERENCES T_HOTE(id_hote)
                                   
                                   
                            );
                           """)
                            
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS T_PROCESSEUR(
                                   id_hote INTEGER ,
                                   nom_processeur TEXT,
                                   max_processeur FLOAT,
                                   min_processeur FLOAT,
                                   actuel_processeur FLOAT,
                                   FOREIGN KEY(id_hote) REFERENCES T_HOTE(id_hote)
                                   
                                   
                            );
                           """)
            conn.commit() 
        else :
            self.send_response(200)
            
            print(self.path)
            #self.wfile.write(b'Hello, world!')
            #self.wfile.write(self.path)
            if self.path.endswith(".jpeg"):
                f = open("."+self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type',        'image/jpg')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            self.end_headers()
            self.wfile.write(bytes(main(),"utf-8")) 



page_template = """
<html>
  <script src="https://www.gstatic.com/charts/loader.js"></script>
  <script>
    google.charts.load('current', {packages:['table']});

    google.charts.setOnLoadCallback(drawTable);
    function drawTable() {
      %(jscode1)s
      %(jscode2)s
      %(jscode3)s
      %(jscode4)s
      %(jscode5)s
      %(jscode6)s
      %(jscode7)s
      var jscode_table_hote = new google.visualization.Table(document.getElementById('table_div_jscode_hote'));
      jscode_table_hote.draw(jscode_data_hote, {showRowNumber: true});
      
      var jscode_table_memoire = new google.visualization.Table(document.getElementById('table_div_jscode_memoire'));
      jscode_table_memoire.draw(jscode_data_memoire, {showRowNumber: true});
      
      var jscode_table_charge_cpu = new google.visualization.Table(document.getElementById('table_div_jscode_charge_cpu'));
      jscode_table_charge_cpu.draw(jscode_data_charge_cpu, {showRowNumber: true});
      
      var jscode_table_services = new google.visualization.Table(document.getElementById('table_div_jscode_services'));
      jscode_table_services.draw(jscode_data_services, {showRowNumber: true});
      
      var jscode_table_partition = new google.visualization.Table(document.getElementById('table_div_jscode_partition'));
      jscode_table_partition.draw(jscode_data_partition, {showRowNumber: true});
      
      var jscode_table_system = new google.visualization.Table(document.getElementById('table_div_jscode_system'));
      jscode_table_system.draw(jscode_data_system, {showRowNumber: true});
      
      var jscode_table_processeur = new google.visualization.Table(document.getElementById('table_div_jscode_processeur'));
      jscode_table_processeur.draw(jscode_data_processeur, {showRowNumber: true});


    }
  </script>
  <body>
  
    <p><a href="/createdb">Create Database</a> |
    <a href="/stop">Stop Server</a></p>


    <H1>Les hotes</H1>
    <div id="table_div_jscode_hote"></div>
    <H1>Memoires</H1>
    <div id="table_div_jscode_memoire"></div>
    <H1>Charge CPU</H1>
    <div id="table_div_jscode_charge_cpu"></div>
    <H1>Services</H1>
    <div id="table_div_jscode_services"></div>
    <H1>Partitions</H1>
    <div id="table_div_jscode_partition"></div>
    <H1>Informations systeme</H1>
    <div id="table_div_jscode_system"></div>
    <H1>Processeurs</H1>
    <div id="table_div_jscode_processeur"></div>

   
  </body>
</html>
"""

#      var json_table = new google.visualization.Table(document.getElementById('table_div_json'));
#      var json_data = new google.visualization.DataTable(%(json)s, 0.6);
#      json_table.draw(json_data, {showRowNumber: true});

def main(): # cette methode me retourne ma page web avec mon js appliqué
  # Creating the data


    #query les informations de la bdd
  conn = sqlite3.connect('ma_base2.db')
  
  cursor = conn.cursor()
  #cursor.execute("""SELECT name, age FROM users""")
  #cursor.execute("""SELECT * 
  #              FROM T_HOTE
  #              INNER JOIN T_MEMOIRE
  #                   on T_HOTE.id_hote = T_MEMOIRE.id_hote
  #               INNER JOIN T_PARTITION
  #                   on T_HOTE.id_hote = T_PARTITION.id_hote
  #               INNER JOIN T_SYSTEM
  #                   on T_HOTE.id_hote = T_SYSTEM.id_hote
  #               INNER JOIN T_CHARGE_CPU
  #                   on T_HOTE.id_hote = T_CHARGE_CPU.id_hote
  #               INNER JOIN T_PROCESSEUR
  #                   on T_HOTE.id_hote = T_PROCESSEUR.id_hote
  #               INNER JOIN T_SERVICES
  #                   on T_HOTE.id_hote = T_SERVICES.id_hote
  #                   ;
                 
  
  #""")
  #users = cursor.fetchall()
  ##print(users)
  #cursor.execute("""SELECT * 
  #               FROM T_PARTITION
  #                   ;
  #""")
    
  
  ###############################HOTES################################
  cursor.execute("""SELECT * FROM T_HOTE;""")
  datas = cursor.fetchall()
  data_dictionnary={}
  data_list=[]
  for record in datas:
      data_dictionnary = {"id" : record[1],"nom" : record[0]}
      data_list.append(data_dictionnary)
  description2 = {"id": ("number", "id hote"),
                 "nom": ("string", "Nom d'hote")}
  data_table = gviz_api.DataTable(description2)
  data_table.LoadData(data_list)
  jscode1 = data_table.ToJSCode("jscode_data_hote",
                               columns_order=("id","nom"),
                               order_by="id")
  
  ###############################MEMOIRE################################
  cursor.execute("""SELECT * FROM T_MEMOIRE;""")
  datas = cursor.fetchall()
  data_dictionnary={}
  data_list=[]
  for record in datas:
      data_dictionnary = {"id" : record[0],"total_memoire" : record[1], "used_memoire" : record[2], "free_memoire" : record[3], "buffer_memoire" : record[4], "cache_memoire" : record[5]}
      data_list.append(data_dictionnary)
  description2 = {"id": ("number", "id hote"),
                 "total_memoire": ("number", "Memoire Totale"),
                 "used_memoire": ("number", "Memoire utilisee"),
                 "free_memoire": ("number", "Memoire libre"),
                 "buffer_memoire": ("number", "Buffer Memoire"),
                 "cache_memoire": ("number", "Cache Memoire")}
  data_table = gviz_api.DataTable(description2)
  data_table.LoadData(data_list)
  jscode2 = data_table.ToJSCode("jscode_data_memoire",
                               columns_order=("id","total_memoire", "used_memoire", "free_memoire","buffer_memoire", "cache_memoire"),
                               order_by="id")
 
  ###############################CHARGE_CPU################################
  cursor.execute("""SELECT * FROM T_CHARGE_CPU;""")
  datas = cursor.fetchall()
  data_dictionnary={}
  data_list=[]
  for record in datas:
      data_dictionnary = {"id" : record[0],"charge_cpu" : record[1]}
      data_list.append(data_dictionnary)
  description2 = {"id": ("number", "id hote"),
                 "charge_cpu": ("number", "Charge du CPU")}
  data_table = gviz_api.DataTable(description2)
  data_table.LoadData(data_list)
  jscode3 = data_table.ToJSCode("jscode_data_charge_cpu",
                               columns_order=("id","charge_cpu"),
                               order_by="id")

  ###############################SERVICES################################
  cursor.execute("""SELECT * FROM T_SERVICES;""")
  datas = cursor.fetchall()
  data_dictionnary={}
  data_list=[]
  for record in datas:
      data_dictionnary = {"id" : record[0],"nom_service" : record[1],"etat_service" : record[2]}
      data_list.append(data_dictionnary)
  description2 = {"id": ("number", "id hote"),
                  "nom_service": ("string", "Nom service"),
                 "etat_service": ("string", "Etat service")}
  data_table = gviz_api.DataTable(description2)
  data_table.LoadData(data_list)
  jscode4 = data_table.ToJSCode("jscode_data_services",
                               columns_order=("id","nom_service","etat_service"),
                               order_by="id")

  ###############################SYSTEM################################
  cursor.execute("""SELECT * FROM T_SYSTEM;""")
  datas = cursor.fetchall()
  data_dictionnary={}
  data_list=[]
  for record in datas:
      data_dictionnary = {"id" : record[0],"plateforme_system" : record[1],"tempsactif_system" : record[2],"noyau_system" : record[3]}
      data_list.append(data_dictionnary)
  description2 = {"id": ("number", "id hote"),
                  "plateforme_system": ("string", "Nom du systeme"),
                  "tempsactif_system": ("string", "Temps actif"),
                 "noyau_system": ("string", "Le noyau du systeme")}
  data_table = gviz_api.DataTable(description2)
  data_table.LoadData(data_list)
  jscode5 = data_table.ToJSCode("jscode_data_system",
                               columns_order=("id","plateforme_system","tempsactif_system","noyau_system"),
                               order_by="id")
            
  ###############################PROCESSEUR################################
  cursor.execute("""SELECT * FROM T_PROCESSEUR;""")
  datas = cursor.fetchall()
  data_dictionnary={}
  data_list=[]
  for record in datas:
      data_dictionnary = {"id" : record[0],"nom_processeur" : record[1], "max_processeur" : record[2], "min_processeur" : record[3], "actuel_processeur" : record[4]}
      data_list.append(data_dictionnary)
  description2 = {"id": ("number", "id hote"),
                 "nom_processeur": ("string", "Nom du processeur"),
                 "max_processeur": ("number", "Max"),
                 "min_processeur": ("number", "Min"),
                 "actuel_processeur": ("number", "Actuellement")}
  data_table = gviz_api.DataTable(description2)
  data_table.LoadData(data_list)
  jscode6 = data_table.ToJSCode("jscode_data_processeur",
                               columns_order=("id","nom_processeur", "max_processeur", "min_processeur","actuel_processeur"),
                               order_by="id")
            
  ###############################PARTITIONS################################
  cursor.execute("""SELECT * FROM T_PARTITION;""")
  datas = cursor.fetchall()
  data_dictionnary={}
  data_list=[]
  for record in datas:
      data_dictionnary = {"id" : record[0],"numero" : record[1], "total" : record[2], "used" : record[3], "free" : record[4], "percent" : record[5]}
      data_list.append(data_dictionnary)
  description2 = {"id": ("number", "id hote"),
                 "numero": ("number", "Numero de partition"),
                 "total": ("number", "Size"),
                 "used": ("number", "Used"),
                 "free": ("number", "Free"),
                 "percent": ("number", "Percent")}
  data_table = gviz_api.DataTable(description2)
  data_table.LoadData(data_list)
  jscode7 = data_table.ToJSCode("jscode_data_partition",
                               columns_order=("id","numero", "total", "used","free", "percent"),
                               order_by="id")
  # Put the JS code and JSON string into the template.
  print ("Content-type: text/html")
  #print
  return page_template % vars()
  

if __name__ == '__main__':

  httpd = HTTPServer((ip, port), SimpleHTTPRequestHandler) #penser à mettre l'adresse ip au lieu de localhost
                                                                        #car pas accès depuis l'extèrieur
  httpd.serve_forever()


        
        
        
