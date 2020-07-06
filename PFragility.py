# Defining Fragility Curves

import numpy as np
import pandas as pd
from scipy.spatial import distance
import matplotlib.pyplot as plt
import networkx as nx

class Fragility(object):

    def __init__(self):
        self._no_dam_state = 0
        self._dam_states = {}

    def add_dam_state(self, name, level=0, dist={}):
        dam_state = DState(name, level, dist)
        self._dam_states[name] = dam_state
        self._no_dam_state += 1
    
    def states(self):
        sorted_list = [x for x in self._dam_states.items()] 
        sorted_list.sort(key=lambda x: x[1].level) 
        
        for state_name, dam_state in sorted_list:
            yield state_name, dam_state
    
    def get_level_map(self):
        level_map = {None: 0}
        
        for state_name, dam_state in self.states():
            level_map[state_name] = dam_state.level
            
        return level_map
        
    def cdf_probability(self, x):
        state_names = [name for name, dam_state in self.states()]
        Pr = pd.DataFrame(index = x.index, columns=state_names)

        for element in Pr.index:
            for state_name, dam_state in self.states():
                try:
                    dist=dam_state.dist[element]
                except:
                    dist=dam_state.dist['Default']
                Pr.loc[element, state_name] = dist.cdf(x[element])
            
        return Pr
    
    def sample_damage_state(self, Pr):
        p = pd.Series(data = np.random.uniform(size=Pr.shape[0]), index=Pr.index)
        
        damage_state = pd.Series(data=[None]* Pr.shape[0], index=Pr.index)
        
        for DS_names in Pr.columns:
            damage_state[p < Pr[DS_names]] = DS_names
        
        return damage_state
        
class DState(object):

    def __init__(self, name, level=0.0, dist={}):
        self.name = name
        self.level = level
        self.dist = dist


def plot_FC(FP, fill=True, key='Default', title='Fragility curve', npoints=100, xlabel='x', ylabel='Prob. of Exceedance', figsize=[10,6], xmin=0, xmax=100):

    if plt is None:
        raise ImportError('matplotlib is missing!')
    plt.figure(figsize=tuple(figsize))
    plt.title(title)
    plt.xlim((xmin,xmax))
    x = np.linspace(xmin,xmax,npoints)
    for name, dam_state in FP.states():
        try:
            dist=dam_state.dist[key]
            if fill:
                plt.fill_between(x,dist.cdf(x), label=name)
            else:
                plt.plot(x,dist.cdf(x), label=name)
        except:
            pass        

    plt.ylim((0,1))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
