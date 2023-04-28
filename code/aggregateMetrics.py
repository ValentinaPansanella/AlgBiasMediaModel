import numpy as np
import json
from metrics import *

class aggregateMetrics:

    def __init__(self, final_opinions, final_iterations):
        self.finalopinions=final_opinions
        self.finaliterations=final_iterations
        self.metrics = {
            'avg_nc': [],
            'avg_entr': [],
            'avg_pwdist': [],
            'avg_nit': [],
            'avg_op': []
        }
    
    @staticmethod
    def compute_avg_std(m):
        return np.average(np.array(m)), np.std(np.array(m))
    
    def compute_metrics(self):

        clusters, entropies, pwdists, avgops, nit = [], [], [], [], []
        
        for run in self.finalopinions.keys():
            finalopinions = list(self.finalopinions[run].values())
            finaliterations = int(self.finaliterations[run])

            clusters.append(nclusters(finalopinions, 0.01))
            entropies.append(entropy(finalopinions, len(finalopinions), len(finalopinions)+1))
            pwdists.append(pwdist(finalopinions))
            avgops.append(np.average(np.array(finalopinions)))
            nit.append(finaliterations)

        anc, stdnc = self.compute_avg_std(clusters)
        aentr, stdentr = self.compute_avg_std(entropies)
        apwd, stdpwd = self.compute_avg_std(pwdists)
        aop, stdop = self.compute_avg_std(avgops)
        ait, stdit = self.compute_avg_std(nit)

        self.metrics['avg_nc'] = (anc, stdnc)
        self.metrics['avg_entr'] = (aentr, stdentr)
        self.metrics['avg_pwdist'] = (apwd, stdpwd)
        self.metrics['avg_op'] = (aop, stdop)
        self.metrics['avg_nit'] = (ait, stdit)

    def get_avg_nc(self):
        return self.metrics['avg_nc']
    
    def get_avg_entr(self):
        return self.metrics['avg_entr']
    
    def get_avg_pwdist(self):
        return self.metrics['avg_pwdist']
    
    def get_avg_opinion(self):
        return self.metrics['avg_op']
    
    def get_avg_nit(self):
        return self.metrics['avg_nit']
    





