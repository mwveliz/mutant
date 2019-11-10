import json
from flask import current_app as app
from flask import jsonify
from flask_restful import Resource
from flask import Response
import time
import sqlite3



class stats(Resource):
    def get(self):
        """
        ---
        responses:
         200:
           description: Stats
        """

        try:
          json_docs=[]
          _id = id
          print(app.config["DATABASE"])
          con = sqlite3.connect(app.config["DATABASE"])
          cursor = con.cursor()
          #look for mutants
          queryMutants ="SELECT dna from mutants WHERE ismutant = 1"
          cursor.execute(queryMutants)
          muts=cursor.fetchall()
          #look for humans
          queryHumans ="SELECT dna from mutants WHERE ismutant = 0"
          cursor.execute(queryHumans)
          hums=cursor.fetchall()
          ratio = 0
          if len(hums)>0:
            ratio = len(muts)/len(hums)
          header = {"success":True, "code": 200, "message":"OK", "version":"2.0.0", "timestamp": int(time.time())}
          body = {'count_mutant_dna':  len(muts),'count_human_dna': len(hums),'ratio':ratio}

          return jsonify({"header" : header, "body":body})

        except Exception as e:
          #cursor.close()
          print(str(e))
          #header = "{success:False, code: 400, message:"+e+}
          header = {"success":False, "code": 400, "message":str(e), "version":"2.0.0", "timestamp": int(time.time())}
          return Response(json.dumps(header), status=400)
