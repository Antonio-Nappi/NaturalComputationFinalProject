import json
import csv
import os
#Chiavi del dizionario dei parametri
keys =[
'backontracksx',
'backward',
'brakingpacefast',
'brakingpaceslow',
'carmaxvisib',
'carmin',
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
#Salvataggio della popolazione su file
def store_population(filename,population,fname):
    to_store = list()
    for i in range(len(population)):
        to_store.append((float(population.get_f()[i]),list(population.get_x()[i]))) #estrazione dell'individuo e della sua fitness
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    #Salva su file in formato csv
    with open(filename+'.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        header_row = ['fitness']
        header_row.extend(keys)
        writer.writerow(header_row)
        for result in to_store:
            row = [result[0]]
            row.extend(result[1])
            writer.writerow(row)