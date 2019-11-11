"""
This file to define Fragility Curves
"""

import numpy as np
import pandas as pd
from scipy.spatial import distance
import matplotlib.pyplot as plt
import networkx as nx

def plot_fragility_curve(FC, fill=True, key='Default', 
                         title='', xmin=0, xmax=250, npoints=100, 
                         xlabel='x', 
                         ylabel='Probability of exceedance',
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

