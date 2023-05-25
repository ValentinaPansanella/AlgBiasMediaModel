import numpy as np
import ndlib.models.ModelConfig as mc
import ndlib.models.opinions as op
import networkx as nx
import json
from utils import *
from aggregate import *
from plots import *
import csv

g = nx.read_edgelist('../dataset/euro2020_edgelist.csv', delimiter=',', nodetype=str)

graph = nx.relabel_nodes(g, mapping={n:int(n) for n in list(g.nodes)}, copy=True)

with open('../dataset/euro2020_t0.json', 'r') as f:
    nodelist = json.load(f)

nodes = {}
for k, v in nodelist.items():
    nodes[int(k)] = float(v)

pros = {k:v for k,v in nodes.items() if v <= 0.4}
avg_pros = np.average(np.array(list(pros.values())))
cons = {k:v for k,v in nodes.items() if v >= 0.6}
avg_cons = np.average(np.array(list(cons.values())))
neut = {k:v for k,v in nodes.items() if v < 0.6 and v > 0.4}
avg_neut = np.average(np.array(list(neut.values())))

openmindedness = {}
with open('../res/euro2020_openMindedness.csv', 'r') as f:
    csv_reader = csv.reader(f)
    next(csv_reader)
    for row in csv_reader:
        openmindedness[int(row[0])] = float(row[1])

# Model settings
media_opinions = [[avg_pros], [avg_cons], [avg_neut], [avg_pros, avg_cons], [avg_pros, avg_cons, avg_neut]]
max_it = 100
gammas, pms, epsilons = [0.0, 0.5, 1.0, 1.5], [0.1], [0.2, 0.3, 0.4, 'heterogeneous']

#perform multiple runs and average results
for media_op in media_opinions:
    k = len(media_op)
    for gamma in gammas:
        for pm in pms:
            for epsilon in epsilons:
                respath = '../res/'
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

                final_opinions, final_niter = read_dicts(respath, name)

                for run in range(1):
                    if str(run) in final_opinions.keys(): 
                        print(f'run {run} already present. skipping.')
                        run += 1
                    else:
                        print(f'run {run} {name}')    

                        #create model
                        model = op.AlgorithmicBiasMediaModel(graph)

                        #create configuration
                        config = mc.Configuration()
                        config.add_model_parameter("mu", 0.5)
                        config.add_model_parameter("gamma", gamma)
                        config.add_model_parameter("gamma_media", gamma)
                        config.add_model_parameter("p", pm)
                        config.add_model_parameter("k", k)

                        if epsilon == 'heterogeneous':
                            for node in list(graph.nodes):
                                config.add_node_configuration("epsilon_node", node, float(openmindedness[node]))
                        else:
                            config.add_model_parameter("epsilon", epsilon)

                        #configure model
                        model.set_initial_status(configuration=config, initial_status=nodes)
                        model.set_media_opinions(media_op)

                        #perform iterations untill convergence
                        iterations = model.steady_state(max_iterations=max_it, nsteady=500, sensibility=0.01, node_status=True, progress_bar=True)
                        
                        final_opinions[run] = iterations[-1]['status']
                        final_niter[run] = iterations[-1]['iteration']

                        write_dicts(respath, name, final_opinions, final_niter)
































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
