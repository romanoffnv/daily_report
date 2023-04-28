import os
import sys
# Global imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from __init__ import *
from Settings import *


class Crews:
    crews = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 16, 17, 18, 19, 22, 31, 32]

class ShiftExtractor(Crews):
    def __init__(self, df):
        self.df = df
    
    def get_indeces(self):
        indeces = []
        for num in self.crews:
            for index, value in self.df.iloc[:, 0].items():
                if value == f"ГНКТ № {num}" or value == f"ГНКТ №{num}":
                    for i, row in self.df.iloc[index:].iterrows():
                        if row.str.contains("Видеофиксация", regex=True).any():
                            indeces.append(i)
                            break
        return indeces
        
    def extract_shifts(self, indeces, col_index):
        L = []
        for i in indeces:
            # Iterate over rows starting from the specified index and the column of interest
            last_index = None
            last_value = None

            for i, value in self.df.iloc[:i, col_index].items():
                # Check if the value is non-NaN
                if not pd.isna(value):
                    # If a non-NaN value is found, store the index and the value
                    last_index = i
                    last_value = value

            # Print the last non-NaN value (if any)
            if last_index is not None:
                L.append(last_value)
            else:
                print("No non-NaN values found in the column.")
        return L

    def extract_all_shifts(self):
        indeces = self.get_indeces()
        L_shift1 = self.extract_shifts(indeces, 8)
        L_shift2 = self.extract_shifts(indeces, 9)
        return L_shift1, L_shift2 
    
    def clean_all_shifts(self):
        L_shift1, L_shift2 = self.extract_all_shifts()
        L_shift1 = [str(x).strip() for x in L_shift1]
        L_shift2 = [str(x).strip() for x in L_shift2]
        return L_shift1, L_shift2

class ObjectiveExtractor(Crews):
    def __init__(self, df):
        self.df = df
    
    def get_indeces(self):
        indeces = []
        for num in self.crews:
            for index, value in self.df.iloc[:, 0].items():
                if value == f"ГНКТ № {num}" or value == f"ГНКТ №{num}":
                    indeces.append(index)
                    break
        return indeces
    
    def extract_objectives(self, col_index):
        L_indeces = self.get_indeces()
        L = []
        for i in L_indeces:
            L.append(self.df.iloc[i + 1, col_index])
        return L

class DataExtractor(Crews):
        def __init__(self, df):
            self.df = df
        def get_indeces(self):
            indeces = []
            for num in self.crews:
                for index, value in self.df.iloc[:, 0].items():
                    if value == f"ГНКТ № {num}" or value == f"ГНКТ №{num}":
                        indeces.append(index)
                        break
            return indeces
        def extract_data(self, col_index, offset):
            L_indeces = self.get_indeces()
            L = []
            for i in L_indeces:
                L.append(self.df.iloc[i + offset, col_index])
            L = [str(x).strip() for x in L]
            return L


import re

class ListDecomposer:
    def __init__(self, L_crew_head_tp1_tp2_mech, nt_nka_uga_mac_auxtrucks, df):
        self.L_crew_head_tp1_tp2_mech = L_crew_head_tp1_tp2_mech
        self.nt_nka_uga_mac_auxtrucks = nt_nka_uga_mac_auxtrucks
        self.df = df
        
    def decomp_col(self, reg, L_target):
        L = [i if re.findall(reg, str(i)) else None for i in L_target]
        return L[1:]
    
    def decomp_lists(self):
        L_crew = self.decomp_col('\ГНКТ №\s*\d+', self.L_crew_head_tp1_tp2_mech)
        L_head = self.decomp_col('Руководитель проекта', self.L_crew_head_tp1_tp2_mech)
        L_tp1 = self.decomp_col('Мастер 1', self.L_crew_head_tp1_tp2_mech)
        L_tp2 = self.decomp_col('Мастер 2', self.L_crew_head_tp1_tp2_mech) 
        L_mech = self.decomp_col('Механик', self.L_crew_head_tp1_tp2_mech) 

        L_temperature = self.df.iloc[:, 1].tolist()
        L_pad = self.df.iloc[1:, 2].tolist()
        L_well = self.df.iloc[1:, 3].tolist()
        L_field = self.df.iloc[1:, 4].tolist()

        L_nt = self.decomp_col('(НТ)|(МЗКТ)', self.nt_nka_uga_mac_auxtrucks)
        L_nka = self.decomp_col('НКА', self.nt_nka_uga_mac_auxtrucks)
        L_uga = self.decomp_col('УГА', self.nt_nka_uga_mac_auxtrucks)
        L_mac = self.decomp_col('(ПКА)|(МАК)', self.nt_nka_uga_mac_auxtrucks)
        
        return L_crew, L_head, L_tp1, L_tp2, L_mech, L_temperature, L_pad, L_well, L_field, L_nt, L_nka, L_uga, L_mac
