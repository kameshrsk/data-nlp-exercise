import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from datetime import datetime

def ensure_data_dir(subdir):
    if not os.path.exists(f'data/{subdir}'):
        os.makedirs(f'data/{subdir}')

def get_timestamp():
    return datetime.now().strftime('%Y%m%d_%H%M%S')


class TextProcess:

    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'[^\w\s]', '', text)
        text = text.lower()
        return text
    
    def extract_keywords(self, text, n=10):
        words = word_tokenize(self.clean_text(text))
        words = [word for word in words if word not in self.stop_words]
        freq_dist = nltk.FreqDist(words)
        return dict(freq_dist.most_common(n))