import numpy as np
import pandas as pd


def preprocess(d1, d2):
    # Filtering data for summer olympics
    d1 = d1[d1['Season'] == 'Summer']
    # merge region (region_df) with main data (df)
    d = d1.merge(d2, on='NOC', how='left')
    #  Dropping duplicates
    d.drop_duplicates(inplace=True)
    # One hot encoding of Medals
    d = pd.concat([d, pd.get_dummies(d['Medal'])], axis=1)
    return d


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['region', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].reset_index()
        x = x.sort_values(by='Year', ascending=True).reset_index(drop=True)
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].reset_index()
        x = x.sort_values(by='Gold', ascending=False).reset_index(drop=True)
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x


def medal_tally(df):
    medal_data = df.drop_duplicates(subset=['region', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_data = medal_data.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].reset_index()
    medal_data = medal_data.sort_values(by='Gold', ascending=False).reset_index()
    medal_data['Total'] = medal_data['Gold'] + medal_data['Silver'] + medal_data['Bronze']
    return medal_data


def year_list(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')
    return year


def country_list(df):
    country = np.unique(df['region'].dropna()).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return country


def sport_list(df):
    sp = df['Sport'].unique().tolist()
    sp.sort()
    sp.insert(0, 'Overall')
    return sp


def value_over_time(df, col):
    over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    return over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(5).merge(df, on='Name', how='left')[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates().reset_index()
    return x.rename(columns={'Name': 'Athlete', 'count': 'Medals', 'region': 'Nation'})


def medal_country_list(df):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['region', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    country = np.unique(temp_df['region'].dropna()).tolist()
    country.sort()
    return country


def year_wise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['region', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    medal_data = new_df.groupby('Year').count()['Medal'].reset_index()
    country_medal = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(
        'int')
    return medal_data, country_medal


def most_successful_by_country(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(5).merge(df, on='Name', how='left')[
        ['Name', 'count', 'Sport']].drop_duplicates().reset_index()
    return x.rename(columns={'Name': 'Athlete', 'count': 'Medals'})


def height_weight_scatter_plot(df, sport):
    local_df = df.copy()
    local_df['Medal'] = local_df['Medal'].fillna('No Medal')
    if sport != "Overall":
        local_df = local_df[local_df['Sport'] == sport]
    return local_df


def male_female_graph(df):
    men = df[df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = df[df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    return final
