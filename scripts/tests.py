# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 16:05:02 2020

Various tools and libraries tested for the task 

@author: Hair Parra

INSTRUCTIONS: 
    - Place this script inside the `scripts` directory to apply the different
     tets.     
"""

###############################################################################

### 1. Imports ### 

import re
import docx2txt
import cvparser # modify this script 
import pandas as pd
from time import time
from tqdm import tqdm 
from spacy.matcher import Matcher
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer


###########################################################


EDUCATION = [
            'ba', 'ab', 'barts', 'baarts','bsci', 
            'bachelorarts', 'bachelorscience', 'bsba'
            'bachelorcommerce', 'bachelorartsbcience', 
            'bsa','bacy','bacc','bcomm','bs','bcommerce', 
            'bacommerce', 'majorfinance', 
            'me', 'ms', 'btech', 'mtech', 
            'ssc', 'hsc', 'cbse', 'icse', 'x', 'xii'
        ]

SYMBOLS_ext = r'[?|$|.|!|,|\s]|(of)|(and)|\'\(\)'


STOPWORDS = set(stopwords.words('english'))


###############################################################################

# Read word documents

PATH1 = '../data_raw/collegestudent.docx' ## Sample 1
PATH2 = '../data_raw/Hair_Parra_CV_English.docx' ## Sample 2

# extract text
text1 = docx2txt.process(PATH1)
text2 = docx2txt.process(PATH2)


###############################################################################

# Class testing 

cv_obj = cvparser.CV_parser(path=PATH2)
#cv_obj.self_print()

cand_name = cv_obj.fetch_candidate_name() 
cand_phones = cv_obj.fetch_phone_numbers() 
cand_emails = cv_obj.fetch_emails()
cand_educ = cv_obj.fetch_education() 
cand_skills = cv_obj.fetch_skills()
cand_df = cv_obj.to_dataframe()

#cand_data = {'name':cand_name, 'phones':cand_phones,'emails':cand_emails, 
#             'education':cand_educ ,'cand_skills':cand_skills}
#        
#df = pd.DataFrame(cand_data.items(), columns=['Field','Content'] )





nlp_text = [sent.string.strip() for sent in cv_obj.doc.sents]
     
edu ={} 
# Extract education degree 
for idx, text in enumerate(nlp_text): 
    text_unigrams = text.split()         
    text_bigrams = [tup[0] + tup[1] for tup in list(ngrams(text_unigrams,2))]
    all_grams = text_unigrams + text_bigrams
    
    for tok in all_grams: 
        # Replace special symbols and lowercase                
        re_tok = re.sub(SYMBOLS_ext,'',tok.lower().strip())
        print(re_tok)
        if re_tok in EDUCATION and re_tok not in STOPWORDS: 
            edu[tok] = text + nlp_text[idx + 1] 
            
            
matcher = Matcher(cv_obj.nlp.vocab)     
                
nlp_text = cv_obj.doc

# First name and Last name are always Proper Nouns
pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

matcher.add('NAME', None, pattern)

matches = matcher(nlp_text)

for match_id, start, end in matches:
    span = nlp_text[start:end]  
    print(span.text)


# test 
data = pd.read_csv("skills.csv") 

# extract values
skills = list(data.columns.values)


### Fetch skills 

noun_chunks = cv_obj.doc.noun_chunks
nlp_text = cv_obj.doc

# removing stop words and implementing word tokenization
tokens = [token.text for token in nlp_text if not token.is_stop]

data = pd.read_csv("skills.csv")  # reading the csv file
skills = list(data.columns.values) # extract values into a lis
skillset = []  # store final skills here

# check for one-grams (example: python)
for token in tokens:
    if token.lower() in skills:
        skillset.append(token)

# check for bi-grams and tri-grams (example: machine learning)
for token in noun_chunks:
    token = token.text.lower().strip()
    if token in skills:
        skillset.append(token)

return [i.capitalize() for i in set([i.lower() for i in skillset])]

#################################################################################

# REgex Testing

pattern = r'[\w\.-]+@[\w\.-]+'
re.findall(pattern, "sf@somedomain.com fsdfsdfdsfsdfds  hair.parra@gmail.com") 

pattern = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
re.findall(pattern, "514-586-8551  fdfsdsd 555.555.5555  ")

tok = "BA.Commerce?"
re_tok = re.sub(SYMBOLS_ext,'',tok.lower().strip())
re_tok in EDUCATION


r = re.compile(re_tok)

newlist = list(all(r.match, EDUCATION)) # Read Note
print(newlist)













