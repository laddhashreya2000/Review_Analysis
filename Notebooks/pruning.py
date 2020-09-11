"""
The Pruning class is used to obtain a list of meaningful features given a list of candidate features. This is the last part of our feature extraction pipeline.
"""
import pandas as pd
import numpy as np
import spacy
nlp = spacy.load("en_core_web_sm")
import os
os.system('pip install python-levenshtein')
import Levenshtein as lev
import csv

class Pruning():
    def __init__(self, data, feature_list):
        self.df = pd.DataFrame()
        self.df = data
        self.features = feature_list
        return
    def get_one_word_feature(self):
        # This function extracts one word features from a provided combined list of features
        one_word = []
        for feature in self.features:
            if(len(feature)==1):
                for feat in feature:
                    one_word.append(feat)
        return one_word
    def get_two_word_feature(self):
        # This function extracts two word features from a provided combined list of features
        two_word = []
        for feature in self.features:
            if(len(feature)==2):
                two_word.append(feature)
        return two_word
    def superset(self, feature, two_word):
        # This function extracts superset of a one word feature given a list of all the two word features. This is used in redundancy pruning.
        superset = []
        for x in two_word:
            if(x[0] in feature):
                superset.append(x[1])
            elif(x[1] in feature):
                superset.append(x[0])
        return superset

    def final_list(self):
        # This function outputs a list of all the final meaningful features obtained after pruning techniques.
        with open("final_features.txt" , "w") as f:
          for i in self.two_word_features:
            f.write(str(i) + "\n")
          for i in self.one_word_feature:
            f.write(i+"\n")
        return

    def compactness_pruning(self, per=0.44):
        # This function applies the technique of compactness pruning to obtain meaningful two word features.
        two_word = self.get_two_word_feature()
        self.two_word_features = []
        d = {}
        for item in two_word:
            d[' '.join(item)] = [0,0]
        for x in self.df.processed:
            doc = nlp(str(x))
            for sent in doc.sents:
                for tok1 in sent:
                    for feature in two_word:
                        if(tok1.lemma_ in feature):
                            m = tok1.i - sent.start
                            total = 0
                            occurs = 0
                            for tok2 in sent[m+1:]:
                                compact = False
                                if(tok2.lemma_ in feature):
                                    total=1
                                    n = tok2.i - sent.start
                                    if(abs(m-n)<=3):
                                        if(m>n):
                                            span = sent[n:m+1]
                                        else:
                                            span = sent[m:n+1]
                                        for tok3 in span:
                                            if(tok3.pos_ in ['PUNCT', 'CCONJ']):
                                                compact = False
                                                break
                                            else:
                                                compact=True
                                if(compact):
                                    occurs=1
                                    break
                            if(total!=0):
                                d[' '.join(feature)][0]+=total
                                d[' '.join(feature)][1]+=occurs


        with open("compact_pruning.csv", "w") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(['feature', 'total', 'occurs', 'percent'])
            for item in two_word:
                total = d[' '.join(item)][0]
                occurs = d[' '.join(item)][1]
                if(total!=0):
                    percent = occurs/total
                    csvwriter.writerow([item, total, occurs, percent])
                    if(percent>0.4):
                        self.two_word_features.append(item)

    def redundancy_pruning(self, thresh=100):
        # This function applies the technique of redundancy pruning to obtain meaningful one word features.
        one_word = self.get_one_word_feature()
        self.one_word_feature = []
        s = {}
        d = {}
        for item in one_word:
            d[item] = [0,0]
            s[item] = self.superset(item, self.two_word_features)
        for x in self.df.processed:
            doc = nlp(str(x))
            for sent in doc.sents:
                for tok1 in sent:
                    if(tok1.lemma_ in one_word):
                        d[tok1.lemma_][0]+=1
                        c = True
                        for tok2 in sent:
                            if(tok2.lemma_ in s[tok1.lemma_]):
                                c = False
                                break
                        if(c):
                            d[tok1.lemma_][1]+=1
        with open("redund_pruning.csv", "w") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(['feature', 'total', 'p'])
            for item in one_word:
                total = d[item][0]
                occurs = d[item][1]
                csvwriter.writerow([item, total, occurs])
                if(total!=occurs and occurs>thresh):
                    self.one_word_feature.append(item)

    def correct(self):
        # This functions returns a dictionary obtained after applying spelling correction technique, where the keys are the misspelled words and values are correct features.
        feature = []
        for i in self.one_word_feature:
            feature.append(i)
        for i in self.two_word_features:
            for item in i:
                if(item not in feature):
                    feature.append(item)
        self.df['noun_imp']=""
        final_dict={}
        for j in range(len(self.df)):
            self.df['noun_imp'][j] = []
            for i in self.df['nouns'][j]:
                if(final_dict.get(i)):
                    self.df['noun_imp'][j].append(i)
                else:
                    for item in feature:
                        dist = lev.distance(item, i)
                        if(dist<=1 and item[0]==i[0]):
                            self.df['noun_imp'][j].append(i)
                            final_dict[i]=item
                            break
        self.df = self.df[self.df.astype(str)['noun_imp'] != '[]']
        self.df = self.df.reset_index(drop=True)
        self.final_dict = final_dict
        return
