import os.path
import sqlite3
import pandas as pd

class DataBase:
        def __init__(self, db_name):
            self.db_name = db_name
            self.conn, self.cursor = self.db_connect()
        
        def db_connect(self):
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            return conn, cursor

        def db_post(self, df, table_name, close=True, if_exists = 'replace'):
            df.to_sql(name=table_name, con=self.conn, if_exists=if_exists, index=False)
            self.conn.commit()
            if close:
                self.conn.close()
        
        def db_get(self, table_name, close=True):
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
            if close:
                self.conn.close()
            return df

# db = DataBase('db_cits_ct.db')
# db.db_post(df_all, 'Experimental', close=False)
# df = db.db_get('Experimental', close=True)

def set_pandas_options(df, width, colwidth, colmap):
    # Pandas
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', width)
    pd.set_option('display.max_colwidth', colwidth)
    # cmd view control
    if colmap:
        df.columns = df.columns.map(str)
        df.rename(columns=lambda x: x[:10] if len(x) > 20 else x, inplace=True)

# pprint(df, set_pandas_options(df, width=1000, colwidth=30, colmap = False))
