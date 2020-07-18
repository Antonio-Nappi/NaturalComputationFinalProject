from matplotlib import pyplot as plt
import numpy as np
import csv
import re
import os


def get_results_sade(name):
    i = 1
    fitness_values_seed1 = list()
    fitness_values_seed2 = list()
    fitness_values_seed3 = list()
    average_fitness_values = list()
    best_fitness_values = list()
    sd_fitness_values = list()
    for folder in os.listdir(name):
        print(folder)
        for dir in os.listdir(name+'\\'+folder):
            for f in sorted(os.listdir(name+'\\'+folder+'\\'+dir)):
                '''if re.match('[0-9]_.*_population',f):
                    os.rename(name+'\\'+folder+'\\'+dir+'\\'+f,name+'\\'+folder+'\\'+dir+'\\'+'0'+f)
                '''
                if re.match('.*_population',f):
                    print(name+'\\'+folder+'\\'+dir+'\\'+f)
                    with open(name+'\\'+folder+'\\'+dir+'\\'+f) as input_file:
                        reader = csv.DictReader(input_file)
                        tmp = []
                        for row in reader:
                            tmp.append(abs(float(row['fitness'])))
                        if i == 1:
                            fitness_values_seed1.append(tmp)
                        elif i ==2:
                            fitness_values_seed2.append(tmp)
                        else:
                            fitness_values_seed3.append(tmp)
        i +=1
    variant = list()
    variant.extend(fitness_values_seed1[49])

    variant.extend(fitness_values_seed3[49])

    variant.extend(fitness_values_seed2[49])
    for gen in range(len(fitness_values_seed1)):

        mean_individuals_seed1 = np.mean(fitness_values_seed1[gen])
        sd_individuals_seed1 = np.std(fitness_values_seed1[gen])
        max_individual_seed1 = np.max(fitness_values_seed1[gen])

        mean_individuals_seed2 = np.mean(fitness_values_seed2[gen])
        sd_individuals_seed2 = np.std(fitness_values_seed2[gen])
        max_individual_seed2 = np.max(fitness_values_seed2[gen])

        mean_individuals_seed3 = np.mean(fitness_values_seed3[gen])
        sd_individuals_seed3 = np.std(fitness_values_seed3[gen])
        max_individual_seed3 = np.max(fitness_values_seed3[gen])

        average_fitness_values.append((mean_individuals_seed1+mean_individuals_seed2+mean_individuals_seed3)/3)
        sd_fitness_values.append((sd_individuals_seed1+sd_individuals_seed2+sd_individuals_seed3)/3)
        best_fitness_values.append((max_individual_seed1+max_individual_seed2+max_individual_seed3)/3)
    return (average_fitness_values,sd_fitness_values,best_fitness_values,variant)

average_fitness_values_v6,sd_fitness_values_v6,best_fitness_values_v6,variant_6 = get_results_sade('variante_6')
average_fitness_values_v8,sd_fitness_values_v8,best_fitness_values_v8,variant_8 = get_results_sade('variante_8')

generations = [i for i in range(1,51)]
#Fitness media
plt.plot(generations,average_fitness_values_v6,label='best/1/bin')
plt.plot(generations,average_fitness_values_v8,label='rand-to-best/1/bin')
plt.xlabel("Generazione")
plt.ylabel("Fitness")
plt.legend(loc='best')
plt.title("Fitness media in funzione delle generazioni")
axes = plt.gca()
axes.set_xlim([1,51])
axes.set_ylim([1500,3000])
plt.xticks([i for i in range(0,51,5)])
plt.savefig('Andamento_fitness_media.png')
plt.show()

#Fitness dell'individuo migliore
plt.plot(generations,best_fitness_values_v6,label='best/1/bin')
plt.plot(generations,best_fitness_values_v8,label='rand-to-best/1/bin')
plt.xlabel("Generazione")
plt.ylabel("Fitness")
plt.legend(loc='best')
plt.title("Fitness dell'individuo migliore in funzione delle generazioni")
axes = plt.gca()
axes.set_xlim([1,51])
axes.set_ylim([1500,3000])
plt.xticks([i for i in range(0,51,5)])
plt.savefig('Andamento_fitness_best.png')
plt.show()

#Fitness media VS fitness migliore
plt.plot(generations,best_fitness_values_v6,'#1f77b4',label='best for best/1/bin',ls='-')
plt.plot(generations,best_fitness_values_v8,'#ff7f0e',label='best for rand-to-best/1/bin',ls='-')
plt.plot(generations,average_fitness_values_v6,'#1f77b4',label='average for -best/1/bin',ls='--')
plt.plot(generations,average_fitness_values_v8,'#ff7f0e',label='average for rand-to-best/1/bin',ls='--')
plt.xlabel("Generazione")
plt.ylabel("Fitness")
plt.legend(loc='best')
plt.title("Fitness media e dell'individuo migliore")
axes = plt.gca()
axes.set_xlim([1,51])
axes.set_ylim([1500,3000])
plt.xticks([i for i in range(0,51,5)])
plt.savefig('Andamento_fitness_best_and_average.png')
plt.show()


#deviazione standard della fitness
plt.plot(generations,sd_fitness_values_v6,label='best/1/bin')
plt.plot(generations,sd_fitness_values_v8,label='rand-to-best/1/bin')
plt.xlabel("Generazione")
plt.ylabel("Deviazione Standard")
plt.legend(loc='best')
plt.title("Deviazione standard in funzione delle generazioni")
axes = plt.gca()
axes.set_xlim([1,51])
axes.set_ylim([0,700])
plt.xticks([i for i in range(0,51,5)])
plt.yticks([i for i in range(0,701,50)])
plt.savefig('Andamento_sd.png')
plt.show()

variant = [variant_6,variant_8]
data = np.negative(variant)
labels=["best/1/bin","rand-to-best/1/bin"]
plt.boxplot(variant,showfliers=False)
plt.xticks(np.arange(len(labels))+1,labels)
plt.title("Distribuzione per le due varianti di SaDE")
plt.savefig("distribuzioni.png")
plt.show()

import csv
from itertools import zip_longest
export_data = zip_longest(*data, fillvalue = '')
with open('Risultati/comparazione.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow(("Best/1/bin", "Rand-to-best/1/bin"))
      wr.writerows(export_data)
myfile.close()