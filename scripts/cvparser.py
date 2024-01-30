# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 17:12:39 2020

@author: jairp

cyparser.py: 
    This module contains all the main implementations for a CV parser, 
    encapsulated inside the class `CV_parser`. This class can be loaded and 
    imported form another class when copied into the same directory. 
"""

###############################################################################

### 1. Imports ###

import re 
import json 
import nltk 
import spacy 
import docx2txt 
import pandas as pd
from time import time
from urllib.parse import urlparse
from spacy.matcher import Matcher 
from nltk.util import ngrams 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.tokenize import sent_tokenize 
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from win32com.client import Dispatch
speak = Dispatch("SAPI.SpVoice")


nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

###############################################################################

EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+'
PHONE_REGEX = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
LINKS_REGEX = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
STREET_REGEX = r'\d{1,4}( \w+){1,5}, (.*), ( \w+){1,5}, (AZ|CA|CO|NH), [0-9]{5}(-[0-9]{4})?'
SYMBOLS = r'[?|$|.|!|,]'
SYMBOLS_ext = r'[?|$|.|!|,|\s]|(of)|(and)| '


# Education Degrees
EDUCATION = [
    'ba', 'ab', 'barts', 'baarts', 'bsci',
    'bachelorarts', 'bachelorscience',
    'bachelorcommerce', 'bachelorartsbcience',
    'bsa', 'bacy', 'bacc', 'bcomm', 'bs', 'bcommerce',
    'bacommerce', 'businessmajor',
    'me', 'ms', 'btech', 'mtech',
    'ssc', 'hsc', 'cbse', 'icse', 'x', 'xii'
]

# Languages 
LANGUAGES = [
    'english','french','spanish','italian','portuguese', 
    'chinese','mandarin', 'japanese','korean','cantonese', 
    'german','russian'
]

# Educational institutions 
SCHOOLWORDS = [
    'school', 'college', 'univers', 'academy', 'faculty',
    'institute', 'faculdades', 'Schola', 'schule',
    'lise', 'lyceum', 'lycee', 'polytechnic', 'kolej',
    'ünivers', 'okul',
]

###############################################################################

### 3. Object Implementation ###

class CV_parser():
    """
    A class used to automatically parse CVs and extract useful information from them. 

    Attributes
    ----------
    says_str : str 
        a formatted string to print out what the animal says
    name : str 
        the name of the animal
    sound : str 
        the sound that the animal makes
    num_legs : int
        the number of legs the animal has (default 4) 

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """

    def __init__(self, stringtext='',  path='', language='english', language_model='md'):
        """ 
        Sets up a CV parser according to input language.
        Example languages: 'english','french','spanish'
        NOTE: Works best in English (to be extended to French later)
        
        @attributes: 
            @ stringtext: full parsed word text 
            @ _language : parser language 
            @ word_tokenizer : nltk word tokenizer
            @ sent_tokeizer : nltk sentence tokenizer 
            @ stemmer : nltk Snowball stemmer  
            @ lemmatizer : nltk lemmatizer 
            @ stopwords :  stopwords list from input language
            
        @ other arguments: 
            @ path:  input PATH to try to parse 
        """
        
        ### Attributes ### 
        
        # General 
        self._language = language 
        self.language_model = None 
        self.stringtext = "" # text version of the input 
        self.stopwords = None 
        
        # Parsing objects 
        self.word_tokenizer = word_tokenize  # Re-assign word tokenizer
        self.sent_tokenizer = sent_tokenize  # Re-assign sentence tokenizer
        self.stemmer = None 
        self.lemmatizer = WordNetLemmatizer()  # Re-assign lemmatizer
        
        # SpaCy objects 
        self.nlp = None  # instantiate model
        self.doc = None  # fitted object in spacy nlp
        self.matcher = None  # to match NER
        
        # Intermediate fetched fields 
        self._links = []
        
        # Parsed document in dictionary format 
        self.parsed_doc = {}
        
        ### Attributes ### 
        
        print("Initializing...")
        t0 = time()  # timing

        if language == 'english':
            self._language = 'english'

            if language_model == 'sm':
                self.language_model = 'en_core_web_sm'
            elif language_model == 'lg':
                self.language_model = 'en_core_web_lg'
            else:
                self.language_model = 'en_core_web_md'

        elif language == 'spanish':
            self._language = 'spanish'

            if language_model == 'sm':
                self.language_model = 'es_core_news_sm'
            else:
                self.language_model = 'es_core_news_md'

        elif language == 'french':
            self._language = 'french'

            if language_model == 'sm':
                self.language_model = 'fr_core_news_sm'
            else:
                self.language_model = 'fr_core_news_md'

        else:
            message = "Input language not recognized. "
            message += "Please make sure to input a valid language. \n"
            message += "Valid languages are : 'english','spanish''french'"
            raise ValueError(message)

        # Initialize Snowball stemmer
        self.stemmer = SnowballStemmer(language=self._language)

        # Obtain language stopwords
        self.stopwords = set(stopwords.words(self._language))

        try:
            # Option for when the input is already in string format
            if type(stringtext) == str and len(stringtext) > 1:
                print("stringtext input")
                self.stringtext = stringtext
            elif len(path) > 1:
                print("processing file...")
                # convert into string and assign
                self.stringtext = docx2txt.process(path)
            else:
                raise ValueError("Invalid Input")

        except Exception as e:
            print("ERROR: Something went wrong")
            e.with_traceback()

        # Initialize SpaCy objects
        print("Fitting text to spaCY NLP model...")
        self.nlp = spacy.load(self.language_model)  # instantiate model
        self.doc = self.nlp(self.stringtext)  # fitted object in spacy nlp
        self.matcher = Matcher(self.nlp.vocab)  # to match NER
        t1 = time() ; print("Done in {} seconds.".format(t1-t0))
        
        # Automatically parse input document 
        print("\nParsing document...")
        self.fetch_self() 
        

    @property
    def language(self):
        return self._language

    def self_print(self):
        print(self.stringtext)

    def self_tokenize(self):
        return self.word_tokenizer(self.stringtext)

    def fetch_candidate_name(self):
        """ 
        Fetches candidate name from input text
        """
        # variable to save possible matches
        possible_names = []

        # source text is input document in text format
        nlp_text = self.doc  # := nlp(self.stringtext)

        # Add patterns to match proper names
        patterns = [[{'POS': 'PROPN'}]]
        self.matcher.add('NAME', patterns) 
        matches = self.matcher(nlp_text) 

        # fetch the matches
        for match_id, start, end in matches:
            span = nlp_text[start:end] 
            possible_names += [span.text] 
            if len(possible_names) >= 2: 
                break

        # Extract candidates
        doc_entities = self.doc.ents

        # Subset to person type entities
        doc_persons = filter(lambda x: x.label_ == 'PERSON', doc_entities)
        doc_persons = filter(lambda x: len(
            x.text.strip().split()) >= 2, doc_persons)
        doc_persons = map(lambda x: x.text.strip(), doc_persons)
        doc_persons = list(doc_persons)

        # Assume the first Person entity with more than two tokens is the candidate's name
        if len(doc_persons) > 0:
            return possible_names + [doc_persons[0]]

        return "NOT FOUND"

    def fetch_emails(self):
        return re.findall(EMAIL_REGEX, self.stringtext)

    def fetch_phone_numbers(self):
        return re.findall(PHONE_REGEX, self.stringtext)

    def fetch_links(self):
        return re.findall(LINKS_REGEX, self.stringtext)
    
    def fetch_address(self): 
        # apply regrex finding for all sentences  
        addr_list = [ l for sent in self.doc.sents for l in re.findall(STREET_REGEX, sent.text)]
        
        return addr_list
    
    def fetch_languages(self): 
        """
        Obtains language tokens in string text
        """
               
        # tokenize, clean and filter document tokens 
        toks = [re.sub(r'[^a-zA-Z]','', tok.text.lower().strip()) for tok in self.doc]
        toks = [tok for tok in toks if len(tok)>1 and tok in LANGUAGES]
        toks = sorted(set(toks))
        
        return toks
    
    def fetch_github(self): 
        
        # fetch links if they haven't been fetched yet 
        if not self._links: 
            self._links = self.fetch_links()
            
        # identify if they actually are links containing `github` 
        urls = [l for l in self._links if 'github' in l] 
        
        # filter urls depending on paths and only keep 2 
        urls = [l for l in urls if len(urlparse(l).path.split('/')) <= 2 ] 
                
        return urls
    
    
    def fetch_linkedin(self): 
        
        # fetch links if they haven't been fetched yet 
        if not self._links: 
            self._links = self.fetch_links()
            
        # identify links containing 'linkedin' 
        urls = [l for l in self._links if 'linkedin' in l] 
                
        return urls
    

    def fetch_degrees(self):
        """
        Fetch education like tokens from the applicant's CV
        """
        # Sentence tokenize text
        print("self.doc.sents:", self.doc.sents)
        nlp_text = [str(sent).strip() for sent in self.doc.sents]

        # dictionary to save possible educations
        edu = {}

        # Extract education degree
        for idx, text in enumerate(nlp_text):

            # split the text, obtain bigrams, and cat both
            text_unigrams = text.split()
            text_bigrams = [tup[0] + tup[1]
                            for tup in list(ngrams(text_unigrams, 2))]
            all_grams = text_unigrams + text_bigrams

            # filder every ngram obtained
            for tok in all_grams:

                # Replace special symbols and lowercase to match list of possible degrees
                re_tok = re.sub(SYMBOLS_ext, '', tok.lower().strip())

                # if the token is matched , return actual
                if re_tok in EDUCATION and re_tok not in self.stopwords:
                    edu[tok] = text + nlp_text[idx + 1]

        # extract year? 
        education = []
        for key in edu.keys():
            year = re.search(re.compile(r'(((19|20)(\d{2})))'), edu[key])
            if year:
                education.append((key, ''.join(year[0])))
            else:
                education.append(key)

        return education
    
    
    def fetch_education(self): 
        """
        Attemps to fetch educational institutions using nltk NER
        """
        # intialize storage vars
        organizations = []
        education = set()

        ## 1.  first get all the organization names using nltk
        
        # go through every sentence
        for sent in nltk.sent_tokenize(self.stringtext):
            # the through every POS-tagged chunk 
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                # filter organizations 
                if hasattr(chunk, 'label') and chunk.label() == 'ORGANIZATION':
                    # append the matches to the result 
                    organizations.append(' '.join(c[0] for c in chunk.leaves()))
    
        # we search for each bigram and trigram for reserved words
        # (college, university etc...)
        for org in organizations:
            for word in SCHOOLWORDS:
                # append if it appears in the organization 
                if org.lower().find(word) >= 0:
                    education.add(org)
    
        return list(education)
    
            

    def fetch_skills(self):
        """ 
        Look for skillset matches based on a reference skills file
        """

        noun_chunks = self.doc.noun_chunks
        nlp_text = self.doc

        # removing stop words and implementing word tokenization
        tokens = [token.text for token in nlp_text if not token.is_stop]

        data = pd.read_csv("skills.csv")  # reading the csv file
        skills = list(data.columns.values)  # extract values into a lis
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

    def fetch_self(self):
        """
        Calls method to obtain information from input document and stores it. 
        """
        self.parsed_doc['names'] = self.fetch_candidate_name() 
        self.parsed_doc['phones'] = self.fetch_phone_numbers() 
        self.parsed_doc['emails'] = self.fetch_emails() 
        self.parsed_doc['github'] = self.fetch_github() 
        self.parsed_doc['linkedin'] = self.fetch_linkedin() 
        self.parsed_doc['degrees'] = self.fetch_degrees() 
        self.parsed_doc['skills'] = self.fetch_skills() 
        self.parsed_doc['education'] = self.fetch_education() 
        self.parsed_doc['languages'] = self.fetch_languages() 
        self.parsed_doc['addresses'] = self.fetch_address() 
        self.parsed_doc['raw_resume'] = self.stringtext

    def to_json(self, savedir='', filename='', defaultsave=False):
        """
        Saves extracted information as a json file
        @args: 
            - savedir: target saving directory path 
            - filename: name of the file 
            - defaultsave: determines whether to save on the same location as the 
                           running script 
        """
        # Create the savepath
        savepath = savedir + '/' + filename + '.json'

        # save filepath according to input filename
        if len(savepath) > 2:
            with open(savepath, 'w') as fp:
                json.dump(self.parsed_doc, fp, indent=4)

        elif defaultsave:
            with open(filename + '.json', 'w') as fp:
                json.dump(self.parsed_doc, fp, indent=4)

    def to_dataframe(self, savedir='', filename='', defaultsave=False):
        """ 
        Saves extracted information as a dataframe
        """
        # Create the savepath
        savepath = savedir + '/' + filename + '.csv'

        # Convert to pandas dataframe
        df = pd.DataFrame(self.parsed_doc.items(),
                          columns=['Field', 'Content'])
        print(df)

        # save file if prompted
        if len(savepath) > 2:
            df.to_csv(savepath)
        elif defaultsave:
            df.to_csv()

        return df

    def mistery_function(self):
        print("\U0001f600")
        print("Thank you for trying my code!")
        speak.speak("Thank you for trying my code!")
        speak.speak("Wink, wink~")
