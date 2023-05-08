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

def read_dicts(path, name):
    print('reading dictionaries')
    try:
        with open(f'{path}/{name}.json', 'rt') as file:
            print('final_opinions already exists. reading json file')
            final_opinions = json.load(file)
    except:
        print('final_opinions created')
        final_opinions = {}
    
    return final_opinions

def write_dicts(path, name, final_opinions):
    with open(f'{path}/{name}.json', 'wt') as file:
        print(final_opinions)
        json.dump(final_opinions, file)