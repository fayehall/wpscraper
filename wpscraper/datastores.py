import os
from os.path import isfile
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd

"""
CSVDataStore
"""
class CSVDataStore:
    def __init__(self, filename):
        self.filename = filename
        
    def clean(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)

    def read(self):
        if self.filename:
            try:
                with open(self.filename, 'r') as f:
                    try:
                        df = pd.read_csv(self.filename)
                    except pd.errors.EmptyDataError:
                        pass
                    else:
                        return df
            except FileNotFoundError:
                pass
            
        return pd.DataFrame()

    def save(self, df):
        if isinstance(df, pd.DataFrame) and not df.empty:
            if isfile(self.filename):
                mode = 'a'
                writeHeader = False
            else:
                mode = 'w'
                writeHeader = True

            with open(self.filename, mode) as f:
                df.to_csv(f,header=writeHeader,index=False)


"""
SqliteDataStore
"""
class SqliteDataStore:
    def __init__(self, db_name, table_name):
        self.db_name = db_name
        self.table_name = table_name
        
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        sql = 'CREATE TABLE IF NOT EXISTS ' + self.table_name + ' (id INT, author INT, author_name TEXT, date TEXT, title TEXT, link TEXT, content TEXT)'
        cursor.execute(sql)
        connection.commit()
        connection.close()
        
    def clean(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        sql = 'DROP TABLE IF EXISTS ' + self.table_name
        cursor.execute(sql)
        connection.commit()
        connection.close()
        os.remove(self.db_name)
        
    
    def read(self):
        engine = sqlalchemy.create_engine('sqlite:///' + self.db_name, echo=False)
        try:
            df = pd.read_sql(self.table_name, con=engine)
        except sqlalchemy.exc.OperationalError:
            df = pd.DataFrame()
        finally:
            return df
            
        
    def save(self, df):
        if isinstance(df, pd.DataFrame) and not df.empty:
            engine = sqlalchemy.create_engine('sqlite:///' + self.db_name, echo=False)
            df.to_sql(self.table_name, con=engine, if_exists='append',index=False)

            connection = sqlite3.connect(self.db_name)
            connection.commit()
            connection.close()

        