import praw
import pandas as pd
from .utils import ensure_data_dir, get_timestamp

from dotenv import load_dotenv
import os

load_dotenv()

class RedditScraper:

    def __init__(self, client_id, client_secret, user_agent):
        self.reddit=praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def get_discussion(self, news_df, city, limit=5):

        political_subreddits = [
            'politics', 'news', 'localgovernment', 'infrastructure'
        ]

        discussions=[]

        topics=news_df['topic'].tolist()

        for topic in topics:

            for subreddit in political_subreddits:

                try:
                    query=f"{topic} {city}"

                    submissions=self.reddit.subreddit(subreddit).search(
                        query=query, sort='relevance', limit=limit
                    )

                    for submission in submissions:
                        discussions.append({
                            'title': submission.title,
                            'text': submission.selftext,
                            'url': f"https://reddit.com{submission.permalink}",
                            'score': submission.score,
                            'num_comments': submission.num_comments,
                            'topic': topic,
                            'city': city
                        })

                except Exception as e:

                    print(f"Error fetching the discussions: {subreddit}")

        df = pd.DataFrame(discussions)
        ensure_data_dir("reddit")
        filename = f'data/reddit/reddit_discussions_{city}_{get_timestamp()}.csv'
        df.to_csv(filename, index=False)
        
        return df

if __name__=="__main__":

    scrapper=RedditScraper(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent='sentiment-dashboard'
    )

    news_df=pd.read_csv('/teamspace/studios/this_studio/RamailoTech/data/news/news_topics_Texas_20241105_054258.csv')

    city='Texas'

    print(scrapper.get_discussion(news_df, city))
