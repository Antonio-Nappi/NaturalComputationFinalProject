import json


def load_population(filename):
    population = list()
    with open(filename,'r') as f:
        for line in f.readlines():
            population.append(json.loads(line))
    return population

def store_population(filename,population):
    keys = list()
    with open('keys.txt','r') as f:
        for line in f.readlines():
            keys.append(line)
    with open(filename,'w') as f:
        for i in range(len(population)):
            values = population.get_x()[i]
            d = dict(zip(keys,values))
            json_object = json.dumps(d)
            f.write('{}\\n'.format(json_object))
