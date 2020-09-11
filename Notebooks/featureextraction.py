"""
The feature class operates on a cleaned dataset to get a list of candidate features, i.e, possible meaningful features after applying POS tagging and Apriori algorithm.
"""

import pandas as pd
import numpy as np
import spacy
nlp = spacy.load("en_core_web_sm")
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import apriori
class Feature():
    def __init__(self, data):
        self.df = pd.DataFrame()
        self.df = data
        return
    def extract_nouns(self):
        # This function is used to extract nouns from the dataset using POS tagging
        keep_pos = ['PROPN', 'NOUN']
        self.df['nouns'] = ''
        i=0
        for text in self.df['processed']:
            self.df['nouns'][i] = [str(tok.lemma_) for tok in nlp(str(text)) if tok.pos_ in keep_pos and len(tok.lemma_)>2]
            i+=1
        self.df = self.df[self.df.astype(str)['nouns'] != '[]']
        self.df = self.df.reset_index(drop=True)
        return
    def extract_nounlist(self):
        # This function is used to get a list of all nouns that are extracted from POS tagging.
        unique = []
        for x in self.df['nouns']:
            for item in x:
                if(item not in unique):
                    unique.append(item)
        with open('noun_list.txt','w') as f:
            f.write('\n'.join(unique))
        return
    def ass_rules(self, support=0.01):
        # This function uses apriori algorithm to apply association rules mining. Default support is set to be 0.01
        self.one_hot_data = self.df['nouns'].str.join('|').str.get_dummies()
        self.frequent_itemsets = apriori(self.one_hot_data, min_support=support, use_colnames=True, max_len=2)
        self.rules = association_rules(self.frequent_itemsets, metric="lift", min_threshold=1)
        return
    def get_features(self):
        # This function is used to extract candidate features after applying association rules mining.
        b=self.frequent_itemsets.iloc[:,1:].values
        self.features = []
        for x in b:
            for i in x:
                self.features.append((list(i)))
