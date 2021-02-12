#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# installer pip install gviz_api      --> c'est l'api google charts
import gviz_api
import sqlite3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        conn = sqlite3.connect('ma_base2.db')
        cursor = conn.cursor()
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        #content_len = int(self.headers.get('Content-Length'))
        #post_body = self.rfile.read(content_len).decode('utf-8')
        print(message)
        print('USAGGEEEEE',message['informationsPartitions'][1])
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
        
        print('L hote existe !',hote_exists[0])
        if(hote_exists[0]==1 or hote_exists[0]== None):
            cursor.execute('SELECT id_hote,nom_hote FROM T_HOTE WHERE nom_hote="%s"' % nom_dhote)
            id_hote = cursor.fetchone()
            print('L hote existe !',hote_exists[0],id_hote[0],id_hote[1])
        if(hote_exists[0]!=1 and hote_exists[0]!= None ) :
            cursor.execute('INSERT INTO T_HOTE(nom_hote) VALUES("%s")' % nom_dhote)

            cursor.execute('SELECT id_hote FROM T_HOTE WHERE nom_hote="%s"' % nom_dhote)
            id_hote = cursor.fetchone()
            print('id_hote:',id_hote)
            id_hote=int(id_hote[0])
            print('id:',id_hote)
            cursor.execute("""INSERT INTO T_SYSTEM(id_hote,plateforme_system,tempsactif_system,noyau_system) VALUES(?,?,?,?)""",
                           (id_hote,message['platforme'],message['tempsActif'],message['noyau']))
            
            cursor.execute("""INSERT INTO T_MEMOIRE(id_hote,total_memoire,free_memoire,used_memoire,buffer_memoire,cache_memoire) VALUES(?,?,?,?,?,?)""",
                           (id_hote,message['memoireTotal'],message['memoireFree'],message['memoireOccupée'],message['memoireBuffer'],message['memoireCache']))
            
            cursor.execute("""INSERT INTO T_CHARGE_CPU(id_hote,charge_cpu) VALUES(?,?)""",
                           (id_hote,message['chargeCPU']))
            
            
            for services in message['Services']:
                for noms in services:
                    print(noms,services[noms])
                    cursor.execute("""INSERT INTO T_SERVICES(id_hote,nom_service,etat_service) VALUES(?,?,?)""",
                           (id_hote,noms,services[noms]))

                
                
                
            cursor.execute("""INSERT INTO T_PROCESSEUR(id_hote,nom_processeur,max_processeur,min_processeur,actuel_processeur) VALUES(?,?,?,?,?)""",
                           (id_hote,message['Processeur0'][0],message['Processeur0'][1],message['Processeur0'][2],message['Processeur0'][3]))
                
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
            
        
        #for i in message['informationsPartitions']:
         #   iii+=1
          #  parition ="'"+'usagePartition'+str(iii)+"'"
           # print(parition)
            #print ('i :',i[parition])
            #for ii in i[parition.strip('"')]:
             #    print ('ii :',ii)
                 
        self.send_response(200)
        
    def do_GET(self):
        if self.path=="/index.html":
            self.send_response(301)
            self.send_header('Location','http://www.example.com')
            self.end_headers()
        elif self.path=="/stop":
            httpd.server_close()
        elif self.path=="/createdb":
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
            self.end_headers()
            print(self.path)
            #self.wfile.write(b'Hello, world!')
            #self.wfile.write(self.path)
            self.wfile.write(bytes(main(),"utf-8")) 



page_template = """
<html>
  <script src="https://www.gstatic.com/charts/loader.js"></script>
  <script>
    google.charts.load('current', {packages:['table']});

    google.charts.setOnLoadCallback(drawTable);
    function drawTable() {
      %(jscode)s
      var jscode_table = new google.visualization.Table(document.getElementById('table_div_jscode'));
      jscode_table.draw(jscode_data, {showRowNumber: true});

      var json_table = new google.visualization.Table(document.getElementById('table_div_json'));
      var json_data = new google.visualization.DataTable(%(json)s, 0.6);
      json_table.draw(json_data, {showRowNumber: true});
    }
  </script>
  <body>
    <H1>Table created using ToJSCode</H1>
    <div id="table_div_jscode"></div>
    <H1>Table created using ToJSon</H1>
    <div id="table_div_json"></div>
  </body>
</html>
"""

def main(): # cette methode me retourne ma page web avec mon js appliqué
  # Creating the data


    #query les informations de la bdd
  conn = sqlite3.connect('ma_base2.db')
  
  cursor = conn.cursor()
  #cursor.execute("""SELECT name, age FROM users""")
  cursor.execute("""SELECT * 
                 FROM T_HOTE
                 INNER JOIN T_MEMOIRE
                     on T_HOTE.id_hote = T_MEMOIRE.id_hote
                 INNER JOIN T_PARTITION
                     on T_HOTE.id_hote = T_PARTITION.id_hote
                 INNER JOIN T_SYSTEM
                     on T_HOTE.id_hote = T_SYSTEM.id_hote
                 INNER JOIN T_CHARGE_CPU
                     on T_HOTE.id_hote = T_CHARGE_CPU.id_hote
                 INNER JOIN T_PROCESSEUR
                     on T_HOTE.id_hote = T_PROCESSEUR.id_hote
                 INNER JOIN T_SERVICES
                     on T_HOTE.id_hote = T_SERVICES.id_hote
                     ;
                 
  
  """)
  user1 = cursor.fetchone()
  user2 = cursor.fetchone()
  user3 = cursor.fetchone()
  print(user1,user2 ,user3)
  
  # fin de la partie sql
  
  # deux exemple de déclaration d'une liste
  description = {"name": ("string", "Name"),
                 "salary": ("number", "Salary"),
                 "full_time": ("boolean", "Full Time Employee")}
  data = [{"name": "Mike", "salary": (10000, "$10,000"), "full_time": True},
          {"name": "Jim", "salary": (800, "$800"), "full_time": False},
          {"name": "Alice", "salary": (12500, "$12,500"), "full_time": True},
          {"name": "Bob", "salary": (7000, "$7,000"), "full_time": True}]

  # Loading it into gviz_api.DataTable
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)

  # Create a JavaScript code string.
  jscode = data_table.ToJSCode("jscode_data",
                               columns_order=("name", "salary", "full_time"),
                               order_by="salary")
  # Create a JSON string.
  json = data_table.ToJSon(columns_order=("name", "salary", "full_time"),
                           order_by="salary")

  # Put the JS code and JSON string into the template.
  print ("Content-type: text/html")
  #print
  return page_template % vars()
  

if __name__ == '__main__':
  
  httpd = HTTPServer(('192.168.1.101', 8001), SimpleHTTPRequestHandler) #penser à mettre l'adresse ip au lieu de localhost
                                                                        #car pas accès depuis l'extèrieur
  httpd.serve_forever()


        
        
        
