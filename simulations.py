from utils import *
from aggregate import *
from plots import *
import sys

# Model settings

def simulations(max_iterations, nruns):
        k = 3
        epsilons, gammas, pms, media_op = [0.2, 0.3, 0.4, 0.5], [0.0, 0.5, 1.0, 1.5], [0.0, 0.1, 0.2, 0.3, 0.4, 0.5], [0.05, 0.5, 0.95]
        #perform multiple runs and average results
        graph = nx.complete_graph(100)
        for epsilon in epsilons:
            for gamma in gammas:
                for pm in pms:
                    respath = f'../res/'
                    name = f'e{epsilon}_g{gamma}_pm{pm}_mo{media_op}'
                    final_opinions, final_niter = read_dicts(respath, name, max_iterations)
                    
                    for run in range(nruns):
                        if str(run) in final_opinions.keys() and str(run) in final_niter.keys(): 
                            print('run already present. skipping.')
                            run += 1
                        else:
                            print(f'run {run} epsilon = {epsilon} gamma = {gamma} pm = {pm} media_op = {media_op}')    
   
                            #create model
                            model = op.AlgorithmicBiasMediaModel(graph)

                            #create configuration
                            config = mc.Configuration()
                            config.add_model_parameter("epsilon", epsilon)
                            config.add_model_parameter("gamma", gamma)
                            config.add_model_parameter("gamma_media", gamma)
                            config.add_model_parameter("p", pm)
                            config.add_model_parameter("k", k)

                            #configure model
                            model.set_initial_status(config)
                            model.set_media_opinions(media_op)

                            #perform iterations untill convergence
                            iterations = model.steady_state(max_iterations=1000000, nsteady=1000, sensibility=0.00001, node_status=True, progress_bar=True)

                            finalopinions = iterations[-1]['status']
                            niter = int(iterations[-1]['iteration'])
                            
                            final_opinions[run] = finalopinions
                            final_niter[run] = niter
                            
                            write_dicts(respath, name, max_iterations, final_opinions, final_niter)

                            plotevolution(iterations, name=name, run=run)
                            plotdistribution(list(finalopinions.values()), name=name, run=run)


def main():
    max_iterations, nruns = int(sys.argv[1]), int(sys.argv[2])
    simulations(max_iterations, nruns)
    aggregate(max_iterations)

if __name__ == '__main__':
    main()
