# Mass Media Impact on Opinion Evolution in Biased Digital Environments: a Bounded Confidence Model
Valentina Pansanella, Alina Sirbu, Janos Kertesz, Giulio Rossetti
valentina.pansanella@sns.it

## Abstract
People increasingly shape their opinions by accessing and discussing content shared on social networking websites. These platforms contain a mixture of other users' shared opinions and content from mainstream media sources. While online social networks have fostered information access and diffusion, they also represent optimal environments for the proliferation of polluted information and contents, which are argued to be among the co-causes of polarization/radicalization phenomena. 
Moreover, recommendation algorithms - intended to enhance platform usage - likely augment such phenomena, generating the so-called _Algorithmic Bias_. 
In this work, we study the effects of the combination of social influence and mass media influence on the dynamics of opinion evolution in a biased online environment, using a recent bounded confidence opinion dynamics model with algorithmic bias (Sirbu et al., 2019) as a baseline and adding the possibility to interact with one or more media outlets, modeled as stubborn agents. 
![example](https://github.com/ValentinaPansanella/AlgBiasMediaModel/assets/56345821/c6cf995f-6898-477b-b0b9-1b0a7dff0db8)
We analyzed four different media landscapes and found that an open-minded population is more easily manipulated by external propaganda - moderate or extremist - while remaining undecided in a more balanced information environment. 
By reinforcing users' biases, recommender systems appear to help avoid the complete manipulation of the population by external propaganda. 

After installig NDlib Python Library
```
pip install ndlib
```
In the ```code``` folder you can find ```simulation_example.ipynb``` with the pipeline to reproduce this work. 

You need to **create a graph representing your simulation population**
```python
graph = nx.complete_graph(250)
```

**Set up model parameters**
```python
mu = 0.5
epsilon = 0.3
gamma = 1.0
gamma_media = gamma
pm = 0.5
k = 3
media_op = [0.05, 0.5, 0.95]
```

**Set up simulation parameters**
```python
max_iterations = 1000
sensibility = 0.00001
nsteady = 1000
nodeStatus = True
progressBar = True
drop_evolution = False
```

**Create model**
```python
model = op.AlgorithmicBiasMediaModel(graph)
```

**Create configuration**
```python
config = mc.Configuration()
config.add_model_parameter("mu", mu)
config.add_model_parameter("epsilon", epsilon)
config.add_model_parameter("gamma", gamma)
config.add_model_parameter("gamma_media", gamma)
config.add_model_parameter("p", pm)
config.add_model_parameter("k", k)
```

**Configure model**
```python
model.set_initial_status(config)
model.set_media_opinions(media_op)
```

**Perform iterations untill convergence (if possible)**
```python
iterations = model.steady_state(max_iterations=max_iterations, nsteady=nsteady, sensibility=sensibility, node_status=nodeStatus, progress_bar=progressBar, drop_evolution=False)
```





