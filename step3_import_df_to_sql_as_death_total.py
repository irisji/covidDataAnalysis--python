import pandas as pd
import numpy as np
import configparser
import pymysql

Config = configparser.ConfigParser()
Config.read("./env.ini")

#open data.csv
covid_19_df_unpivot = pd.read_csv('covid_19_df_unpivot.csv')

#rename Country/Region to country_region
covid_19_df_unpivot.rename(columns={'Country/Region':'country_region'}, inplace=True)

#format date datatype
covid_19_df_unpivot['calander'] = pd.to_datetime(covid_19_df_unpivot['calander']).dt.strftime('%d-%m-%y')

#datetype transformation
def convertor (df):
    for items in df.columns.tolist():
        df[items] = df[items].astype('object')
        
#transform all datatype into object
convertor(covid_19_df_unpivot)

#connect to database 
connection = pymysql.connect(host = Config.get('mysqld', 'host'),
                             user = Config.get('mysqld', 'user'),
                             password = Config.get('mysqld', 'password'))
#define cursor method
cursor = connection.cursor()

# create database name covid_19 
database_name = 'covid_19'
sql_ddrop =  "DROP DATABASE IF EXISTS "+ database_name
cursor.execute(sql_ddrop)
sql_dcreate = "CREATE DATABASE "+ database_name
cursor.execute(sql_dcreate)
    
#show the database list

#connect to database
connection = pymysql.connect(host = Config.get('mysqld', 'host'),
                             user = Config.get('mysqld', 'user'),
                             password = Config.get('mysqld', 'password'),
                             db = Config.get('mysqld', 'dbName'))
cursor = connection.cursor()

#create table death_total
sql = "DROP TABLE IF EXISTS death_total"
cursor.execute(sql)
sql = "CREATE TABLE death_total (ID INT, country_region VARCHAR(255), calander DATE, death_per_day INT )"
cursor.execute(sql)


#insert value row by row____iterrow____

# prepare column list for insert value
cols_list = [str(i) for i in covid_19_df_unpivot.columns.tolist()]
cols = ",".join(cols_list)

for index, row in covid_19_df_unpivot.iterrows():
    sql = "INSERT INTO death_total (" +cols+ ") VALUES ("+"%s,"*(len(row)-1)+"%s)"
    cursor.execute(sql,tuple(row.tolist()))
    connection.commit()
    
#test if data is in database

#close connection with database
connection.close()
