"""
This file includes all the techniques applied for review cleaning. It outputs a cleaned dataset for further use.
"""
import pandas as pd
import os
os.system('pip install demoji')
import demoji
demoji.download_codes()
import spacy
nlp = spacy.load("en_core_web_sm")

class Process():
    def __init__(self, data):
        self.df = pd.DataFrame()
        self.df['Review_Text'] = data
    def lower(self):
        # This function is used for lowercasing all dataset before applying any feature extraction technique.
        self.df['processed'] = self.df['Review_Text'].str.lower()
    def demojify(self):
        # This function is used to remove all emoji from dataset before applying any feature extraction technique.
        for text in self.df['processed']:
            text = demoji.replace(str(text))
        self.df = self.df.dropna(axis=0, subset=['processed']).reset_index(drop=True)
    def remove_1word(self):
        # This function removes all one word reviews from dataset, as they do not contain any useful information on any particular feature.
        j = 0
        indexes = []
        for text in self.df['processed']:
            if(len(nlp(str(text)))==1):
                indexes.append(j)
            j+=1
        self.df = self.df.drop(self.df.index[indexes], axis = 0)
        self.df = self.df.dropna(axis=0, subset=['processed']).reset_index(drop=True)
    def remove_2word(self):
        # This function removes all two word dataset that do not contain any noun+adjective pair, i.e no useful information on any feature.
        j=0
        indexes = []
        keep_pos = ['NOUN', 'ADJ', 'PROPN']
        for text in self.df['processed']:
            token = nlp(str(text))
            if(len(token)==2):
                for tok in token:
                    if(tok.pos_ not in keep_pos):
                        indexes.append(j)
            j+=1
        self.df = self.df.drop(self.df.index[indexes], axis = 0)
        self.df = self.df.dropna(axis=0, subset=['processed']).reset_index(drop=True)
