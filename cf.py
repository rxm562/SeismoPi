"""
This file to for correction factor
"""

import numpy as np
import pandas as pd
from scipy.spatial import distance
import matplotlib.pyplot as plt
import networkx as nx

def correction_factor(pipe_characteristics, M_type=None, soil_type=None, age=None):

    # Make sure the values are strings
    pipe_characteristics = pd.DataFrame(data = pipe_characteristics.values, columns =pipe_characteristics.columns, index = pipe_characteristics.index.astype('str'))
                  
    if M_type is None:
        k3_weight = {'AC': 1.0, 'CI': 1.0, 'DI': 0.5, 'PVC': 0.5, 'STL': 0.7, 'RCCP': 0.2}

    if M_type is None:
        k2_weight = {'AC': 1.0, 'CI': 1.0, 'DI': 1.5, 'PVC': 1.0, 'STL': 1.0, 'RCCP': 1.0}
        
    def find_corrosion(arrlike):
        age = arrlike['age']
        soil_type = arrlike['soil_type']
        M_type = arrlike['M_type']
        if M_type == 'CI':
            if soil_type == 'H':
                if age < 1920:
                    corrosion_rate = 3.0
                elif age<1960:
                    corrosion_rate = -0.05*age+99
                else:
                    corrosion_rate = 1.0
            elif soil_type == 'M':
                if age < 1920:
                    corrosion_rate = 2.0
                elif age<1960:
                    corrosion_rate = -0.025*age+50
                else:
                    corrosion_rate = 1.0
            elif soil_type == 'L':
                corrosion_rate = 1.0
            else:
                print('Soil Type Index Wrong')

        elif M_type == 'DI':
            corrosion_rate = 1.5
        else:
            corrosion_rate = 1.0
            
        return corrosion_rate
        
    C0 = pipe_characteristics['M_type'].map(k3_weight)
    C1 = pipe_characteristics['M_type'].map(k2_weight)
    C2 = pipe_characteristics.apply(find_corrosion,axis = 1)
    C = C0*C2

    return C
