import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ndlib.models.ModelConfig as mc
import ndlib.models.opinions as op
import numpy as np
from plots import *
import networkx as nx
import os
import json
import gzip

plt.rcParams['axes.facecolor']='white'
plt.rcParams['savefig.facecolor']='white'
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 11, 'font.style': 'normal', 'font.family':'serif'})

def read_dicts(path, name, max_iterations):
    print('reading dictionaries')
    try:
        with open(f'{path}/final_opinions_{name}_maxit{max_iterations}.json', 'rt') as file:
            print('final_opinions already exists. reading json file')
            final_opinions = json.load(file)
    except:
        print('final_opinions created')
        final_opinions = {}

    try:
        with open(f'{path}/final_iterations_{name}_maxit{max_iterations}.json', 'rt') as file:
            print('final_iterations already exists. reading json file')
            final_iterations = json.load(file)
    except:
        print('final_iterations created')
        final_iterations = {}
    
    return final_opinions, final_iterations

def write_dicts(path, name,max_iterations, final_opinions, final_niter):
    with open(f'{path}/final_opinions_{name}_maxit{max_iterations}.json', 'wt') as file:
        print(final_opinions)
        json.dump(final_opinions, file)
        
    with open(f'{path}/final_iterations_{name}_maxit{max_iterations}.json', 'wt') as file:
        json.dump(final_niter, file)