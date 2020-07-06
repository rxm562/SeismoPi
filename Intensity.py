# Intensity Calculator

# Import Libraries
import numpy as np
from scipy.spatial import distance

#Intensity Calculation Model
class Intensity (object):
    def __init__(self, ex, ey, M):
        self.ex = ex  # Long of Epicenter
        self.ey = ey  # Lat of Epicenter
        self.M=M      # EQ Magnitude
    def intensity_node(data,ex,ey,M):
        d = []        # Distance from Epicenter to node
        PGA = []      # Peak Ground Acceleration
        PGV = []      # Peak Ground Velocity
        pos = {}
        for index, row in data.iterrows():
            x = row['x'] # long of site
            y = row['y'] # lat of site
            D = distance.euclidean((ex,ey), (x,y))/1000                      #Distance from Epicenter to node
            A = (403.8*np.power(10, 0.265*M)*np.power(D+30, -1.218))/981     # Attenuation Model for PGA (g)
            V = (np.power(10, -0.848 + 0.775*M + -1.834*np.log10(D+17)))/100  # Attenuation Model for PGV (m/s)
            d.append(D)
            PGA.append(A)
            PGV.append(V)
            pos[int(row['id'])]=(x,y)
        d = np.array(d)
        PGA = np.array(PGA)
        PGV = np.array(PGV)
        return d, PGA, PGV, pos

    def intensity_link(link,node,ex,ey,M):
        PGA = []
        PGV = []
        for index, row in link.iterrows():
            start_node = row['start_node'] # Start node for link
            end_node = row['end_node']     # End node for link
            start_x, start_y = node.loc[node['id']==start_node, ['x','y']].values[0]
            end_x, end_y = node.loc[node['id']==end_node, ['x','y']].values[0]
            D_start = distance.euclidean((ex,ey), (start_x,start_y))/1000
            A_start = (403.8*np.power(10, 0.265*M)*np.power(D_start+30, -1.218))/980
            V_start = (np.power(10, -0.848 + 0.775*M + -1.834*np.log10(D_start+17)))/100
            D_end = distance.euclidean((ex,ey), (end_x,end_y))/1000
            A_end = 403.8*np.power(10, 0.265*M)*np.power(D_end+30, -1.218)/980
            V_end = (np.power(10, -0.848 + 0.775*M + -1.834*np.log10(D_end+17)))/100
            PGA.append((A_start+A_end)/2)
            PGV.append((V_start+V_end)/2)
        return PGA, PGV


# Attenuation Equations provided by Kawashima et al. (1984) and Yu and Jin (2008) are used for intensity estimation at site
