import pandas as pd
import streamlit as st
import preprocess,helper
import plotly.express as px
df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')


df=preprocess.preprocess(df,region_df)

menu=st.sidebar.radio(
    'Select an option',
    ('Medal Telly','Data Analysis','Country-wise Analysis',"Athelete-wise Analysis")
)

if menu=='Medal Telly':
    st.header('Medal Tally')
    years, country=helper.country_year_list(df)


    selected_year=st.sidebar.selectbox('Select Year',years)
    selected_country=st.sidebar.selectbox('Select Country',country)
    mt=helper.medal_telly(df,selected_year,selected_country)

    if selected_year=='Overall' and selected_country=='Overall':
        st.title("Overall Medal Tally")
    if selected_year!='Overall' and selected_country=='Overall':
        st.title("Medal Tally in "+str(selected_year)+" Olympics")
    if selected_year=='Overall' and selected_country!='Overall':
        st.title(selected_country+" Overall Performance")
    if selected_year!='Overall' and selected_country!='Overall':
        st.title(selected_country+" Performance in "+str(selected_year)+" Olympics")
    st.table(mt)

if menu == 'Data Analysis':
    editions=df['Year'].nunique()
    cities=df['City'].nunique()
    sports=df['Sport'].nunique()
    events=df['Event'].nunique()
    athletes=df['Name'].nunique()
    nations=df['region'].nunique()-1
    C1,C2,C3=st.columns(3)
    with C1:
        st.header("Total Number of Events")
        st.title(events)
    with C2:
        st.header("Total Number of Sports")
        st.title(sports)
    with C3:
        st.header("Total Number of Cities")
        st.title(cities)
    c1,c2,c3=st.columns(3)
    with c1:
        st.header("Participating Nations")
        st.title(nations)
    with c2:
        st.header("Unique Athletes")
        st.title(athletes)
    with c3:
        st.header("Editions Held")
        st.title(editions)

    nations_over_time=helper.nations_over_time(df)
    fig=px.line(nations_over_time,x='Year',y='Nations')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    














