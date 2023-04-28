import os
from datetime import datetime
import networkx as nx
import tqdm
progress_bar = True
import json
import pickle
import csv

def create_dictionaries(timestamps, dataset_name='euro2020'):
    t2node2opinions = dict()
    for t in timestamps.keys():
        t2node2opinions[t] = dict()
        filename = f'{dataset_name}_{timestamps[t]}.json'
        with open(f'{dataset_name}/{filename}', 'r') as f:
            node2op = json.load(f)
            for k, v in node2op.items():
                t2node2opinions[t][k] = float(v)

    with open(f'euro2020_t2node2opinions.pickle', 'wb') as ofile:
        pickle.dump(t2node2opinions, ofile)        
    return t2node2opinions 

def sortNeighOps(g, v, t, t2node2opinions, opvt):
    neighs = list(g.neighbors(v))
    opinions = [t2node2opinions[t][u] for u in neighs if len(neighs)>0]
    sorted_opinions = sorted(opinions, key=lambda x: abs(x-opvt))
    return sorted_opinions
    

def createGraph(dataset_name, timestamps, t):
    g = nx.Graph()
    filename = f'{dataset_name}_edgelist.csv'
    with open(dataset_name+'/'+filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # the below statement will skip the first row
        for line in csv_reader:
            a = line[0]
            b = line[1]
            g.add_edge(a, b)
    return g

def estimation(opvt, opvt1, sorted_vals):
    errs = []
    estimated_opinions = []
    est_opvt1=opvt
    for oput in sorted_vals:
        est_opvt1 = (est_opvt1 + oput)/2
        err = abs(est_opvt1 - opvt1)
        estimated_opinions.append(est_opvt1)
        errs.append(err)
    try:
        i = len(errs) - 1 - errs[::-1].index(min(errs))
        last_op = sorted_vals[i]
        cb = abs(last_op - opvt) 
    
        if errs[i] < abs(opvt-opvt1):
            return cb, errs[i], estimated_opinions[i]        
        else:
            return 0.0, abs(opvt-opvt1), opvt
    except:
        return -1.0
        

def politicalLeaning(opvt):
    if opvt < 0.4:
        orientation='Democrat'
    elif opvt > 0.6:
        orientation = 'Republican'
    else:
        orientation = 'Moderate'
    return orientation









