#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as array # Unused numpy imported as array
import csv
import string
import datetime
import os, sys # Unused import sys 
import collections # Unused import collections
import itertools
import random
from time import sleep # Unused imports are dead code, bringing no value to the code.
import math


class Emotions(object):
  """docstring for ClassName"""
  def __init__(self, filepath):
    self.filepath = filepath

  def get_emotions(self):
    all_dates = []
    all_emotions = []
    all_values = []

    with open(self.filepath) as input_file:
      post = input_file.read()
    words = post.lower().split(' ')
    words_no_punct = [''.join(ch for ch in token if not ch in string.punctuation) for token in words] 

    length = len(words_no_punct)
    emotion_index = []
    emotions_in_message = []
    emotions_count = []

    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "emotion_Lexicon.csv"))
    for word in words_no_punct:
      if any(df['TargetWord'] == word):
        df2 =  pd.DataFrame(df.loc[df['TargetWord'] == word, 'AssociationFlag'] == 1)
        
        try:
          a = df2[df2['AssociationFlag'] == True].index.values
          emotion_index.append(a)
        except KeyError:
          pass

    for i in emotion_index:
      if i.size is not 0:
        for k in i:
          emotions = df.get_value(k, 'AffectCategory')
          emotions_in_message.append(emotions)

    # emotion_set = ['positive', 'joy','anticipation', 'trust', 'surprise', 'anger',  'disgust',  'fear', 'sadness', 'negative']
    emotion_set = ['positive', 'negative']

   # Statements that don't have any side-effect and whose return value isn't used.
    for entry in emotion_set:
      count = emotions_in_message.count(entry)
      all_values.append(count)
      all_emotions.append(entry)

    columns = ['key', 'value']
    df5 = pd.DataFrame(columns=columns)
    df5['key'] = all_emotions
    df5['value'] = all_values

    post_name = self.filepath.split('/')[-1][:-4]
    df5.to_csv("Results/" + post_name + "_EMOTION_results.csv", sep=',')
    # df5 = df5.append(df5)

for filename in os.listdir("../posts/"):
  Emotions('../posts/%s' % filename).get_emotions()
