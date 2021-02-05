#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# installer pip install gviz_api      --> c'est l'api google charts
import gviz_api
import sqlite3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        #content_len = int(self.headers.get('Content-Length'))
        #post_body = self.rfile.read(content_len).decode('utf-8')
        print(message['informationsPartitions'])
        for i in message['informationsPartitions']:
                print ('i :',i.get(0))
        self.send_response(200)
        
    def do_GET(self):
        if self.path=="/index.html":
            self.send_response(301)
            self.send_header('Location','http://www.example.com')
            self.end_headers()
        elif self.path=="/stop":
            httpd.server_close()
            
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
  conn = sqlite3.connect('ma_base.db')
  
  cursor = conn.cursor()
  cursor.execute("""SELECT name, age FROM users""")
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
  
  httpd = HTTPServer(('192.168.1.101', 8097), SimpleHTTPRequestHandler) #penser à mettre l'adresse ip au lieu de localhost
                                                                        #car pas accès depuis l'extèrieur
  httpd.serve_forever()


# piste pour gestion json :https://gist.github.com/nitaku/10d0662536f37a087e1b
  # do_post à tester, semble fonctionnel
  #def do_POST(self):
   #     length = int(self.headers.get('content-length'))
    #    message = json.loads(self.rfile.read(length))
     #   message['date_ms'] = int(time.time()) * 1000
      #  _g_posts.append(message)
       # self._set_headers()
        #self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
        
# format des usagePartition https://psutil.readthedocs.io/en/latest/  psutil.disk_usage(path)