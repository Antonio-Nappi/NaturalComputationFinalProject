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
            keys.append(line[:-1])
    with open(filename,'w') as f:
        for i in range(len(population)):
            values = population.get_x()[i]
            d = dict(zip(keys,values))
            json_object = json.dumps(d)
            f.write('{}\n'.format(json_object))
    with open('best_{}'.format(filename)) as f:
        best = population.champion_x
        d = dict(zip(keys, best))
        json_object = json.dumps(d)
        f.write('{}\n'.format(json_object))
