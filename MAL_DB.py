import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import ast

df = pd.read_csv('/Users/luigibagos/Desktop/MALWebscraper/MAL_DF.csv')

#Clean the DataFrame upon loading
df = df.dropna(subset=['Score', 'Members'])
df = df.reset_index(drop=True)
df['Start_Date'] = pd.to_datetime(df['Start_Date'])
df[['Season', 'Year']] = df['Season'].str.split(' ', expand=True)
df['Year'] = pd.to_datetime(df['Year']).dt.year
df['Total_Watchtime_Days'] = round(df['Episodes'] * df['Min_Per_Ep'] / 1440, 2)

st.set_page_config(page_title="MAL Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")

#SIDEBAR SECTION

st.sidebar.image('/Users/luigibagos/Desktop/MAL_Extract/MAL_Long_Logo.jpg', use_column_width=True)
st.sidebar.header("Use the filters below to explore Top Anime:")

year = st.sidebar.slider(
    "Select the Year:", 
    min_value=int(df["Year"].min()), 
    max_value=int(df["Year"].max()), 
    value=int(df["Year"].max()))

season = st.sidebar.multiselect(
    "Select the Season:",
    options = df["Season"].unique(),
    default =df["Season"].unique()
)

df_selection = df.query(
    "Year == @year & Season == @season"
)

selected_grouping = st.sidebar.radio("See Top Anime Based On:", ['Score', 'Members'])
selected_filter = st.sidebar.radio("Top Anime Grouping:", ['All', 'Top 10', 'Top 100'])

#sorts the anime based on Score and Members. If there is a tie in Score, Members will be the tie breaker and vice versa
if selected_grouping == 'Score':
    df_selection['Rank_Criteria'] = df_selection[['Score', 'Members']].apply(tuple, axis=1)
    df_selection['Rank'] = df_selection.groupby('Year')['Rank_Criteria'].rank(ascending=False).astype(int)
else:
    df_selection['Rank_Criteria'] = df_selection[['Members', 'Score']].apply(tuple, axis=1)
    df_selection['Rank'] = df_selection.groupby('Year')['Rank_Criteria'].rank(ascending=False).astype(int)

df_selection = df_selection.sort_values(by=['Year', 'Rank'])

if selected_filter == 'Top 10':
    df_selection = df_selection[df_selection['Rank'] <= 10]
elif selected_filter == 'Top 100':
    df_selection = df_selection[df_selection['Rank'] <= 100]

if df_selection.empty:
    st.warning("Please select at least one season!")
    st.stop()

df_selection = df_selection.sort_values(by=['Year', 'Rank'])
df_selection = df_selection.reset_index(drop=True)
df_selection.index += 1

# MAIN PAGE SECTION

custom_color = "#2e51a2"

#Title Section

st.markdown(f'''
    <h1 style="color: {custom_color}; text-align: center;">ANIME TV SHOW DASHBOARD</h1>
    <div style="text-align: center; font-size: 24px;">
        <p>In the last 10 years, there have been 2000+ Anime TV Shows that MyAnimeList (MAL) has documented in its website. 
        This dashboard provides a close look at which anime have been the most popular, whether it's due to the highest Scores or highest Member count.
        See what common factors are shared by the most popular anime, you might discover your next show to binge!</p>
    </div>'''
    , unsafe_allow_html=True)
#<b>Highest {selected_grouping} from {year}</b>


st.markdown("##")

#KPI Section
total_anime = df_selection["Title"].count()
total_watchtime = round(df_selection['Total_Watchtime_Days'].sum(),2)
average_score = round(df_selection["Score"].mean(),2)
average_members = '{:,.0f}'.format(int(round(df_selection["Members"].mean(),0)))

KPICol1, KPICol2, KPICol3, KPICol4 = st.columns(4)

with KPICol1:
    st.markdown(
        f'<p style="color: {custom_color}; font-size: 50px;text-align: center;"><b>{total_anime}</b></p>',
        unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 24px;"><b>Anime Shows</b></div>', unsafe_allow_html=True)

with KPICol2:
    st.markdown(
        f'<p style="color: {custom_color}; font-size: 50px;text-align: center;"><b>{total_watchtime}</b></p>',
        unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 24px;"><b>Days Worth of Content</b></div>', unsafe_allow_html=True)

with KPICol3:
    st.markdown(
        f'<p style="color: {custom_color}; font-size: 50px;text-align: center;"><b>{average_score}</b></p>',
        unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 24px;"><b>Average Score</b></div>', unsafe_allow_html=True)

with KPICol4:
    st.markdown(
        f'<p style="color: {custom_color}; font-size: 50px;text-align: center;"><b>{average_members}</b></p>',
        unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 24px;"><b>Average Members</b></div>', unsafe_allow_html=True)

st.markdown("---")

# Dataframe Display Section

relevant_columns = ['Score', 'Members', 'Title', 'English_Title', 'Season', 'Year', 'Demographic', 'Rating', 'Source', 'Genres', 'Themes', 'Studios']
st.dataframe(df_selection[relevant_columns], height=400)

st.markdown("---")

# Visuals Section

#Function for Columns that have string data type for records: Demographic, Rating, Source
def Visualize_String_Column(column_name,filter):
    column_count = df_selection.groupby(column_name).size().reset_index(name='Anime Count').sort_values(by="Anime Count", ascending=True)
        
    visualize_column = px.bar(
        column_count,
        x = 'Anime Count',
        y = column_name,
        orientation = 'h',
        title = f'<b>{column_name} Breakdown of {filter} Anime<b>',
        color_discrete_sequence=[custom_color],
        template="plotly_white")
    
    st.plotly_chart(visualize_column, use_container_width = True)

#Assists with conversion to list for records uploaded from csv
def safe_eval(val):
    try:
        return ast.literal_eval(val)
    except (SyntaxError, ValueError):
        return val 

#Function for Columns that have lists in the record: Studios, Genres, Themes 
def Visualize_List_Column(column_name, filter):

    df_selection[column_name] = df_selection[column_name].apply(safe_eval)
    separated_values = df_selection.explode(column_name)
    values_counts = separated_values[column_name].value_counts()
    column_count = values_counts.reset_index()
    column_count.columns = [column_name, 'Anime Count']

    visualize_column = px.bar(
        column_count.nlargest(10,'Anime Count').sort_values(by="Anime Count", ascending=True),
        x="Anime Count",
        y= column_name,
        orientation="h",
        title=f'<b>Top {column_name} Count of {filter} Anime<b>',
        color_discrete_sequence=[custom_color],
        template="plotly_white",
    )

    st.plotly_chart(visualize_column, use_container_width = True)

left_column, right_column = st.columns(2)

with left_column:
    Visualize_String_Column('Demographic',selected_filter)
    Visualize_List_Column('Genres', selected_filter)
    Visualize_String_Column('Rating',selected_filter)

with right_column:
    Visualize_String_Column('Source',selected_filter)
    Visualize_List_Column('Themes', selected_filter)
    Visualize_List_Column('Studios', selected_filter)
