"""
This file is to extract reviews of length 1, 2, 3.
For better understanding of dataset.
"""
import spacy
nlp = spacy.load("en_core_web_sm")

def oneword(df):
    # this function is used to extract one word reviews in a list.
  list = []
  for text in df:
    if(len(nlp(str(text)))==1):
      list.append(str(text))
  with open('oneword.txt','w') as f:
    f.write('\n'.join(list))
  return

def twowords(df):
    # this function is used to extract two word reviews in a list.
  list = []
  for text in df:
    if(len(nlp(str(text)))==2):
      list.append(str(text))
  with open('twowords.txt','w') as f:
    f.write('\n'.join(list))
  return

def threewords(df):
    # this function is used to extract three word reviews in a list.
  list = []
  for text in df:
    if(len(nlp(str(text)))==3):
      list.append(str(text))
  with open('threewords.txt','w') as f:
    f.write('\n'.join(list))
  return
