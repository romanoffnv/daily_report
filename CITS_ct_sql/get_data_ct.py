import os
import sys

# Global imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..'))
sys.path.append(parent_dir)
from __init__ import *
from Settings import *
from extract_data import *


def main(df):
    
    warnings.filterwarnings("ignore") 
    df = df.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 14]]
    # Get the last column name
    last_col_name = df.columns[-1]
    # Replace the substring in column names
    
    df.loc[:, last_col_name] = np.nan
    # Set the first row's value to be the last column name
    df.iloc[0, -1] = last_col_name


    # Forward fill the value throughout the entire last column
    df[last_col_name] = df[last_col_name].fillna(method='ffill')

    
    # 28.02.2023г to 28.02.2023
    for index, row in df.iterrows():
        last_col_value = row[last_col_name]
        last_col_value = last_col_value.replace('г', '')
        df.at[index, last_col_name] = last_col_value
    
    
    
    shift_extractor = ShiftExtractor(df)  
    L = shift_extractor.clean_all_shifts()
    L_shift1 = L[0]
    L_shift2 = L[1]
    
    
    # Pulling needed cols, converting them into lists
    cols = [0, 1, 2, 3, 4, 5, 6, 10]
    data_lists = [df.iloc[:, i].tolist() for i in cols]
    
    L_crew_head_tp1_tp2_mech, L_temperature, L_pad, L_well, L_field, nt_nka_uga_mac_auxtrucks, L_objective, L_date = data_lists
    
    
    ldcmp = ListDecomposer(L_crew_head_tp1_tp2_mech, nt_nka_uga_mac_auxtrucks, df)  
    L_crew, L_head, L_tp1, L_tp2, L_mech, L_temperature, L_pad, L_well, L_field, L_nt, L_nka, L_uga, L_mac = ldcmp.decomp_lists()

         
    # Extracting objectives from imported class
    # 1. Making df1 with L_objective
    df1 = pd.DataFrame(zip(L_crew, L_head, L_tp1, L_tp2, L_mech, L_temperature, L_pad, L_well, L_field, L_nt, L_nka, L_uga, L_mac, L_objective, L_date))
    # 2. Initiating ObjectiveExtractor class by sending df1
    obext = ObjectiveExtractor(df1)
    # 3. Assigning the class return to L_objective by sending col by index
    L_objective = obext.extract_objectives(13)
    
    
    # Cleaning L_mac list by extracting mac or pka entries only with the keyword 'Маш-т'
    L_mac = [x if 'Маш-т' in str(x) else None for x in L_mac ]
    df = pd.DataFrame(zip(L_crew, L_mac))
    # Cleaning primary df of nones
    
   
    # Picking relative entries from gen table's logical crew squares by setting offests relative to the crew
    dext = DataExtractor(df1)
    indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    offsets = [0, 1, 3, 5, 7, 10, 0, 0, 0, 7, 9, 11, 11]
    L = [dext.extract_data(i, offset) for i, offset in zip(indices, offsets)]
    L_crew, L_head, L_tp1, L_tp2, L_mech, L_temperature, L_pad, L_well, L_field, L_nt, L_nka, L_uga, L_mac = L

    
    # Making ultimate database
    df1 = pd.DataFrame(zip(L_crew, L_head, L_tp1, L_tp2, L_mech, L_temperature, L_pad, 
                           L_well, L_field, L_nt, L_nka, L_uga, L_mac, L_objective, L_shift1, L_shift2, L_date), 
                           columns=['Crew', 'Head', 'tp_1', 'tp_2', 'mech', 'temp', 'pad', 'well', 'field', 'truck_1', 
                                    'truck_2', 'truck_3', 'truck_4', 'objective', 'shift_1', 'shift_2', 'date'])
    df = df1
    L_cols = ['truck_1', 'truck_2', 'truck_3', 'truck_4']
    for i in L_cols:
        df[i] = df[i].str.replace('Маш-т', '')
    
    # Rearrange cols
    cols = df.columns.tolist()
    cols = ['date', 'Crew', 'Head', 'tp_1', 'tp_2', 'mech', 'temp', 'pad', 'well', 'field', 'truck_1', 
            'truck_2', 'truck_3', 'truck_4', 'objective', 'shift_1', 'shift_2']
    df = df[cols]
    warnings.resetwarnings()
    return df


    
if __name__ == '__main__':
    start_time = time.time()
    try:
        main()
    except UnicodeEncodeError as e:
        print("UnicodeEncodeError: ignoring characters that cannot be encoded")
    print("--- %s seconds ---" % (time.time() - start_time))
