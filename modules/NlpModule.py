import io
import random
import string
import warnings
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer

from exceptions.NlpQueryNotFoundException import NlpQueryNotFoundException





class NLP:
    def __init__(self, filePath = None) -> None:
        self.firstTimeDownload()
        self.allTimeDownload()
        if filePath == None:
            filePath = r'database\output.txt'

        #Reading in the corpus
        with open(filePath,'r', encoding='utf8', errors ='ignore') as fin:
            self.raw = fin.read().lower()

        #TOkenisation
        self.sent_tokens = nltk.sent_tokenize(self.raw)# converts to list of sentences 
        self.word_tokens = nltk.word_tokenize(self.raw)# converts to list of words

        self.preprocessingNlp()

    # Generating response
    def standAloneInput(self, question):
        self.sent_tokens.append(question)
        TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx=vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(float(req_tfidf) == 0.0):
            raise NlpQueryNotFoundException
        else:
            return self.sent_tokens[idx]

    def firstTimeDownload(self):
        nltk.download('punkt') # first-time use only
        nltk.download('wordnet') # first-time use only

    def allTimeDownload(self):
        nltk.download('popular', quiet=True) # for downloading packages

    # Preprocessing
    def preprocessingNlp(self):
        self.lemmer = WordNetLemmatizer()
        self.remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        
    def LemTokens(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]
        
    
    def LemNormalize(self, text):
        return self.LemTokens(nltk.word_tokenize(text.lower().translate(self.remove_punct_dict)))


