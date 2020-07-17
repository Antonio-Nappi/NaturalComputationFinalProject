# Importazione delle librerie Python.
import csv
import json
from multiprocessing import Pool
import numpy as np

# Importazione dei moduli custom.
from client import Client


# Definizione della classe Continuous Ant Colony System.
# L'implementazione è in accordo con l'algoritmo definito nel testo
# "Natural Computing ALgorithms" a cura di A. Brabazo, M. O'Neill e S. McGarraghy.
class CACS():
    # Inizializzatore, prende in ingresso:
    # - il nome del file JSON dei parametri;
    # - il nome della directory in cui salvare i risultati (default: directory corrente);
    # - il numero di formiche che costituiscono una colonia (default: None);
    # - il fattore di evaporazione (default: 1);
    # - il numero di colonie (default: 100).
    #
    # Inizializza:
    # il dizionario dei parametri;
    # l'indice dell'iterazione iniziale;
    # il nome della directory in cui salvare i risultati;
    # il numero dei parametri;
    # il numero di formiche, pari al numero di parametri se non diversamente indicato;
    # il numero di colonie;
    # il dizionario dei range;
    # il dizionario delle medie delle distribuzioni gaussiane (max perché si vuole
    # massimizzare);
    # il dizionario delle deviazioni standard delle distribuzioni gaussiane;
    # il fattore di evaporazione;
    # il valore della fitness del miglior individuo.
    def __init__(self, param_file_name, dir_name='.\\', n_ants=None, evaporation=1,
                 stop_condition=100):
        with open(param_file_name, "r") as file:
            self._params = json.load(file)
        self._starting_iteration = 0
        self._dir_name = dir_name
        self._n_params = len(self._params.keys())
        self._n_ants = len(self._params.keys()) if n_ants is None else n_ants
        self._stop_condition = stop_condition
        self._bounds = {}
        self._x_max = {}
        self._sigma = {}
        self._evaporation = evaporation
        self._fitness = None

    # Metodo che guida l'evoluzione.
    # Prende in ingresso opzionalmente una tupla contenente:
    # - il nome del file CSV del migliore risultato;
    # - il nome del file CSV dell'ultimo risultato.
    def evolve(self, recover=None):
        # Nuova evoluzione da 0.
        # Dopo aver definito la soluzione iniziale, la valuta e aggiorna
        # il valore della funzione di fitness del migliore individuo.
        if recover is None:
            self.initial_solution()
            fitness = self.evaluate(self._x_max)
            print("Initial fitness:", fitness)
            if self.is_higher_fitness(fitness):
                self.update(fitness)

        # Ripristino dello stato di un'evoluzione interrotta.
        else:
            self.recover_solution(recover[0], recover[1])

        # Ciclo di lunghezza pari al numero di colonie da far evolvere.
        # In ogni iterazione:
        # - crea una lista per contenere i risultati di ciascuna formica;
        # - per ogni formica, crea un dizionario che associa a ogni parametro il valore
        # estratto da una distribuzione gaussiana con media e deviazione standard,
        # vincolato dai limiti definiti, e aggiungi alla lista dei risultati una tupla
        # contenente la fitness ottenuta dalla formica e i parametri che definiscono
        # la formica;
        # - ordina la lista dei risultati in ordine decrescente di fitness
        # - se la migliore fitness ottenuta dalla colonia corrente supera la migliore fitness
        # ottenuta fino a questo punto dell'evoluzione, procede con l'aggiornamento;
        # - salva i risultati ottenuti;
        # - aggiorna la deviazione standard.
        for iter in range(self._starting_iteration, self._stop_condition):
            results = []
            print('iteration {}, fitness {}'.format(iter + 1, self._fitness))
            for k in range(self._n_ants):
                print('ant {}'.format(k + 1))
                x = {}
                for key in self._params.keys():
                    drawn = np.random.normal(self._x_max[key], self._sigma[key])
                    if drawn < self._bounds[key][0]:
                        drawn = self._bounds[key][0]
                    elif drawn > self._bounds[key][1]:
                        drawn = self._bounds[key][1]
                    x[key] = drawn
                fitness = self.evaluate(x)
                results.append((fitness, x))

            results.sort(key=lambda t: t[0], reverse=True)
            if self.is_higher_fitness(results[0][0]):
                self.store_data(
                    '{}{}_ants_results_newbest.csv'.format(self._dir_name, iter + 1), results)
                self.update(results[0][0], results[0][1])
            else:
                self.store_data('{}{}_ants_results.csv'.format(self._dir_name, iter + 1), results)
            self.compute_sigma(results)

    # Metodo che definisce la soluzione iniziale.
    # Per ogni parametro:
    # - inserisce nel dizionario dei limiti una tupla contenente il limite inferiore
    # e il limite superiore, calcolati secondo quanto definito nel file dei parametri;
    # - inserisce nel dizionario delle medie il valore di default del parametro;
    # - inserisce nel dizionario delle deviazioni standard la deviazione standard iniziale,
    # calcolata come 3 volte la differenza tra il limite superiore e il limite inferiore
    # (per assicurare un'equa distribuzione nel range [lower bound, upper bound].
    def initial_solution(self):
        for key in self._params.keys():
            self._bounds[key] = (self._params[key][0] * self._params[key][1],
                                 self._params[key][0] * self._params[key][2])
            self._x_max[key] = self._params[key][0]
            self._sigma[key] = 3 * (self._bounds[key][1] - self._bounds[key][0])

    # Metodo che ripristina lo stato di un'evoluzione interrotta.
    # Prende in ingresso:
    # - il nome del file CSV del migliore risultato;
    # - il nome del file CSV dell'ultimo risultato.
    # Inizializza l'indice dell'iterazione iniziale in base al file relativo
    # all'ultimo risultato.
    # Per ogni parametro, inserisce nel dizionario dei limiti una tupla contenente il limite
    # inferiore e il limite superiore, calcolati secondo quanto definito nel file dei parametri.
    # Leggendo il file del miglior risultato, aggiorna la fitness e il dizionario delle medie.
    # Leggendo il file dell'ultimo risultato, aggiorna il dizionario delle deviazioni standard.
    def recover_solution(self, best, last):
        self._starting_iteration = int(last.split("_")[0])

        for key in self._params.keys():
            self._bounds[key] = (self._params[key][0] * self._params[key][1],
                                 self._params[key][0] * self._params[key][2])

        with open('{}{}'.format(self._dir_name, best), "r") as best_file:
            reader = csv.reader(best_file, delimiter=",")
            for index, row in enumerate(reader):
                if index == 1:
                    fitness = float(row[0])
                    if self.is_higher_fitness(fitness):
                        self.update(fitness)
                    self._x_max = dict(zip(self._params.keys(), [float(elem) for elem in row[1:]]))
                    break

        with open('{}{}'.format(self._dir_name, last), "r") as last_file:
            reader = csv.reader(last_file, delimiter=",")
            results = []
            for index, row in enumerate(reader):
                if index > 0:
                    results.append(
                        (None, dict(zip(self._params.keys(), [float(elem) for elem in row[1:]]))))
            self.compute_sigma(results)

    # Metodo che valuta la qualità di una soluzione.
    # Prende in ingresso il dizionario contenente la soluzione da valutare.
    # Avvia la simulazione con due client con gli stessi parametri su due porte differenti,
    # una per ciascuno dei server avviati; per ciascuna simulazione riceve informazioni
    # sulla distanza percorsa, il tempo impiegato e la lunghezza del tracciato (considerando
    # i due lap, quindi doppia).
    # Per ciascuna simulazione, calcola la distanza percorsa in più rispetto alla lunghezza
    # del tracciato; successivamente, calcola il prodotto delle due grandezze così ottenute,
    # per inserirlo come penalità nella funzione di fitness.
    # Restituisce il prodotto delle velocità medie a cui è sottratta la penalità; restituisce
    # una fitness pari a infinito negativo se si sono verificati eventi che hanno compromesso
    # la simulazione.
    def evaluate(self, params):
        with Pool(2) as p:
            results = p.starmap(self.start_client, [(params, 3001), (params, 3002)])
            distRaced_forza, time_forza, length_forza = results[0]
            distRaced_wheel, time_wheel, length_wheel = results[1]
        extra_dist_forza = (distRaced_forza - length_forza) / 10
        extra_dist_wheel = (distRaced_wheel - length_wheel) / 10
        extra_dist_penalty = extra_dist_forza * extra_dist_wheel
        if time_forza == 0 or time_wheel == 0:
            return - np.inf
        return (distRaced_forza / time_forza) * (
                distRaced_wheel / time_wheel) - extra_dist_penalty

    # Metodo di supporto per il multithreading in evaluate.
    def start_client(self, params, port):
        client = Client(params, port)
        return client.race()

    # Variante del metodo di valutazione per l'esecuzione su un solo circuito.
    # def evaluate(self, params):
    #     with Pool(1) as p:
    #         results = p.starmap(Client, [(params, 3001)])
    #         distRaced_forza, time_forza, length_forza = results[0].info
    #     extra_dist_forza = (distRaced_forza - length_forza) / 10
    #     extra_dist_penalty = extra_dist_forza ** 2
    #     if time_forza == 0:
    #         return - np.inf
    #     return (distRaced_forza / time_forza) ** 2 - extra_dist_penalty

    # Metodo che verifica se si è ottenuta una nuova migliore fitness.
    def is_higher_fitness(self, fitness):
        if self._fitness is None or fitness > self._fitness:
            return True
        else:
            return False

    # Metodo che aggiorna la fitness e il dizionario delle medie.
    def update(self, fitness, x_max=None):
        self._fitness = fitness
        if x_max is not None:
            self._x_max = x_max

    # Metodo che calcola e aggiorna il dizionario delle deviazioni standard.
    # Per ciascun parametro, la deviazione standard è calcolata in base a tutti
    # i valori estratti dalle formiche dell'ultima colonia.
    def compute_sigma(self, results):
        xs = [elem[1] for elem in results]
        for key in self._params.keys():
            xi = [elem[key] for elem in xs]
            self._sigma[key] = self._evaporation * np.std(xi)

    # Metodo che si occupa del salvataggio dei dati.
    # Salva in un file CSV la fitness e i parametri di ogni formica, in ordine
    # decrescente di fitness.
    # Salva in un file JSON i parametri della migliore formica.
    def store_data(self, filename, results):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            header_row = ['fitness']
            header_row.extend(self._params.keys())
            writer.writerow(header_row)
            for result in results:
                row = [result[0]]
                row.extend(result[1].values())
                writer.writerow(row)
        with open(filename[:-4], 'w', newline='') as f:
            json.dump(results[0][1], f)
