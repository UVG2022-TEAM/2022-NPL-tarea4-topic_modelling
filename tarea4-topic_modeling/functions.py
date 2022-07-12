import pandas as pd
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords

def remove_stopwords(texts):
    """Remove stopwords in spanish"""
    stop_words = stopwords.words('spanish')
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]


def sentences_to_words(sentences):
    words = []
    for sentence in sentences:
        words.append(simple_preprocess(str(sentence), deacc=True))
    return words