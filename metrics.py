from utils import *
from scipy import stats

def nclusters(opinions, threshold):
    opinions = [float(el) for el in opinions]
    opinions = sorted(opinions)
    start = opinions[0]
    max_val = start + threshold
    c = (start, max_val)
    cluster = dict()
    for i in opinions:
        if i <= max_val:
            if c in cluster.keys():
                cluster[c] += 1
            else:
                cluster[c] = 1
        else:
            max_val = i + threshold
            c = (i, max_val)
            cluster[c] = 1
    #ora ho il dizionario con i cluster di una run
    C_num = len(opinions)**2
    C_den = 0
    for k in cluster.keys():
        C_den += cluster[k]*cluster[k]
    C = C_num / C_den
    return C

def entropy(opinions, n, nbins):
    bincounts, bin_edges = np.histogram(opinions, bins = np.linspace(0, 1, nbins))
    probabilities = bincounts/n
    entr = stats.entropy(probabilities)
    return entr

def pwdist(opinions):
    distances = []
    for i in range(len(opinions)):
        x_i = opinions[i]
        distances_i = []
        for j in range(len(opinions)):
            if i != j:
                x_j = opinions[j]
                d_ij = abs(x_i-x_j)
                distances_i.append(d_ij)
        avg_i = sum(distances_i)/len(distances_i)
        distances.append(avg_i)
    return sum(distances)/len(distances)

def compute_aggregate_metrics(filequintet):

    def _compute_avg_std(l):
        return np.average(np.array(l)), np.std(np.array(l))

    with gzip.open(filequintet, 'rt') as file:
        d = json.load(file)
        final_opinions = {int(k):{int(i): j for i, j in v.items()} for k,v in d.items()}
    
    clusters, entropies, pwdists = [], [], []
    for run in final_opinions.keys():
        finalopinions = final_opinions[run]
        clusters.append(nclusters(finalopinions, 0.01))
        entropies.append(entropy(finalopinions, len(finalopinions), len(finalopinions)+1))
        pwdists.append(pwdist(finalopinions))
    anc, stdnc = _compute_avg_std(clusters)
    aentr, stdentr = _compute_avg_std(entropies)
    apwd, stdpwd = _compute_avg_std(pwdists)
