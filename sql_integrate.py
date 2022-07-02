import os
import pandas as pd
from mysql.connector import Error
import mysql.connector as cu

class CausalSql():
    
    def __init__(self):
        pass
        
    def DBConnect(self, dbName=None):
        """
        A function to connect to SQL database
        """
        mydb = cu.connect(host='localhost', user='root',
                          password='Selam@0102.',
                             database=dbName, buffered=True)
        cursor = mydb.cursor()
        return mydb, cursor


    def createDB(self, dbName: str) -> None:
        """
        A function to create SQL database
        """
        mydb, cursor = DBConnect()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbName};")
        mydb.commit()
        cursor.close()

    def createTables(self, dbName: str) -> None:
        """
        A function to create SQL table
        """
        mydb, cursor = DBConnect(dbName)
        sqlFile = 'schema.sql'
        fd = open(sqlFile, 'r')
        readsqlFile = fd.read()
        fd.close()
        sqlCommands = readsqlFile.split(';')
        for command in sqlCommands:
            try:
                result = cursor.execute(command)
            except Exception as e:
                print('command skipped: ', command)
                print(e)
        mydb.commit()
        cursor.close()

    def insert_into_causality(self, dbName: str, df: pd.DataFrame, table_name: str) -> None:
        """
        A function to insert values in SQL table
        """
        mydb, cursor = DBConnect(dbName)
        for _, row in df.iterrows():
            sqlQuery = f"""INSERT INTO {table_name} 
            (texture_mean, area_mean, smoothness_mean, concavity_mean, fractal_dimension_mean, area_se,
                        smoothness_se, concavity_se, fractal_dimension_se, smoothness_worst, concavity_worst,
                        symmetry_worst, fractal_dimension_worst, diagnosis)
                  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

            data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11],
              row[12], row[13])
            try:
                cursor.execute(sqlQuery, data)
                mydb.commit()
                print('Data inserted successfully')
            except Exception as e:
                mydb.rollback()
                print('Error: ', e)

    def fetch_data(self, table_name):
        """
        A function to fetch data from sql table
        """
        mydb, cursor= DBConnect()
        column = []
        query = "SELECT * FROM {table_name}"
        value = cursor.execute(query)
        for items in cursor.description:
            column.append(items[0])
            mydb.commit()
            df = pd.DataFrame(value, columns=column)
            cursor.close()
            return df

if __name__=="__main__":
    cs = CausalSql()
    cs.createDB(dbName='causality')
    df = pd.read_csv('../data/data2.csv')
    cs.createTables(dbName='causality')
    cs.insert_into_causality(dbName = 'causality', df = df, table_name='Causality')
Footer
