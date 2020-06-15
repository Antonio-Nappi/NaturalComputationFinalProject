import json

lb = dict()
up = dict()

with open('default_parameters_with_bounds','r') as inf:
    json_object = json.load(inf)
    for key in json_object.keys():
        lb[key]=json_object[key][0]*json_object[key][1]
        up[key] = json_object[key][0]*json_object[key][2]
    with open('lower_bounds','w') as outf1,open('upper_bounds','w') as outf2:
        json.dump(lb,outf1)
        json.dump(up,outf2)