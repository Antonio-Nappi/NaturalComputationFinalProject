# Import delle librerie

import json
from multiprocessing.pool import Pool

from SnakeOil.client import Client
import math

#Definizione del UDP
class My_Problem():

    def __init__(self, filename):
        #carico i parametri
        d = json.load(open(filename, 'r'))
        self.params_keys = list(d.keys())
        # definisco i bound per i parametri
        lb = json.load(open('Parameters/lower_bounds', 'r'))
        ub = json.load(open('Parameters/upper_bounds', 'r'))
        self.lower_bounds=[value for value in lb.values()]
        self.upper_bounds=[value for value in ub.values()]

    def fitness(self, params_values):
        #ricostruisco il dizionario dei parametri
        params = dict(zip(self.params_keys, params_values))
        #codice per il multiprocessing, se si avviano duwe
        with Pool(2) as p:
            results=p.starmap(self.start_client, [(params, 3001), (params, 3002)])
            #risultati per il circuito Forza
            distRaced_forza,time_forza,length_forza = results[0]
            penalty_forza = (distRaced_forza-length_forza) / 10
            #Risultati per il circuito Wheel
            distRaced_wheel,time_wheel,length_wheel = results[1]
            penalty_alpine = (distRaced_wheel - length_wheel) / 10
            #Penalità
            penalty = penalty_alpine*penalty_forza
            del results
        print("valutata una fitness")
        #Nel caso in cui la macchina non finisce un giro
        if time_forza == 0 or time_wheel==0:
            return [math.inf]
        return [-(-penalty+((distRaced_forza / time_forza) * (distRaced_wheel/time_wheel)))] #penalizzare se corre di più della lunghezza del circuito , fare anzichè la somma il prodotto, cambiare circuito passando da alpine 1 al 2

    def get_bounds(self):
        #restituisce i bound dei parametri
        return (self.lower_bounds, self.upper_bounds)

 # Metodo di supporto per il multithreading in evaluate.
    def start_client(self, params, port):
        client = Client(params, port)
        return client.race()
