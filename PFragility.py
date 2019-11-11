"""
This file to define Fragility Curves
"""

import numpy as np
import pandas as pd
from scipy.spatial import distance
import matplotlib.pyplot as plt
import networkx as nx

class FragilityCurve(object):
    """
   Fragility Curve class.
    """

    def __init__(self):
        self._num_states = 0
        self._states = {}

    def add_state(self, name, priority=0, distribution={}):
        """
        Add a damage state distribution
        
        Parameters
        ----------
        name : string
            Name of the damage state
        
        priority : int
            Damage state priority
        
        distribution : dict, key = string, value = scipy.stats statistical function
            'Default' can be used to specificy all location
        """
        state = State(name, priority, distribution)
        self._states[name] = state
        self._num_states += 1
    
    def states(self):
        """
        A generator to iterate over all states, in order of priority
        Returns
        -------
        state_name, state
        """
        sorted_list = [x for x in self._states.items()] 
        sorted_list.sort(key=lambda x: x[1].priority) 
        
        for state_name, state in sorted_list:
            yield state_name, state
    
    def get_priority_map(self):
        """
        Returns a dictonary of state name and priority number.
        """
        priority_map = {None: 0}
        
        for state_name, state in self.states():
            priority_map[state_name] = state.priority
            
        return priority_map
        
    def cdf_probability(self, x):
        """
        Return the CDF probability for each state, based on the value of x
        
        Parameters
        -----------
        x : pd.Series
            Control variable for each element
            
        Returns
        --------
        Pr : pd.Dataframe
            Probability of exceeding a damage state
        
        """
        state_names = [name for name, state in self.states()]
        
        Pr = pd.DataFrame(index = x.index, columns=state_names)

        for element in Pr.index:
            for state_name, state in self.states():
                try:
                    dist=state.distribution[element]
                except:
                    dist=state.distribution['Default']
                Pr.loc[element, state_name] = dist.cdf(x[element])
            
        return Pr
    
    def sample_damage_state(self, Pr):
        """
        Sample the damage state using a uniform random variable
        
         Parameters
        -----------
        Pr : pd.Dataframe
            Probability of exceeding a damage state
            
        Returns
        -------
        damage_state : pd.Series
            The damage state of each element
        """
        p = pd.Series(data = np.random.uniform(size=Pr.shape[0]), index=Pr.index)
        
        damage_state = pd.Series(data=[None]* Pr.shape[0], index=Pr.index)
        
        for DS_names in Pr.columns:
            damage_state[p < Pr[DS_names]] = DS_names
        
        return damage_state
        
class State(object):

    def __init__(self, name, priority=0.0, distribution={}):
        """
        Parameters
        -----------
        name : string
            Name of the damage state
            
        priority : int
            
        distribution : dict
        """
        self.name = name
        self.priority = priority
        self.distribution = distribution


def plot_fragility_curve(FC, fill=True, key='Default',
                         title='Fragility curve', 
                         xmin=0, xmax=250, npoints=100, 
                         xlabel='x', 
                         ylabel='Prob. of exceedance',
                         figsize=[10,6]):
    """
    Plot fragility curve.
    
    Parameters
    -----------
    FC : FragilityCurve object
        Fragility curve
    
    fill : bool (optional)
        If true, fill area under the curve (default = True)
    
    key : string (optional)
        Fragility curve state distribution key (default = 'Default')
    
    title : string (optional)
        Plot title
    
    xmin : float (optional)
        X axis minimum (default = 0)
    
    xmax : float (optional)
        X axis maximum (default = 1)
    
    npoints : int (optional)
        Number of points (default = 100)
    
    xlabel : string (optional)
        X axis label (default = 'x')
    
    ylabel : string (optional)
        Y axis label (default = 'Probability of exceedance')
    
    figsize : list (optional)
        Figure size (default = [10,5])
"""
    if plt is None:
        raise ImportError('matplotlib is required')
    
    plt.figure(figsize=tuple(figsize))
    plt.title(title)
    x = np.linspace(xmin,xmax,npoints)
    for name, state in FC.states():
        try:
            dist=state.distribution[key]
            if fill:
                plt.fill_between(x,dist.cdf(x), label=name)
            else:
                plt.plot(x,dist.cdf(x), label=name)
        except:
            pass        
    plt.xlim((xmin,xmax))
    plt.ylim((0,1))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()

