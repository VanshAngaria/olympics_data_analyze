import streamlit as st
import pandas as pd
import preprocess,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
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

nations_over_time = helper.data_over_time(df,'region')
fig = px.line(nations_over_time, x="region", y="count")
st.title("Participating Nations over the years")
st.plotly_chart(fig)

events_over_time = helper.data_over_time(df, 'Event')
fig = px.line(events_over_time, x="Event", y="count")
st.title("Events over the years")
st.plotly_chart(fig)

athlete_over_time = helper.data_over_time(df, 'Name')
fig = px.line(athlete_over_time, x="Name", y='count')
st.title("Athletes over the years")
st.plotly_chart(fig)

if menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)







