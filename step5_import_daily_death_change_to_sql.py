import pandas as pd
import numpy as np
import configparser
import pymysql

Config = configparser.ConfigParser()
Config.read("./env.ini")


#open data.csv
covid_19_df_daily_death_change = pd.read_csv('covid_19_df_daily_death_change.csv')

#remove nan 
covid_19_df_daily_death_change.loc[covid_19_df_daily_death_change['calander']=='2020-01-22','change_per_day'] = 0

#datetype transformation
def convertor (df):
    for items in df.columns.tolist():
        df[items] = df[items].astype('object')

#transform all datatype into object
convertor(covid_19_df_daily_death_change)

#connect to database 
connection = pymysql.connect(host = Config.get('mysqld','host'),
                             user = Config.get('mysqld','user'),
                             password = Config.get('mysqld','password'),
                             db = Config.get('mysqld','dbName'))
#define cursor method
cursor = connection.cursor()


#drop table deaths_change_python if exists
cursor.execute("DROP TABLE IF EXISTS deaths_change_python")
connection.commit()

#create table deaths_change_python
sql = "CREATE TABLE deaths_change_python (ID INT, country_region VARCHAR(255), calander DATE, change_per_day INT)"
cursor.execute(sql)


#insert value row by row____iterrow____

# prepare column list for insert value
cols_list = [str(i) for i in covid_19_df_daily_death_change.columns.tolist()]
cols = ",".join(cols_list)
for index, row in covid_19_df_daily_death_change.iterrows():
    sql = "INSERT INTO deaths_change_python (" +cols+ ") VALUES ("+"%s,"*(len(row)-1)+"%s)"
    cursor.execute(sql,tuple(row.tolist()))
    connection.commit()
    

#close connection with database
connection.close()

