import pandas as pd
import numpy as np
def medal_telly(df):
    medal_count=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_count=medal_count.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False)
    medal_count['Total']=medal_count['Gold']+medal_count['Silver']+medal_count['Bronze']
    return medal_count

def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years, country

def medal_telly(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year=='Overall':
        temp_df= medal_df
    if year=='Overall' and country!='Overall':
        flag=1
        temp_df= medal_df[medal_df['region']==country]
    if year!='Overall' and country=='Overall':
        temp_df= medal_df[medal_df['Year']==year]
    if year!='Overall' and country!='Overall':
        temp_df= medal_df[(medal_df['Year']==year) & (medal_df['region']==country)]

    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=False).reset_index()
    else:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].reset_index()
    x['Total']=x['Gold']+x['Silver']+x['Bronze']
    return x

def nations_over_time(df):
    temp_df=df.drop_duplicates(subset=['Year','region','Team'])
    temp_df=temp_df.groupby('Year').nunique()['region'].reset_index()
    temp_df=temp_df.rename(columns={'region':'Nations'})
    return temp_df



