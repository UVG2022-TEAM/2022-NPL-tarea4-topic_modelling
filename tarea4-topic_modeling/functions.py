import pandas as pd
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from spacy.lang.es import Spanish
import spacy
from typing import Dict, List

def remove_stopwords(texts):
    """Remove stopwords in spanish"""
    stop_words = stopwords.words('spanish')
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]


def sentences_to_words(sentences):
    """Transforms list of text to list of list of words"""
    words = []
    for sentence in sentences:
        words.append(simple_preprocess(str(sentence), deacc=True))
    return words

def generate_bigram_mod (list_words, min_count_p = 5, threshold_p = 10):
    """Returns trigram mod"""
    bigram = Phrases(list_words, min_count=min_count_p, threshold=threshold_p)
    return Phraser(bigram)

def generate_trigram_mod (list_words, min_count_p = 5, threshold_p = 10):
    """Returns trigram mod"""
    bigram = Phrases(list_words, min_count=min_count_p, threshold=threshold_p)
    trigram = Phrases(bigram[list_words], threshold=threshold_p)
    return Phraser(trigram)

def make_bigrams(articles, bigram_mod):
    """Returns trigrams from text"""
    return [bigram_mod[doc] for doc in articles]

def make_trigrams(articles, bigram_mod, trigram_mod):
    """Returns trigrams from text"""
    return [trigram_mod[bigram_mod[doc]] for doc in articles]

def lemmatization(texts: List[List[str]], allowed_postags: List = None) -> List[List[str]]:
    nlp = spacy.load('es_core_news_sm')
    if allowed_postags is None:
        allowed_postags = ['NOUN', 'ADJ', 'ADV']

    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

def plot_subject (result):
    x = []
    y = []
    for i in result:
        x.append(i[0])
        y.append(i[1])
    df_result = pd.DataFrame({'Tema':x, 'Resultado':y })
    df_result.sort_values('Resultado', ascending=False, inplace=True)
    return df_result.plot.bar(y  = 'Resultado', x = 'Tema')