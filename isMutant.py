import sys
import json
from flask import current_app as app
from flask_restful import Resource
from flask import Response
import time
from itertools import groupby
import random

def isMutant(dna):
  #first clean and convert string to matrix
  dna =  "".join(str(x) for x in dna)
  print("dna is")
  print(dna)
  data = dna.replace('{', '')
  data = data.replace('}', '')
  data = data.replace('[', '')
  data = data.replace(']', '')
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
          return True
  return False

if __name__ == '__main__':
   print(isMutant(sys.argv[1]))
