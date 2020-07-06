# ALA (2001) Correction Modified Calculator
import pandas as pd


# calculator
def Correction_Modifiers(pipe_info, Mat_type=None, Soil_type=None, Age=None):
    pipe_info = pd.DataFrame(data = pipe_info.values, columns =pipe_info.columns, index = pipe_info.index.astype('str')) # Pipe characteristics, strings
                  
    if Mat_type is None:
        k1_wei = {'AC': 1.0, 'CI': 1.0, 'DI': 0.5, 'PVC': 0.5, 'STL': 0.7, 'RCCP': 0.2}
        
    def corrosion_factor(arrlike):
        Age = arrlike['Age']
        Soil_type = arrlike['Soil_type']
        Mat_type = arrlike['Mat_type']
        if Mat_type == 'CI':
            if Soil_type == 'H':
                if Age < 1920:
                    corrosion_rate = 3.0
                elif Age < 1960:
                    corrosion_rate = -0.05*Age+99
                else:
                    corrosion_rate = 1.0
            elif Soil_type == 'M':
                if Age < 1920:
                    corrosion_rate = 2.0
                elif Age < 1960:
                    corrosion_rate = -0.025*Age+50
                else:
                    corrosion_rate = 1.0
            elif Soil_type == 'L':
                corrosion_rate = 1.0
            else:
                print('Soil Type Index Wrong')

        elif Mat_type == 'DI':
            corrosion_rate = 1.5
        else:
            corrosion_rate = 1.0
            
        return corrosion_rate
        
    k1 = pipe_info['Mat_type'].map(k1_wei)            # Modifier for material type
    k2 = pipe_info.apply(corrosion_factor,axis = 1)   # Modifier for corrosion
    C = k1*k2

    return C
