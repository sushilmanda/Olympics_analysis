import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt
import helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

data = helper.preprocess(df, region_df)

st.sidebar.image('Olympics_image.png')

st.sidebar.header("Olympics Analysis")

user_menu = st.sidebar.radio(
    "Select an Option",
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

# st.dataframe(df)
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years = helper.year_list(data)
    country = helper.country_list(data)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetch_medal_tally(data, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally of ' + selected_country)
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally of ' + selected_country + ' in ' + str(selected_year))
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = data['Year'].unique().shape[0] - 1
    cities = data['City'].unique().shape[0]
    sports = data['Sport'].unique().shape[0]
    events = data['Event'].unique().shape[0]
    athletes = data['Name'].unique().shape[0]
    nations = data['region'].unique().shape[0]
    st.title('Top Statistics')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.title('Editions')
        st.header(editions)
    with col2:
        st.title('Cities')
        st.header(cities)
    with col3:
        st.title('Sports')
        st.header(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.title('Events')
        st.header(events)
    with col2:
        st.title('Athletes')
        st.header(athletes)
    with col3:
        st.title('Nations')
        st.header(nations)

    st.title('Participating nations over the year')
    over_time_data = helper.value_over_time(data, 'region')
    over_time_data.rename(columns={'Year': 'Edition', 'count': 'No of Countries'}, inplace=True)
    fig = px.line(over_time_data, x='Edition', y='No of Countries')
    st.plotly_chart(fig)

    st.title('Events over the year')
    over_time_data = helper.value_over_time(data, 'Event')
    over_time_data.rename(columns={'Year': 'Edition', 'count': 'No of Event'}, inplace=True)
    fig = px.line(over_time_data, x='Edition', y='No of Event')
    st.plotly_chart(fig)

    st.title('Participating Athletes over the year')
    over_time_data = helper.value_over_time(data, 'Name')
    over_time_data.rename(columns={'Year': 'Edition', 'count': 'No of Athletes'}, inplace=True)
    fig = px.line(over_time_data, x='Edition', y='No of Athletes')
    st.plotly_chart(fig)

    st.title('No. of Events over time (every sport)')
    fig = plt.figure(figsize=(20, 20))
    x = data.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    st.title('Most successful Athletes')
    sp = helper.sport_list(data)
    sp_select = st.sidebar.selectbox('Select Sport for successful Athletes', sp)
    x = helper.most_successful(data, sp_select)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.title('Country wise Analysis')
    country = helper.medal_country_list(data)
    selected_country = st.sidebar.selectbox("Select Country", country)
    country_df, country_medal = helper.year_wise_medal_tally(data, selected_country)

    fig = px.line(country_df, x='Year', y='Medal')
    st.header(selected_country + ' Medal Tally Over The Years')
    st.plotly_chart(fig)

    st.header(selected_country + ' Medals won by Sport over the year')
    fig = plt.figure(figsize=(20, 20))
    ax = sns.heatmap(country_medal, annot=True)
    st.pyplot(fig)

    st.title('Top 5 Most successful Athletes')
    x = helper.most_successful_by_country(data, selected_country).drop(columns='index')
    st.table(x)

if user_menu == 'Athlete-wise Analysis':
    athlete_df = data.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    st.title('Distribution of Age')
    fig.update_layout(autosize=False, width=800, height=500)
    st.plotly_chart(fig)

    all_sports = df['Sport'].unique().tolist()
    x = []
    name = []

    for sport in all_sports:
        local_df = athlete_df[athlete_df['Sport'] == sport]
        if len(local_df['Age'].unique()) <= 1:
            continue
        else:
            x.append(local_df['Age'].dropna())
            name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    st.title('Distribution of Age wrt Sports')
    fig.update_layout(autosize=False, width=800, height=500)
    st.plotly_chart(fig)

    st.title('Height VS Weight')
    sp_list = helper.sport_list(athlete_df)
    sport_select = st.selectbox('Select Sport', sp_list)
    temp_df = helper.height_weight_scatter_plot(athlete_df, sport_select)
    fig = plt.figure(figsize=(15, 15))
    ax = sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=100)
    st.pyplot(fig)

    st.title('Male VS Female Participants')
    temp_df = helper.male_female_graph(athlete_df)
    fig = px.line(temp_df, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=800, height=400)
    st.plotly_chart(fig)
