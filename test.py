import requests
from flask_testing import LiveServerTestCase
from app import run
import click

class MyTest(LiveServerTestCase):

    def create_app(self):
        app = run(False)
        return app

    def test_stats(self):
        response = requests.get(f"{self.get_server_url()}/stats")
        self.assertEqual(response.status_code, 200)
        
    def test_mutant(self):
        dna1 = '{"dna":["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]}' 
        response = requests.post(f"{self.get_server_url()}/mutant", dna1)
        self.assertEqual(response.status_code, 200)
        dna2 = '{"dna":["ATGCGA","CGGTGA","TTATCT","AGAAGG","CACCTA","TCACTG"]}' 
        response = requests.post(f"{self.get_server_url()}/mutant", dna2)
        self.assertEqual(response.status_code, 403)
