import streamlit as st
import pandas as pd
import medal_tally,helper_medal
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df= pd.read_csv('athlete_events.csv')
df_region = pd.read_csv('noc_regions.csv')

df = medal_tally.process(df,df_region)
# Title of Web App
st.sidebar.title("Olympics Analysis")
st.sidebar.image('Olampic Pic.jpg')
# Skeleton Code for web app
user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country=helper_medal.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",country)
    medal_tally = helper_medal.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Medal Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in "+str(selected_year)+" Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in "+str(selected_year) + " Olampics")
    st.table(medal_tally)
    # In Streamlit rather than using dataframe function use table function for better look
if user_menu == "Overall Analysis":
    st.title("Top Statistics")
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Presenter")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_year = helper_medal.data_over_time(df,'region')
    fig = px.line(nations_over_year, x='Editions', y='region')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_year = helper_medal.data_over_time(df,'Event')
    fig = px.line(events_over_year, x='Editions', y='Event')
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_year = helper_medal.data_over_time(df, 'Name')
    fig = px.line(athletes_over_year,x='Editions',y='Name')
    st.title("Atheletes over the years")
    st.plotly_chart(fig)

    st.title("No of Events over time(Every Sport) Heatmap")
    fig,ax=plt.subplots(figsize=(24,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper_medal.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper_medal.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df,x='Year',y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " details in all sports")
    pt = helper_medal.country_event_heatmap(df,selected_country)
    fig,ax=plt.subplots(figsize=(24,20))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 15 atheletes of "+selected_country)
    top10_df = helper_medal.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age of Atheletes")
    st.plotly_chart(fig)

    #x =[]
    #name = []
    #famous_sports = ['Basketball','Judo','Football','Tug-Of-War','Athletics',
    #                 'Swimming','Badminton','Sailing','Gymnastics',
    #                 'Art Competitions','Handball','Weightlifting','Wrestling',
    #                 'Water Polo','Hockey','Rowing','Fencing','Shooting',
    #                 'Boxing','Taekwondo','Cycling','Diving','Canoeing',
    #                 'Tennis','Golf','Softball','Archery','Volleyball',
    #                 'Synchronized Swimming','Table Tennis','Baseball',
    #                 'Rhythmic Gymnastics','Rugby Sevens','Beach Volleyball',
    #                 'Triathlon','Ruby','Polo','Ice Hockey']
    #for sport in famous_sports:
    #    temp_df = athlete_df[athlete_df['Sport']==sport]
    #    x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
    #    name.append(sport)

    #fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    #fig.update_layout(autosize=False, width=1000, height=600)
    #st.title("Distribution of Age with respect to sports")
    #st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title("Height vs Weight")
    selected_sport = st.selectbox('Select a Sport',sport_list)
    temp_df=helper_medal.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots(figsize=(20,20))
    ax=sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=140)
    st.pyplot(fig)

    st.title("Men vs Women Participation over the Years")
    final=helper_medal.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)

    st.title('Number of Athletes with Sport over the Year')
    new_df = df.pivot_table(index='Sport', columns='Year', values='Name', aggfunc='count').fillna(0).astype('int')
    fig,ax=plt.subplots(figsize=(40, 20))
    ax=sns.heatmap(new_df, annot=True)
    st.pyplot(fig)