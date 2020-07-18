# Importazione delle librerie Python.
import time
import numpy as np
import os
# Importazione dei moduli custom.
from Server import Server
from CACS import CACS

# Modulo main.
if __name__ == "__main__":
    # Lista dei fattori di evaporazione.
    evaps = ['1.25', '1.50', '1.75']

    # Lista dei seed
    seeds = [190196, 211294, 290796]

    # Definizione e avvio di due server indipendenti come thread separati.
    # Ciascun oggetto della classe Server prende in ingresso il nome del tracciato.
    server_forza = Server('forza')
    server_forza.start()
    server_wheel = Server('wheel')
    server_wheel.start()

    # Pausa dell'esecuzione per permettere ai server di avviarsi correttamente
    # prima di procedere con l'esecuzione dei client.
    time.sleep(10)

    # Esecuzione dei client al variare del fattore di evaporazione e del seed.
    for evap in evaps:
        for seed in seeds:
            # Impostazione del seed di numpy.
            np.random.seed(seed)

            # Nome della directory in cui salvare i risultati.
            dirname = 'ants_evap_{}_seed_{}\\'.format(evap, seed)
            os.makedirs(os.path.dirname(dirname), exist_ok=True)
            # Oggetto di classe CACS, prende in ingresso:
            # - il nome del file JSON dei parametri;
            # - il nome della directory, definito prima;
            # - il numero di formiche che costituiscono una colonia;
            # - il fattore di evaporazione;
            # - il numero di colonie.
            c = CACS('Parameters/default_parameters_with_bounds', dir_name=dirname, n_ants=48,
                     evaporation=float(evap), stop_condition=50)

            # Esecuzione dell'evoluzione della colonia.
            # Opzionalmente può prendere in ingresso una tupla contenente
            # due nomi di file, così da poter riprendere un'evoluzione
            # avviata precedentemente ma interrotta; la tupla deve contenere:
            # - il nome del file CSV del migliore risultato;
            # - il nome del file CSV dell'ultimo risultato.
            # I file indicati devono essere contenuti nella directory indicata
            # nel costruttore.
            c.evolve()
