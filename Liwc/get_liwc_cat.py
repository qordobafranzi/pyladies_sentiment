import csv
from collections import defaultdict
import string
import pandas as pd
import sys # Unused import sys
import datetime
import os
from pprint import pprint # Unused pprint imported from pprint
# pp = pprint.PrettyPrinter(indent=4)


class LIWC_Index_Count(): # Very old style class defined :)
    def category_matches(self, doc, categories):
        all_words = {}
        time = datetime.datetime.now()
        print "\nContinue with checking categories, can take some time: %s\n" % (time)
        ''' Returns a mapping of LIWC category -> number of occurrences in the given doc '''
        num_matches = defaultdict(int) # Unused variable 'num_matches'
        words = doc.lower().split(' ')
        words_no_punct = [''.join(ch for ch in token if not ch in string.punctuation) for token in words] 
        for w in words_no_punct:
            for category in categories:
                category_stems = self.LIWC_cat_to_stems[category]
                for stem in category_stems:
                    matches_cat = w.startswith(stem.replace("*","")) if stem.endswith("*") else (stem==w)
                    if matches_cat:
                      word = w
                      bucket = category
                      if category in all_words.keys():
                        all_words[bucket][word] = all_words[bucket].get(word, 0) + 1
                      else:
                        all_words[bucket] =  {w : 1}
                      break # done with this category so move to the next        
       
        print "Done with category check. Finished in: %s\n" % (datetime.datetime.now()- time)
        return all_words
    
    def __init__(self):
        (self.LIWC_stem_to_cats, self.LIWC_cat_to_stems) = self.__init_LIWC_dict__()
    def __init_LIWC_dict__(self):   # Method could be a function :-|
        cat_col_map = {
            'Funct':[0,1,2],
            'Pronoun':[3],
           'Ppron':[4],
           'I':[5],
           'We':[6],
           'You':[7],
           'SheHe':[8],
           'They':[9],
           'Ipron':[10],
           'Article':[11],
           'Verbs':[12, 13, 14],
           'AuxVb':[15],
           'Past':[16],
           'Present':[17, 18],
           'Future':[19],
           'Adverbs':[20],
           'Prep':[21],
           'Conj':[22],
           'Negate':[23],
           'Quant':[24],
           'Numbers':[25],
           'Swear':[26],
           'Social':[27, 28, 29],
           'Family':[30],
           'Friends':[31],
           'Humans':[32],
           'Affect':[33, 34, 35, 36, 37, 38],
           'Posemo':[39, 40, 41],
           'Negemo':[42, 43, 44, 45],
           'Anx':[46],
           'Anger':[47, 48],
           'Sad':[49],
           'CogMech':[50, 51, 52, 53, 54],
           'Insight':[55, 56],
           'Cause':[57],
           'Discrep':[58],
           'Tentat':[59],
           'Certain':[60],
           'Inhib':[61],
           'Incl':[62],
           'Excl':[63],
           'Percept':[64, 65],
           'See':[66],
           'Hear':[67],
           'Feel':[68],
           'Bio':[69, 70, 71, 72],
           'Body':[73, 74],
           'Health':[75, 76],
           'Sexual':[77],
           'Ingest':[78],
           'Relativ':[79, 80, 81, 82, 83],
           'Motion':[84],
           'Space':[85, 86],
           'Time':[87, 88],
           'Work':[89, 90, 91],
           'Achiev':[92, 93],
           'Leisure':[94, 95],
           'Home':[96],
           'Money':[97, 98],
           'Relig':[99, 100],
           'Death':[101],
           'Assent':[102],
           'Nonflu':[103],
           'Filler':[104]
           }
        LIWC_stem_to_cats = defaultdict(list)
        LIWC_cat_to_stems = defaultdict(list)
        LIWC_dictionary = os.path.join(os.path.dirname(__file__), "LIWC2007dictionary.csv")
        
        row_count = -1
        for row in csv.reader(open(LIWC_dictionary, "rU")):
            row_count+=1
            if row_count<3 or row_count>171:
                continue # header rows or past any content
            for cat in cat_col_map:
                cols = cat_col_map[cat]
                for col in cols:
                    wp = row[col]
                    if wp == "":
                        continue
                    LIWC_stem_to_cats[wp].append(cat)
                    LIWC_cat_to_stems[cat].append(wp)
        return (LIWC_stem_to_cats, LIWC_cat_to_stems)

class RevealWordsOfPosts(object):
    """docstring for Confession"""
    def __init__(self, filepath):
        self.filepath = filepath
        
    def getLiwcWords(self):
        num_processed = 0
        time = datetime.datetime.now()
        print '\nStarting parsed LIWC data to reveal Words' + str(time)
        with open(self.filepath, 'rb') as input_file:
          alle = []
          file_content = input_file.read()

          new = LIWC_Index_Count()
          count_whole_corpus = new.category_matches(file_content, ['Posemo', 'Negemo', 'Work'])
          print 'Successfully parsed LIWC data' + str(datetime.datetime.now() - time)

          post_name = self.filepath.split('/')[-1][:-4]
          df = pd.DataFrame.from_dict(count_whole_corpus, orient='columns', dtype=None)
          df.to_csv("Results/" + post_name + "_LIWC_results.csv", sep=',')
          if num_processed % 100 == 0:
            print "%s Posts Processed: %s" % (num_processed, datetime.datetime.now())
          print '\nDone! with parsed LIWC dictionary for revealing Words' + str(datetime.datetime.now() - time)


"""Iterating through posts in given directory"""

for filename in os.listdir("../posts/"):
  RevealWordsOfPosts('../posts/%s' % filename).getLiwcWords()


