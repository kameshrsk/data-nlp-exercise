import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd

from src.news_scraper import NewsScraper
from src.reddit_scraper import RedditScraper
from src.analyzer import PoliticalAnalyzer

load_dotenv()

news_scraper=NewsScraper(api_key=os.getenv('NEWS_API_KEY'))

reddit_scrapper=RedditScraper(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent='sentiment-dashboard'
    )

analyzer=PoliticalAnalyzer()

st.title('Political Sentiment Analysis')

city=st.text_input("Enter City Name to Analyze")

if st.button("Analyze"):
    if city:

        tab1, tab2, tab3 = st.tabs(["Analysis", "Public Engagement", "Raw Data"])

        with st.spinner("Data Gathering and Analysis in Progress..."):
            news_df=news_scraper.get_hot_topics(city=city)

            reddit_df=reddit_scrapper.get_discussion(news_df, city)

            analysis=analyzer.analyze_content(news_df, reddit_df)

            with tab1:
                st.subheader("Insights")
                st.write(analysis['summary'])

                st.subheader("People's Mindset")
                st.write(f"People Stand towards the current Government: {analysis['sentiment'][0]['label']}")

                st.subheader('Word Cloud')
                st.image(f"data:image/png;base64,{analysis['wordcloud']}")

                st.subheader('Key Issues')
                issues_df = pd.DataFrame(
                    analysis['key_issues'].items(),
                    columns=['Issue', 'Relevance']
                ).sort_values('Relevance', ascending=False)
                st.bar_chart(issues_df.set_index('Issue'))

            with tab2:
                st.subheader('News Coverage')
                for _, row in news_df.head(5).iterrows():
                    with st.expander(row['topic']):
                        st.write(row['description'])
                        st.write(f"Source: [{row['source']}]({row['url']})")
                
                st.subheader('Public Discussions')
                for _, row in reddit_df.head(5).iterrows():
                    with st.expander(row['title']):
                        st.write(row['text'])
                        st.write(f"Engagement: {row['score']} points, {row['num_comments']} comments")
            
            # Tab 3: Raw Data
            with tab3:
                st.subheader('News Data')
                st.dataframe(news_df)
                
                st.subheader('Reddit Data')
                st.dataframe(reddit_df)
    else:
        st.warning('Please enter a city name.')