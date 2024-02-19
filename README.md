This project was created out of a desire to demonstrate the variety of different skills I have picked up when learning Python. A common recommendation has always been to create a project about a topic you are interested in, so I opted to create one about anime! Since MyAnimeList was such a well known database for anime content, I thought it would be cool to explore how I can webscrape all anime info from this website and convert it into a usable dashboard. 

To learn more about what led to this project, my general workflow and findings,  you can check my portoflio website: https://www.luigibagos.com/malwebscraper

In summary, the objective of this project is to do an analysis of MyAnimeList Website Data. It is comprised of two parts:
1. **Create a Webscraper to obtain anime data.** I would focus on Anime TV shows across Winter, Spring, Summer and Fall Seasons from 2014 - 2023.

![Output](https://github.com/luigibagos94/MALWebscraper/assets/133476028/9b12043d-5ebf-4ec0-8eca-8ee772e3cf5e)
![Screen Shot 2024-01-11 at 8 02 04 AM](https://github.com/luigibagos94/MALWebscraper/assets/133476028/ab1cdf1f-672a-4c57-9a6a-9a1d87b66780)

2. **Visualize the extracted data using Streamlit.** This dashboard makes use of packages like streamlit, pandas, to visualize anime data. I wanted this to be a simple dashboard, but I wanted to ensure python was the main language I used.

![Screen Shot 2024-02-03 at 8 45 46 AM](https://github.com/luigibagos94/MALWebscraper/assets/133476028/71d93fb8-29e3-43ae-83fe-2629517eec99)

To set up this project, I used the following files: 

**MAL_Webscraper.ipynb** - This is the Jupyter Notebook file used to run the webscraper from which I was able to extract 10 years worth of MAL website data. It is comprised of different functions that are described in further detail in the actual notebook. The main output of this file is a CSV extract with organized data that was fed into a Streamlit dashboard

**MAL_DB.py** - This is the main python file used to generate the Streamlit dashboard. It takes the output of the previous file and uses it as an input for dashboard's visualizations. 

**MAL_DF.csv** - This is the dataframe that was generated from the webscraper and fed into the dashboard. 

**MAL_Long_Logo.jpg** - This is just the file I used for the logo in the dashboard. 

**requirements.txt** - This files contains the specific requirements needed to replicate this program. 

To see the final output, check the link: https://myanimelistdashboard.streamlit.app/
