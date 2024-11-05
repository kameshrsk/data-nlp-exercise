from newsapi import NewsApiClient
import pandas as pd
from .utils import ensure_data_dir, get_timestamp
import os

from dotenv import load_dotenv

load_dotenv()

class NewsScraper:

    def __init__(self, api_key):
        self.newsapi=NewsApiClient(api_key=api_key)

    def get_hot_topics(self, city, num_topics=5):

        political_keywords = [
            'politics', 'election', 'government',  'council', 'development', 
            'infrastructure', 'budget', 'tax', 'public service', 'community'
        ]

        all_articles=[]

        for keyword in political_keywords:

            try:
                articles=self.newsapi.get_everything(
                    q=f"{city} {keyword}",
                    language='en',
                    sort_by='relevancy',
                    page=5
                )

                articles=articles['articles']

                

                for article in articles[:num_topics]:
                    all_articles.append({
                        "topic":article['title'],
                        "source":article['source']['name'],
                        'description': article['description'],
                        "url":article['url'],
                        "city":city
                    })

            except Exception as e:
                print(f"Error Fetching the news: {str(e)}")
                return []
        

        df=pd.DataFrame(all_articles)
        ensure_data_dir("news")
        filename=f'data/news/news_topics_{city}_{get_timestamp()}.csv'
        df.to_csv(filename, index=False)

        return df
        
if __name__=="__main__":

    news_scraper=NewsScraper(api_key=os.getenv('NEWS_API_KEY'))

    print(news_scraper.get_hot_topics(city="Texas")) 