"""
This file contains the opinion mining pipeline. It outputs the sentiment score of each feature obtained from feature extraction pipeline.
"""

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
import nltk.sentiment.vader as vader
import spacy
nlp = spacy.load("en_core_web_sm")
import csv

class Opinion():
    def __init__(self, data, final_dict, one_word, two_word):
        self.df = pd.DataFrame()
        self.df = data
        self.final_dict = final_dict
        self.one_word_feature = one_word
        self.two_word_features = two_word
        return

    def find(self, sent, m):
        #this function extracts an opinion phrase and outputs a sentiment score. Much detail in report.
        sentiment = SentimentIntensityAnalyzer()
        i=m-1
        while(i>=0 and (m-i)<=2):
            if(sent[i].pos_ in ['PUNCT', 'CCONJ', 'SCONJ']):
              break
            else:
              i=i-1
        j=m
        while(j<(sent.end-sent.start) and (j-m)<=2):
            if(sent[j].pos_ in ['PUNCT', 'CCONJ', 'SCONJ']):
              break
            else:
              j=j+1

        opinion = sentiment.polarity_scores(str(sent[i+1:j]))
        for tok in sent:
            if(tok.pos_ == 'ADJ'):
              return [opinion['pos'], opinion['neg'], opinion['compound']]

        if(opinion['neg']==0.0 and opinion['pos']==0.0):
            for tok in sent:
              if(tok.lemma_ in vader.NEGATE):
                  return [0.00, 0.25 , -0.25] #corresponding to not good

        return [opinion['pos'], opinion['neg'], opinion['compound']]

    def sentiment_score_one_word(self):
        #this function extracts sentiment score for one word features. Much detail about procedure in report.
        op = {}
        for j in range(len(self.df)):
          x = self.df.Review_Text[j]
          doc = nlp(str(x))
          for sent in doc.sents:
            for tok in sent:
              before = False
              after = False
              if(tok.lemma_ in self.df.noun_imp[j]):
                feat = self.final_dict[tok.lemma_]
                if(feat in self.one_word_feature):

                    m = tok.i - sent.start
                    for i in range(m):
                      if(sent[m-1-i].pos_ in ['ADJ', 'VERB']):
                        before = True
                        first = m-1-i
                        break
                    for i in range(m+1, sent.end-sent.start):
                      if(sent[i].pos_ in ['ADJ', 'VERB']):
                        after = True
                        second = i
                        break
                    if(before and after):
                      if((m-first)<=(second-m)):
                        opinion1 = self.find(sent, first)
                      else:
                        opinion1 = self.find(sent, second)
                    elif(before):
                      opinion1 = self.find(sent, first)
                    elif(after):
                      opinion1 = self.find(sent, second)
                    else:
                      opinion1 = [0.0, 0.0, 0.0]

                    if(op.get(feat)):
                      op[feat] = [op[feat][i]+ opinion1[i] for i in range(3)]
                    else:
                      op[feat] = opinion1
        self.one_word_scores = op
        with open("one_word_scores.csv", "w") as f:
          csvwriter = csv.writer(f)
          csvwriter.writerow(['feature', 'pos', 'neg', 'compound', 'score'])
          for key in self.one_word_scores.keys():
             csvwriter.writerow([key, self.one_word_scores[key][0], self.one_word_scores[key][1], self.one_word_scores[key][2], (self.one_word_scores[key][0]*100/(self.one_word_scores[key][0]+self.one_word_scores[key][1]))])
        return


    def sentiment_score_two_word(self):
        #this function extracts sentiment score for two word features. Much detail about procedure in report.  
        op = {}
        for j in range(len(self.df)):
          x = self.df.Review_Text[j]
          doc = nlp(str(x))
          for sent in doc.sents:
            for tok in sent:
              if(tok.lemma_ in self.df.noun_imp[j]):
                feat = self.final_dict[tok.lemma_]
                m = tok.i - sent.start
                for feature in self.two_word_features:
                  if(feat in feature):
                    for tok2 in sent[m+1:]:
                      if(tok2.lemma_ in self.df.noun_imp[j]):
                        if(self.final_dict[tok2.lemma_] in feature):
                          n = tok.i - sent.start
                          before1 = False
                          after1 = False
                          before2 = False
                          after2 = False
                          for i in range(m):
                            if(sent[m-1-i].pos_ in ['ADJ', 'VERB']):
                              before1 = True
                              first1 = m-1-i
                              break
                          for i in range(m+1, sent.end-sent.start):
                            if(sent[i].pos_ in ['ADJ', 'VERB']):
                              after1 = True
                              second1 = i
                              break
                          for i in range(n):
                            if(sent[n-1-i].pos_ in ['ADJ', 'VERB']):
                              before2 = True
                              first2 = n-1-i
                              break
                          for i in range(n+1, sent.end-sent.start):
                            if(sent[i].pos_ in ['ADJ', 'VERB']):
                              after2 = True
                              second2 = i
                              break
                          index = 1000
                          get = 1
                          if(before1):
                            if((m-first1)<=index):
                              index = m-first1
                              get = first1
                          if(after1):
                            if((second1-m)<=index):
                              index = second1 - m
                              get = second1
                          if(before2):
                            if((n-first2)<=index):
                              index = n-first2
                              get = first2
                          if(after2):
                            if((second2-n)<=index):
                              index = second2 - n
                              get = second2

                          opinion1 = self.find(sent, get)
                          if(op.get(" ".join(feature))):
                            op[" ".join(feature)] = [op[" ".join(feature)][i]+ opinion1[i] for i in range(3)]
                          else:
                            op[" ".join(feature)] = opinion1
        self.two_word_scores = op
        with open("two_word_scores.csv", "w") as f:
          csvwriter = csv.writer(f)
          csvwriter.writerow(['feature', 'pos', 'neg', 'compound', 'score'])
          for key in self.two_word_scores.keys():
             csvwriter.writerow([key, self.two_word_scores[key][0], self.two_word_scores[key][1], self.two_word_scores[key][2], (self.two_word_scores[key][0]*100/(self.two_word_scores[key][0]+self.two_word_scores[key][1]))])
        return
