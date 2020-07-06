"""
This file to define Estimate various parameters
"""

import numpy as np
import pandas as pd
from scipy.spatial import distance
import matplotlib.pyplot as plt
import networkx as nx
from pyproj import Proj
from pyproj import Proj, transform


# trasforming latlong into mercetor coordinates
def tran(data):    
    utmxy = {}
    rx=[]
    ry=[]
    for index, row in data.iterrows():
        x = row['x']
        y = row['y']
        inProj = Proj(init='epsg:4326')
        outProj = Proj(init='epsg:3395')
        cz = transform(inProj,outProj,x,y)
        r1=cz[0]
        r2=cz[1]
        rx.append(r1)
        ry.append(r2)
    rx=np.array(rx)
    ry=np.array(ry)
    return rx,ry


# data1 and data2 should be node and link, respectively
def Length(data1,data2):  
    dist=[]
    for index, row in data2.iterrows():
        sp=data1[data1.id==row['start_node']]
        start_x, start_y = (list(sp.x),list(sp.y))
        ep=data1[data1.id==row['end_node']]
        end_x,end_y=(list(ep.x),list(ep.y))
        lal = distance.euclidean((start_x, start_y),(end_x,end_y))
        dist.append(lal)
    dist=np.array(dist)
    return dist


# data1 and data2 should be node and link, respectively
def C_Check(data):  
    maint=[]
    for index,row in data.iterrows():
        if (row['ind']>=0.5) & (row['dl']>0):
            mm=2
        elif (row['ind']<0.5) & (row['dl']>0):
            mm=1
        else:
            mm=0
        maint.append(mm)
    maint=np.array(maint)
    return maint


def C_Est(data):  
    cost=[]
    for index,row in data.iterrows():
        if (row['MA']==1):
            mm=row['repair_C']*row['nNoB']
        elif (row['MA']==2):
            mm=row['replace_C']
        else:
            mm=0
        cost.append(mm)
    cost=np.array(cost)
    return cost

def T_cost(data,pipe_cost=None):
    """ 
    """
    nrpr = []
    nrpl = []

    network_cost = 0
        
    if pipe_cost is None:
        diameter = [4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 30, 32, 34, 36] # inch
        rpl = [600, 630, 675, 750, 825, 1200, 1950, 2400, 2700, 3450, 4350, 4650, 5250, 5700, 6300] # replace cost/m
        rpr = [400, 420, 450, 500, 550, 800, 1300, 1600, 1800, 2300, 2900, 3100, 3500, 3800, 4200] # repair cost
        
#         diameter = np.array(diameter)*0.0254 # m
        repair_cost = pd.Series(rpr,diameter)        
        replace_cost = pd.Series(rpl,diameter)        

    # Pipe construction cost
    for index, row in data.iterrows():
        dia = row['dia']
        length=row['link_m']
        idxrpr = np.argmin([np.abs(repair_cost.index - dia)])
        idxrpl = np.argmin([np.abs(replace_cost.index - dia)])
        #print(link_name, pipe_cost.iloc[idx], link.length)
        repair_C = network_cost + repair_cost.iloc[idxrpr]
        replace_C = network_cost + replace_cost.iloc[idxrpl]*length
        nrpr.append(repair_C)
        nrpl.append(replace_C)
    nrpr = np.array(nrpr)
    nrpl = np.array(nrpl)

        
    return nrpr,nrpl
