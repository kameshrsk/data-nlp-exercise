# Approach

## Tools & Libraries Decided

1) NewsAPI Client - Scrapping News
2) Praw - Scrapping Reddit Discussions
3) HuggingFace Pipeline - Analysing the Discussions
   
     Update: Previously Lnagchain is decided to analyze the text. but due to rate limit and token constrains HuggingFace Pipeline is is chosen
5) Streamlit - Simple frontend

## Approach Decided

1) Develop a news scrapper script for scrapping the news using the newsapi client.
2) Develop a reddit discussion scrapper script using praw library
3) Develop a Analyzer script that utilizes LLM using Langchain
4) Use streamlit for developing the frontend.

#Files and Functionalities

## utils.py

  This file will be helpful in some basic utilities like getting time stamps, text cleaning and directory creations.

## news_scraper.py

  This script will scrap the news using python's newsAPI client library. This will scrap the news topic based on the city concatenated with some political keywords. It will srap atmost 5(variable) topics for each political keyword. These scraped news will be saved as a.csv file and return the same for further processing

## reddit_scraper.py

  This script will scrap the reddit discussions related to the city on some specific political subreddits. This will use the praw library to scrap from reddit. The sraped data will be stored as a .csv file and returned for furhter processing

## analyzer.py

  The analyzer.py script will take care of the analysis of the scraped data. This will utilize huggingface pipeline. Using this the summarizer, sentiment alanyzers are created. There is another Zero shot classifier that classifies the text based on some political label. This script will also create wordcloud to understand the most discussed things in the social media.

## app.py

  This file uses streamlit to create a simple UI with a textbox to enter the city. After clicking Analyze button it will create three tabs for Analysis, public engagement and showing the raw data.
