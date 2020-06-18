import csv

values = list()
keys = list()
rows = list()
with open('74_ants_results.csv','r') as inf:
    reader = csv.reader(inf)
    for row in reader:
        rows.append(row)

    keys = rows[0][1:]
    for value in rows[1][1:]:
        print(value,type(value))
        values.append(float(value))
import json
with open('best_ant_parameters','w') as outf:
    outf.write(json.dumps(dict(zip(keys,values))))