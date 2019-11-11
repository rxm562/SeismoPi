"""
This file to estimate distances between various points
"""

import numpy as np
import pandas as pd
from scipy.spatial import distance
import matplotlib.pyplot as plt
import networkx as nx

class Distance:
    # Constructor
    def __init__(self, ex, ey, M):
        self.ex = ex  # Create an instance variable
        self.ey = ey
        self.M=Mag
    def com_pga_dist(data,ex,ey,Mag):
        r = []
        PGA = []
        PGV = []
        pos = {}
        for index, row in data.iterrows():
            x = row['x']
            y = row['y']
            dist = distance.euclidean((ex,ey), (x,y))/1000
            P = (403.8*np.power(10, 0.265*Mag)*np.power(dist+30, -1.218))/981
            V = (np.power(10, -0.848 + 0.775*Mag + -1.834*np.log10(dist+17)))/100
            r.append(dist)
            PGA.append(P)
            PGV.append(V)
            pos[int(row['id'])]=(x,y)
        r = np.array(r)
        PGA = np.array(PGA)
        PGV = np.array(PGV)
        return r, PGA, PGV, pos

    def pga_for_link(link,node,ex,ey,Mag):
        r = []
        PGA = []
        PGV = []
        for index, row in link.iterrows():
            start_node = row['start_node']
            end_node = row['end_node']
            start_x, start_y = node.loc[node['id']==start_node, ['x','y']].values[0]
            end_x, end_y = node.loc[node['id']==end_node, ['x','y']].values[0]
            dist_start = distance.euclidean((ex,ey), (start_x,start_y))/1000
            P_start = (403.8*np.power(10, 0.265*Mag)*np.power(dist_start+30, -1.218))/980
            V_start = (np.power(10, -0.848 + 0.775*Mag + -1.834*np.log10(dist_start+17)))/100
            dist_end = distance.euclidean((ex,ey), (end_x,end_y))/1000
            P_end = 403.8*np.power(10, 0.265*Mag)*np.power(dist_end+30, -1.218)/980
            V_end = (np.power(10, -0.848 + 0.775*Mag + -1.834*np.log10(dist_end+17)))/100
            PGA.append((P_start+P_end)/2)
            PGV.append((V_start+V_end)/2)
        return PGA, PGV
