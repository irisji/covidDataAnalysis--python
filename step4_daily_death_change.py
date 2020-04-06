import pandas as pd
import numpy as np

#read data.csv
covid_19_df_total_death = pd.read_csv('covid_19_df_unpivot.csv')

#data transformation
covid_19_df_total_death.rename(columns = {'Country/Region':'country_region'},inplace = True)
covid_19_df_total_death['calander']= pd.to_datetime(covid_19_df_total_death['calander'])

#get a column 'daily change' of death per day per country
covid_19_df_total_death_sorted = covid_19_df_total_death.sort_values(by=['country_region','calander'],ascending=False)
covid_19_df_total_death_sorted['change_per_day'] = covid_19_df_total_death_sorted['death_per_day']- covid_19_df_total_death_sorted['death_per_day'].shift(-1)
covid_19_df_total_death_sorted.loc[covid_19_df_total_death_sorted['calander']=='2020-01-22','change_per_day'] = ''

#sort data
covid_19_df_daily_death_change = covid_19_df_total_death_sorted.sort_values(by=['country_region','calander']).drop(columns = ['death_per_day'])

#export data as data.csv
covid_19_df_daily_death_change.to_csv('covid_19_df_daily_death_change.csv',index_label = False)