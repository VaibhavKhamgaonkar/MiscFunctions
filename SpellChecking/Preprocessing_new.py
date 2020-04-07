# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:40:56 2019

@author: VaibhavK
"""
import string, pickle
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer,TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import subprocess
import pickle
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV,StratifiedKFold
from sklearn.feature_selection import SelectKBest,chi2,f_classif
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np, pandas as pd, os, time
import re
from collections import Counter
from tqdm import tqdm
import wordninja

class Fucntions():
    ''' Class to perform various preprocessing on text data and model training'''

    def __init__(self, dataFilePath, categoryFilterThreshold = 50, wordsFilePath='D:/Projects/Warranty/Data/big.txt'):
        self.df = pd.read_excel(dataFilePath,sheet_name='Data')
        #self.wordsFilePath = wordsFilePath
        self.dataFilePath = dataFilePath
        def words(text): return re.findall(r'\w+', text.lower())
        self.WORDS = Counter(words(open(wordsFilePath).read()))
        
        self.threshValue = categoryFilterThreshold
        
        
    #@staticmethod()
    def filterCategories(self, threshValue):
        
        temp = pd.DataFrame()
        ''' get all the categories with records greater than threshhold'''
        categories = self.df['category'].unique()[self.df.groupby('category')['comments_text'].count()>threshValue]
         
        for cat in categories:
            temp = pd.concat([temp, self.df[self.df['category'] == cat]],axis=0)
        
        return temp.reset_index()
        
    # =============================================================================
    #   Function to perform Preprocessing task on dataframe   
    # =============================================================================
    def preprocessing(self, onAllData=False, saveData=True):
        '''Function to perform the data cleaning activity, Spell checking, 
        splitting the combined words and creating new attributes
        
        Arguments:
        onAllData = signifies whether to process the entire dataframe or 
                    only specific categories  based on threshold value
        
        saveData = Whether to store the filtered data on the disk.
        
        '''
        """ Removing the adient categories with less observations"""
        if onAllData:
            data = self.data
        
        else:
            data = self.filterCategories(self.threshValue)  
        
        tqdm.pandas()
        ''' Apply the spellcheck transformation on each obervation'''
        print('Applying Spellcheck operation on each words.')
        st = time.time()
        data['correctedText'] = data['comments_text'].progress_apply(lambda x : ' '.join([self.spellCheck(item) for item in x.lower().replace(',', ' ').split()]))
        print(f'Spellcheck operation finished in {np.round((time.time()-st)/60.0, 3)} mins.')
        
        
        ''' Spliting the Combined words '''
        print('Starting combined Word seperation operation on each records.')
        st = time.time()
        data['correctedText'] = data['correctedText'].progress_apply(lambda x : ' '.join([' '.join(wordninja.split(item)) for item in x.replace(',', ' ').split(' ')]))
        print(f'Operation finished in {np.round((time.time()-st)/60.0, 3)} mins.')
        
        if saveData:
            path = '/'.join(self.dataFilePath.split('/')[:-1]) +'/'
            try:
                data.to_excel(path + 'FilteredData.xlsx')
            except Exception as e:
                print(f'{e}\n error in storing file hence using pickle to store the file')
                with open(path+'FilterData.pkl', 'wb') as f:
                    f.write(data)
            
        return data
        
        
    # =============================================================================
    #   Function to Perfom Spell checking 
    # =============================================================================
    def spellCheck(self, word):
        """def words(text): return re.findall(r'\w+', text.lower())"""

        """WORDS = Counter(words(open(self.wordsFilePath).read()))"""
        
        def P(word, N=sum(self.WORDS.values())): 
            "Probability of `word`."
            return self.WORDS[word] / N
        
        def correction(word): 
            "Most probable spelling correction for word."
            return max(candidates(word), key=P)
        
        def candidates(word): 
            "Generate possible spelling corrections for word."
            return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])
        
        def known(words): 
            "The subset of `words` that appear in the dictionary of WORDS."
            return set(w for w in words if w in self.WORDS)
        
        def edits1(word):
            "All edits that are one edit away from `word`."
            letters    = 'abcdefghijklmnopqrstuvwxyz'
            splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
            deletes    = [L + R[1:]               for L, R in splits if R]
            transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
            replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
            inserts    = [L + c + R               for L, R in splits for c in letters]
            return set(deletes + transposes + replaces + inserts)
        
        def edits2(word): 
            "All edits that are two edits away from `word`."
            return (e2 for e1 in edits1(word) for e2 in edits1(e1))
       
        return correction(word)
        



if __name__=='__main__':
    obj = Fucntions(dataFilePath='D:/Projects/data.xlsx',
                    categoryFilterThreshold = 500)
    obj.preprocessing( onAllData=False, saveData=True)
    
    #print(obj.spellCheck('sprng'))
    
    