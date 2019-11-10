import json
from flask import current_app as app
from flask import jsonify, request
from flask_restful import Resource
from flask import Response, make_response
import time
from itertools import groupby
import random
import sqlite3


class mutant(Resource):
    
    #Function that checks if mutant was or not in sqlite db and inset
    def InDB(self, adnString, valbool):
      adnString = "".join(str(x) for x in adnString if x!="," and x!="\"" and x!=" ")     
      print(app.config["DATABASE"])
      
      con = sqlite3.connect(app.config["DATABASE"])
      cursor= con.cursor() 
      cursor.execute('create table if not exists mutants(id INTEGER PRIMARY KEY AUTOINCREMENT, dna TEXT, ismutant INTEGER)')
      con.commit()
      query ="SELECT dna from mutants WHERE dna LIKE '%"+adnString+"%'"
      cursor.execute(query)
      resultados=cursor.fetchall()
      if len(resultados)>0:
          return True
      vals = [(adnString, valbool)] # 1 is mutant 0 is human 
      cursor.executemany("INSERT INTO mutants VALUES(null, ?, ?)", vals)
      con.commit()    
      return False
    
    
    def post(self):
        """
        ---
        parameters:
         - in: body
           name: dns
           schema:
              example:
                {
                  dns:["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]
                }                       
              properties:
                dns:
                    type: array
                    description: DNA of candidate
           required: true
        responses:
         200:
           description: Ok- is mutant
         403:
           description: Forbidden- is not mutant

        """
        try:
          dna = json.dumps(request.get_json(force=True))
          dna =  "".join(str(x) for x in dna if x!="d" and x!="n" and x!="a" and x!=":" )
          print(dna)                   
          #first clean and convert string to matrix
          data = dna.replace('{', '')
          data = data.replace('}', '')
          data = data.replace('[', '')
          data = data.replace(']', '')
          adnString = data
          data = list(data.split(','))
          data = list(map(lambda el:[char for char in el if char != ' ' and char!= '"' ], data))

          n_rows = len(data)
          #avoiding repeated random padding
          lft = [ [random.randint(0, 2 ** n_rows - 1)] * i for i in range(n_rows) ]
          rgt = list(reversed(lft))
          header = {"success":True, "code": 200, "message":"OK", "version":"2.0.0", "timestamp": int(time.time())}

          repeats = 0
          #transpose matrix for evaluating adjacents only
          transpositions = {
              'horizontal' : data,
              'vertical'   : zip(*data),
              'diag_forw'  : zip(* [lft[i] + data[i] + data[i] for i in range(n_rows)] ),
              'diag_back'  : zip(* [rgt[i] + data[i] + data[i] for i in range(n_rows)] ),
          }
          for direction, transp in transpositions.items():
              for row in transp:
                runs = [len(list(g)) for _, g in groupby(row)]
                repeats += sum(u for u in runs if u > 3)# if more than three then mutant
                print(row,repeats)
                if (repeats>0):
                  if(self.InDB(adnString, 1)):
                    print('not in db, inserting')
                  return jsonify({"header" : header, "body":True})

          header = {"success":False, "code": 403, "message":"Forbidden", "version":"2.0.0", "timestamp": int(time.time())}
          if(self.InDB(adnString, 0)):
              print('not in db, inserting')                     
            
          return make_response(jsonify({"header" : header, "body":False}), 403)

        except Exception as e:
          print(str(e))
          header = {"success":False, "code": 400, "message":str(e), "version":"2.0.0", "timestamp": int(time.time())}
          return Response(json.dumps(header), status=400)
