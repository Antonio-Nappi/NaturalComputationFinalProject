import json
import pygmo
import csv
import os
keys =[
'backontracksx',
'backward',
'brake',
'brakingpacefast',
'brakingpaceslow',
'carmaxvisib',
'carmin',
'clutch_release',
'clutchslip',
'clutchspin',
'consideredstr8',
'dnsh1rpm',
'dnsh2rpm',
'dnsh3rpm',
'dnsh4rpm',
'dnsh5rpm',
'fullstis',
'fullstmaxsx',
'ignoreinfleA',
'obvious',
'obviousbase',
'offroad',
'oksyp',
'pointingahead',
's2cen',
's2sen',
'safeatanyspeed',
'sensang',
'senslim',
'seriousABS',
'skidsev1',
'slipdec',
'sortofontrack',
'spincutclip',
'spincutint',
'spincutslp',
'st',
'stC',
'steer2edge',
'str8thresh',
'stst',
'sxappropriatest1',
'sxappropriatest2',
'sycon1',
'sycon2',
'upsh2rpm',
'upsh3rpm',
'upsh4rpm',
'upsh5rpm',
'upsh6rpm',
'wheeldia',
'wwlim'
]

def store_population(filename,population):
    to_store = list()
    for i in range(len(population)):
        to_store.append([float(population.get_f()[i]),list(population.get_x()[i])])
    print(type(to_store))
    print(to_store[0])
    to_store = to_store.sort(key=lambda x:x[0])
    print(to_store[0])
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        header_row = ['fitness']
        header_row.extend(keys)
        writer.writerow(header_row)
        for result in to_store:
            writer.writerow(result)
    store_best_and_worst(filename,population)


def load_population(filename,pg_prob):
    population = pygmo.population(pg_prob)
    with open('{}_individuals/'.format(len(population))+filename,'r',newline='') as inf:
        reader = csv.reader(inf)
        for row in reader:
            population.push_back([row[1]],[row[0]])
    return population
'''
def store_population(filename,population):
    keys = list()
    with open('keys.txt','r') as f:
        for line in f.readlines():
            keys.append(line[:-1])
    with open(filename,'w') as f:
        for i in range(len(population)):
            values = population.get_x()[i]
            d = dict(zip(keys,values))
            json_object = json.dumps(d)
            f.write('{}\n'.format(json_object))
    with open('best_{}'.format(filename),'w') as f:
        best = population.champion_x
        d = dict(zip(keys, best))
        json_object = json.dumps(d)
        f.write('{}\n'.format(json_object))

def from_population_to_parameters(population):
'''
def store_best_and_worst(filename,population):
    with open('best_{}'.format(filename), 'w') as f:
        best = population.champion_x
        d = dict(zip(keys, best))
        json_object = json.dumps(d)
        f.write('{}\n'.format(json_object))
    with open('worst_{}'.format(filename), 'w') as f:
        worst = population.get_x()[population.worst_idx()]
        d = dict(zip(keys, worst))
        json_object = json.dumps(d)
        f.write('{}\n'.format(json_object))

##TODO function to pass from parameter(json object) to population(np.array of values) easily
