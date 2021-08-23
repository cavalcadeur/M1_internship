import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models import CoherenceModel
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np

import spacy
#import pyLDAvis
#import pyLDAvis.gensim
import matplotlib.pyplot as plt


def label_topic(post):
    post.label_topic_as("random")
    return post

def lemmatize_stemming(text,stemmer):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def chop_down_text(text,stemmer):
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 2:
            result.append(lemmatize_stemming(token,stemmer))

    return result

def get_topic_from_model(model_results):
    max_value = 0
    result = 0
    for index,score in model_results:
        if score >= max_value:
            max_value = score
            result = index
    return result

def label_topic_list(posts,n=8):
    """
    stemmer = SnowballStemmer("english")
    complete_doc = []
    for p in posts:
        t = p.txt
        p.stemmed_txt = chop_down_text(t,stemmer)
        complete_doc.append(p.stemmed_txt)
    """
    model,bow,coherence_value = best_topic_number(posts)

    for i in range(len(posts)):
        posts[i].label_topic_as(model[bow[i]])

    print("Coherence value : ",coherence_value)
    #print(model.get_document_topics(dict))

    return posts

def train_network(docs,n,talkative=True,passes=6):
    dictionary = gensim.corpora.Dictionary(docs)
    dictionary.filter_extremes(no_below=15, no_above=0.1, keep_n= 100000)

    bag_of_words = [dictionary.doc2bow(doc) for doc in docs]

    lda_model =  gensim.models.LdaMulticore(bag_of_words, num_topics = n, id2word = dictionary, passes = passes, workers = 2)

    coherence_model = CoherenceModel(model=lda_model,dictionary=dictionary,coherence='c_v',texts=docs)

    if talkative:
        for idx, topic in lda_model.print_topics(-1):
            print("Topic: {} \nWords: {}".format(idx, topic ))
            print("\n")

        print("Perplexity :",lda_model.log_perplexity(bag_of_words))
        print("Coherence :",coherence_model.get_coherence())


    return lda_model,bag_of_words,coherence_model

def multiple_label(posts,n_min=6,n_max=50):
    stemmer = SnowballStemmer("english")
    complete_doc = []
    for p in posts:
        t = p.txt
        p.stemmed_txt = chop_down_text(t,stemmer)
        complete_doc.append(p.stemmed_txt)

    for i in range(n_min,n_max+1):
        model,bow,coherence_value = train_network(complete_doc,i,False)
        print("Topics :",i,"   , Coherence :",coherence_value.get_coherence())

def best_topic_number(posts,n_min=6,n_max=32):
    stemmer = SnowballStemmer("english")
    complete_doc = []
    for p in posts:
        t = p.txt
        p.stemmed_txt = chop_down_text(t,stemmer)
        complete_doc.append(p.stemmed_txt)

    best_model,best_bow,best_coherence = 0,0,0

    for i in range(n_min,n_max+1):
        model,bow,coherence_value = train_network(complete_doc,i,False)
        #print("Topics :",i,"   , Coherence :",coherence_value.get_coherence())
        if coherence_value.get_coherence() > best_coherence:
            best_model,best_bow,best_coherence = model,bow,coherence_value.get_coherence()

    for idx, topic in best_model.print_topics(-1):
        print("Topic: {} \nWords: {}".format(idx, topic ))
        print("\n")

    return best_model, best_bow, best_coherence


def different_passes(posts,n=9):
    stemmer = SnowballStemmer("english")
    complete_doc = []
    for p in posts:
        t = p.txt
        p.stemmed_txt = chop_down_text(t,stemmer)
        complete_doc.append(p.stemmed_txt)


    coherences = []
    x = []
    for i in range(2,25,2):
        model,bow,coherence_value = train_network(complete_doc,n,False,i)
        coherences.append(coherence_value.get_coherence())
        x.append(i)

    return x,coherences
