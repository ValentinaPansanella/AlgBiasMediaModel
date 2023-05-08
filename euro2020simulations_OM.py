from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import seaborn as sns
import future.utils
import numpy as np
import ndlib.models.ModelConfig as mc
import ndlib.models.opinions as op
import networkx as nx
import os
import json
import gzip
from scipy import stats

g = nx.read_edgelist('euro2020/euro2020_edgelist.csv', delimiter=',', nodetype=str, )

mapping = dict()
i = 0
for nodename in g.nodes():
    mapping[nodename] = i
    i+=1

with open('euro2020/node_mapping.json', 'w') as f:
    json.dump(mapping, f)

reversemapping = {v: k for k, v in mapping.items()}

graph = nx.relabel_nodes(g, mapping)

with open('euro2020/euro2020_t0.json', 'r') as f:
    nodelist = json.load(f)

nodes = {}
for k, v in nodelist.items():
    try:
        nodes[mapping[k]] = float(v)
    except KeyError:
        # print(f'node {k} not present in graph')
        continue

pros = {k:v for k,v in nodes.items() if v <= 0.4}
avg_pros = np.average(np.array(list(pros.values())))
cons = {k:v for k,v in nodes.items() if v >= 0.6}
avg_cons = np.average(np.array(list(cons.values())))
neut = {k:v for k,v in nodes.items() if v < 0.6 and v > 0.4}
avg_neut = np.average(np.array(list(neut.values())))

import csv
openmindedness = {}
with open('euro2020/euro2020_openMindedness.csv', 'r') as f:
    csv_reader = csv.reader(f)
    next(csv_reader)
    for row in csv_reader:
        try:
            openmindedness[mapping[row[1]]] = float(row[2])
        except KeyError:
            # print('node not present in graph')
            continue
from utils import *
from aggregate import *
from plots import *

# Model settings
media_opinions = [[avg_pros], [avg_cons], [avg_neut]]
print(media_opinions)

max_it = 100000
    
gammas, pms, epsilons = [1.5, 1.0, 1.5, 0.0], [0.5, 0.0], [0.2, 0.3, 0.4]

#perform multiple runs and average results
for media_op in media_opinions:
    k = len(media_op)
    for gamma in gammas:
        for pm in pms:
            epsilon = 'heterogeneous'
            respath = 'res/'
            media = "media" if pm == 0.5 else "nomedia"
            if media == 'media':
                if media_op[0] == avg_pros: 
                    mo='avg_pros'
                elif media_op[0] == avg_cons:
                    mo='avg_cons'
                elif media_op[0] == avg_neut:
                    mo='avg_neut'
                name = f'{epsilon}_g{gamma}_{media}_{mo}'
            elif media == 'nomedia':
                name = f'{epsilon}_g{gamma}_{media}'

            final_opinions = read_dicts(respath, name)

            for run in range(1):
                if str(run) in final_opinions.keys(): 
                    print('run already present. skipping.')
                    run += 1
                else:
                    print(f'run {name}')    

                    #create model
                    model = op.AlgorithmicBiasMediaModel(graph)

                    #create configuration
                    config = mc.Configuration()
                    config.add_model_parameter("mu", 0.5)
                    config.add_model_parameter("gamma", gamma)
                    config.add_model_parameter("gamma_media", gamma)
                    config.add_model_parameter("p", pm)
                    config.add_model_parameter("k", k)

                    for node in list(graph.nodes):
                        config.add_node_configuration("epsilon_node", node, float(openmindedness[node]))

                    #configure model
                    model.set_initial_status(configuration=config, initial_status=nodes)
                    model.set_media_opinions(media_op)

                    #perform iterations untill convergence
                    iterations = model.steady_state(max_iterations=max_it, nsteady=500, sensibility=0.001, node_status=True, progress_bar=True)

                    finalopinions = iterations[-1]['status']
                    
                    to_write = {reversemapping[k]: v for k, v in finalopinions.items()}

                    write_dicts(respath, name, max_it, to_write)


































# for file in os.listdir('res/'):
#     if file.startswith('final_opinions'):
#         filename = file.split('_')[:6]
#         # print(filename)
#         if filename[2] == 'heterogeneous':
#             if filename[4] == 'pm0.5':
#                 if filename[5] == 'mo[0.865708635554234].json':
#                     filename = 'heterogeneous_'+filename[3]+'_'+'media'+'_'+'avg_cons.json'
#                 elif filename[5] == 'mo[0.2825807341574699].json':
#                     filename = 'heterogeneous_'+filename[3]+'_'+'media'+'_'+'avg_pros.json'
#                 elif filename[5] == 'mo[0.48528938156222684].json':
#                     filename = 'heterogeneous_'+filename[3]+'_'+'media'+'_'+'avg_neut.json'
#                 elif filename[5] == 'mo[0.2825807341574699, 0.865708635554234].json':
#                     filename = 'heterogeneous_'+filename[3]+'_'+'media'+'_'+'polarised.json'
#                 elif filename[5] == 'mo[0.2825807341574699, 48528938156222684, 0.865708635554234].json':
#                     filename = 'heterogeneous_'+filename[3]+'_'+'media'+'_'+'balanced.json'
#             elif filename[4] == 'pm0.0':
#                 filename = 'heterogeneous_'+filename[3]+'_'+'nomedia.json'
#             try:
#                 os.rename('res/'+file, 'res/'+filename)
#             except:
#                 print('already renamed')
#         elif filename[2].startswith('e'):
#             if filename[4] == 'pm0.5':
#                 if filename[5] == 'mo[0.865708635554234].json':
#                     filename = filename[2]+'_'+filename[3]+'_'+'media'+'_'+'avg_cons.json'
#                 elif filename[5] == 'mo[0.2825807341574699].json':
#                     filename = filename[2]+'_'+filename[3]+'_'+'media'+'_'+'avg_pros.json'
#                 elif filename[5] == 'mo[0.48528938156222684].json':
#                     filename = filename[2]+'_'+filename[3]+'_'+'media'+'_'+'avg_neut.json'
#                 elif filename[5] == 'mo[0.2825807341574699, 0.865708635554234].json':
#                     filename = filename[2]+'_'+filename[3]+'_'+'media'+'_'+'polarised.json'
#                 elif filename[5] == 'mo[0.2825807341574699, 48528938156222684, 0.865708635554234].json':
#                     filename = filename[2]+'_'+filename[3]+'_'+'media'+'_'+'balanced.json'
#             elif filename[4] == 'pm0.0':
#                 filename = filename[2]+'_'+filename[3]+'_'+'nomedia.json'
#             try:
#                 os.rename('res/'+file, 'res/'+filename)
#             except:
#                 print('already renamed')

# for file in os.listdir('res/'):
#     print(file)