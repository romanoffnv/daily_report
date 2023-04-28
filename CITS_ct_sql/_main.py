import os
import sys
import glob
import pandas as pd
from pprint import pprint
import time

# Global imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..'))
sys.path.append(parent_dir)
from __init__ import *
from Settings import *
from get_data_ct import main as get_data_ct


def main():
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    programm_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\CITS_ct_sql'))
    
    
    def open_file(file_name):
        
        # Find all files in the directory that match the search string
        search_string = file_name
        files = glob.glob(os.path.join(os.path.join(src_dir, search_string)))
        
        
        # Check if any files are found
        if len(files) == 0:
            print('No file found matching the search string')
            return pd.DataFrame()  # Return an empty DataFrame

        # Loop through all files
        for file in files:
             # Read the last sheet in the Excel file into a DataFrame
            df = pd.read_excel(file, sheet_name=-1)
            df = get_data_ct(df)

     
    # List of file names to process
    file_names = ['1. СВОДКА СЛУЖБЫ ГНКТ ООО ПАКЕР СЕРВИС*.xls*']

    for file_name in file_names:
        df = open_file(file_name)
        # Append the current DataFrame to the df_all DataFrame
        df_all = pd.concat([df_all, df], ignore_index=True)
    
    
    db = DataBase('db_cits_ct.db')
    db.db_post(df_all, 'Experimental', close=True)
    # df = db.db_get('Experimental', close=True)
    # pprint(df)
    
   
if __name__ == '__main__':
    start_time = time.time()
    try:
        main()
    except UnicodeEncodeError as e:
        print(e)
    end_time = time.time
