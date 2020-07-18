#import delle librerie
from Server import Server
from SaDE.utils import store_population
from SaDE import problem
import pygmo
import time

def evolve_population_DE_algorithm(gen, variant, variant_adpt, population):
    algo = pygmo.algorithm(pygmo.sade(gen, variant, variant_adpt))
    algo.set_verbosity(1)
    new_pop = algo.evolve(population)
    return new_pop, algo

if __name__ == "__main__":
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

    # definisco un User Defined Problem come richiesto da pygmo
    p = problem.My_Problem('Parameters/0_times_evolved_parameters')
    pg_prob = pygmo.problem(p)
    #scelta del numero di individui
    individuals = 100
    for seed in seeds:

        fname = 0
        # imposto il seed
        pygmo.set_global_rng_seed(seed)
        for variant in [6,8]: # le due varianti: rand-to-best e best
            for i in range(50):
                population = pygmo.population(pg_prob, individuals)# definisco la popolazione per il problema
                last_pop, algo = evolve_population_DE_algorithm(1, variant, 2, population) # faccio evolvere la popolazione
                uda = algo.extract(pygmo.sade) #estraggo le informazioni dell'algoritmo
                fname += 1
                store_population('100_individuals/{}_times_evolved_population'.format(fname),
                                 last_pop, fname)  #salvo la popolazione ad ogni generazione
                if uda is None:
                    print("ERRORE")
                with open('log_file_{}_generations.txt'.format(fname), 'w') as f: #salvo il file di log
                    for line in uda.get_log():
                        f.write('{}\n'.format(line))