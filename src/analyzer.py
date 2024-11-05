from transformers import pipeline
import pandas as pd
from wordcloud import WordCloud
import io
import base64

from src.utils import TextProcess

class PoliticalAnalyzer:

    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.zero_shot_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.textprocessor=TextProcess()

    def analyze_content(self, news_df, reddit_df):

        all_text="\n".join([
            ' '.join(news_df['topic'].fillna('').tolist())+
            ' '.join(reddit_df['text'].fillna('').tolist())
        ])

        summary=self.summarizer(all_text[:1024], max_length=120, min_length=20, do_sample=False)[0]['summary_text']

        sentiments=self.sentiment_analyzer(all_text[:1024])

        political_labels = [
            "infrastructure", "education", "healthcare", "safety", "housing",
            "transportation", "environment", "economy", "social services"
        ]

        issues=self.zero_shot_classifier(all_text[:1024], political_labels)

        wordcloud=WordCloud(width=800, height=400, background_color='white').generate(self.textprocessor.clean_text(all_text))

        img=io.BytesIO()

        wordcloud.to_image().save(img, format='PNG')

        img_str = base64.b64encode(img.getvalue()).decode()
        
        return {
            'summary': summary,
            'sentiment': sentiments,
            'key_issues': dict(zip(issues['labels'], issues['scores'])),
            'wordcloud': img_str
        }
    
if __name__=="__main__":
    news_df=pd.read_csv('/teamspace/studios/this_studio/RamailoTech/data/news/news_topics_Texas_20241105_054258.csv')


    reddit_df=pd.read_csv('/teamspace/studios/this_studio/RamailoTech/data/reddit/reddit_discussions_Texas_20241105_054423.csv')

    analyzer=PoliticalAnalyzer()

    print(analyzer.analyze_content(news_df=news_df, reddit_df=reddit_df))
