from utils import *
import json
import aggregateMetrics as am

def aggregate(max_iterations=100000):
    if not os.path.exists("../aggregate/"):
        os.mkdir('../aggregate/')

    epsilons, gammas, pms, media_op = [0.2, 0.3, 0.4, 0.5], [0.0, 0.5, 1.0, 1.5], [0.0, 0.1, 0.2, 0.3, 0.4, 0.5], [0.05, 0.5, 0.95]    
    i=0
    aggregate_metrics = dict()
    for epsilon in epsilons:
        for gamma in gammas:
            for pm in pms:
                respath = f'../res/'
                name = f'e{epsilon}_g{gamma}_pm{pm}_mo{media_op}'
                final_opinions, final_niter = read_dicts(respath, name, max_iterations)
                
                metrics = am.aggregateMetrics(final_opinions, final_niter)
                metrics.compute_metrics()
                
                aggregate_metrics[i] = {
                        'epsilon': epsilon,
                        'gamma': gamma,
                        'pm': pm,
                        'media_op': media_op,
                        'avg_nc': metrics.get_avg_nc(),
                        'avg_entr': metrics.get_avg_entr(),
                        'avg_pwdist': metrics.get_avg_pwdist(),
                        'avg_op': metrics.get_avg_opinion(),
                        'avg_nit': metrics.get_avg_nit
                    }
                i+=1

    with open(f'../aggregate/aggregate_metrics_{name}.json', 'w') as ofile:
        print('writing aggregate')
        json.dump(aggregate_metrics, ofile)
    
    try:
        with open(f'../aggregate/aggregate_metrics_{name}.json', 'r') as ifile:
            aggregate_metrics = json.load(ifile)
    except FileNotFoundError:
        print('file not correctly written')
        exit


