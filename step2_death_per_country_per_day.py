import pandas as pd
import numpy as np

# read covid_19 csv file
covid_19_df = pd.read_csv('time_series_covid19_confirmed_global.csv')

# get matix of country and date
covid_19_df.drop(['Province/State','Lat','Long'],axis = 1, inplace = True)
covid_19_df_per_country = covid_19_df.groupby(['Country/Region'], as_index = False).sum()

# unpivot the matix of country and date to dataframe that each country and each day is a separate row 
covid_19_df_unpivot = covid_19_df_per_country.melt(
    id_vars=['Country/Region'], var_name = 'calander',value_name = 'death_per_day')

# insert incremental ID columns as unique id for each record
covid_19_df_unpivot.insert(0,'ID',range(1,1+len(covid_19_df_unpivot)))

#save as data.csv
covid_19_df_unpivot.to_csv('covid_19_df_unpivot.csv',index_label = False)
