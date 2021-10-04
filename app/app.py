import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


df= pd.read_csv('athlete_events.csv')
region_df= pd.read_csv('noc_regions.csv')

df= preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://cdnph.upi.com/svc/sv/upi/4281505356725/2017/1/4ebf7ba84ea70d9f02236dcc2e5cc7ea/Paris-to-host-2024-Summer-Olympics-Los-Angeles-in-2028.jpg')

user_menu= st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise-Analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country= helper.country_year_list(df)
    selected_year= st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    medal_tally= helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall Perfomance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country+ ' perfomance in ' + str(selected_year) + ' Olympics')

    st.table(medal_tally)
    #st.dataframe(medal_tally)


if user_menu == 'Overall Analysis':
    editions= df['Year'].unique().shape[0] - 1
    cities= df['City'].unique().shape[0]
    sports= df['Sport'].unique().shape[0]
    events= df['Event'].unique().shape[0]
    athletes= df['Name'].unique().shape[0]
    nations= df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3= st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)



    nations_over_time= helper.data_over_time(df,'region')
    fig= px.line(nations_over_time,x='Edition',y='region')
    st.title('Participating Nations over the years')
    st.plotly_chart(fig)

    sports_over_time= helper.data_over_time(df,'Sport')
    fig= px.line(sports_over_time,x='Edition',y='Sport')
    st.title('Sports over the years')
    st.plotly_chart(fig)

    events_over_time= helper.data_over_time(df,'Event')
    fig= px.line(events_over_time,x='Edition',y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig)

    athletes_over_time= helper.data_over_time(df,'Name')
    fig= px.line(athletes_over_time,x='Edition',y='Name')
    st.title('Athletes over the years')
    st.plotly_chart(fig)


    #males vs females over the years
    figure=helper.male_female(df)
    st.header("Male and Female participation over the years")
    #st.text("Male= Blue")
    #st.text('Female= Red')
    st.plotly_chart(figure)


    st.title("No. of events  over time (every sport)")
    fig,ax= plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax= sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)



    st.title('Most successful Athletes')
    sport_list= df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport= st.selectbox('Select a Sport',sport_list)
    x= helper.most_successful(df, selected_sport)
    st.table(x)


if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list= df['region'].dropna().unique().tolist()     ##dropna cos of null values
    country_list.sort()

    selected_country= st.sidebar.selectbox('Select a country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + ' Medals over the years')
    st.plotly_chart(fig)


    ## Country wise Heatmap

    st.title(selected_country + ' Heatmap over the years')
    pt= helper.country_sport_heatmap(df,selected_country)
    fig, ax= plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    ## Top 10 Athletes of each country

    st.title('Top 10 Athletes of '+selected_country)
    temp_df = helper.top_atheletes(df,selected_country)
    st.table(temp_df)

if user_menu == 'Athlete-wise-Analysis':

    st.sidebar.title('Athlete-wise-Analysis')

    athlete_df = df.dropna(subset=['Medal'])
    athlete_list = athlete_df['Name'].dropna().unique().tolist()  ##dropna cos of null values
    athlete_list.sort()

    selected_athlete = st.sidebar.selectbox('Select an athlete', athlete_list)

    t,s,y= helper.ath_d(df,selected_athlete)
    ath_df = helper.athlete_details(df,selected_athlete)
    medals = ath_df['Medals'].sum()

    st.title(selected_athlete)

    col1, col2= st.columns(2)
    with col1:
        st.header('Nation')
        st.subheader(t)
    with col2:
        st.header('Sport')
        st.subheader(s)

    col1, col2 = st.columns(2)
    with col1:
        st.header('Editions Played')
        st.subheader(y)
    with col2:
        st.header('Total Medals')
        st.subheader(medals)

    st.table(ath_df)
