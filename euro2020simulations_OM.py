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

graph = nx.relabel_nodes(g, mapping)

with open('euro2020/euro2020_t0.json', 'r') as f:
    nodelist = json.load(f)

nodes = {}
for k, v in nodelist.items():
    try:
        nodes[mapping[k]] = float(v)
    except KeyError:
        print(f'node {k} not present in graph')
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
            print('node not present in graph')
            continue
from utils import *
from aggregate import *
from plots import *
import sys

# Model settings
media_opinions = [[], [avg_pros], [avg_pros, avg_cons], [avg_pros, avg_neut, avg_cons]]

max_it = 100000

for k in [1, 2, 3]:
    gammas, pms, media_op = [0.0, 0.5, 1.0, 1.5], [0.0, 0.5], media_opinions[k]
    #perform multiple runs and average results
    for gamma in gammas:
        for pm in pms:
            epsilon = 'heterogeneous'
            respath = 'res/'
            name = f'e{epsilon}_g{gamma}_pm{pm}_mo{media_op}'
            final_opinions, final_niter = read_dicts(respath, name, max_it)

            for run in range(1):
                if str(run) in final_opinions.keys() and str(run) in final_niter.keys(): 
                    print('run already present. skipping.')
                    run += 1
                else:
                    print(f'run {run} epsilon = {epsilon} gamma = {gamma} pm = {pm} media_op = {media_op}')    

                    #create model
                    model = op.AlgorithmicBiasMediaModel(graph)

                    #create configuration
                    config = mc.Configuration()
                    config.add_model_parameter("mu", 0.5)
#                         config.add_model_parameter("epsilon", epsilon)
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
                    iterations = model.steady_state(max_iterations=max_it, nsteady=3000, sensibility=0.001, node_status=True, progress_bar=True)

#                     with open(respath+f'iterations_{name}_maxit{max_it}.json', 'w') as ofile:
#                         json.dump(iterations, ofile)

                    finalopinions = iterations[-1]['status']
                    niter = int(iterations[-1]['iteration'])

                    final_opinions[run] = finalopinions
                    final_niter[run] = niter

                    write_dicts(respath, name, max_it, final_opinions, final_niter)

                    plotevolution(iterations, name=name, run=run)
                    plotdistribution(list(finalopinions.values()), name=name, run=run)