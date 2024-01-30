# CV_parser
A parser for word and pdf resumes

## Instructions 
1) Go to the `/scripts` directory and run the  `main.py` file for immediate results. 
2) The `data_raw` folder contains two sample CV's to be parsed. 
3) The `data_clean` folder contains the fetched information from the raw input CV's using the `main` script in the `/scripts` directory.
4) Inside the `/scripts` directory, the `cvparser.py` module contains all the main implementaions, which aare called by the `main.py` on the two CVs inside the `data_raw` directory. 

### Demo (main.py) 

```python 

import cvparser

if __name__ == "__main__": 
    
    # Provide paths to the documents to be parsed 
    PATH1 = '../data_raw/collegestudent.docx' ## Sample 1
    PATH2 = '../data_raw/Name1_Name2_CV_English.docx' ## Sample 2 
    
    ## Example 1: Random standup CV
    
    # Object initialization 
    cv_obj1 = cvparser.CV_parser(path=PATH1) 
    
    # saving the parsed objects 
    cand_df1 = cv_obj1.to_dataframe(savedir='../data_clean/', 
                                    filename='fetched_collegestudent',
                                    defaultsave=False) 
    cand_df1 = cv_obj1.to_json(savedir='../data_clean/', 
                               filename='fetched_collegestudent', 
                               defaultsave=False ) 
    
    
    ## 2. Example 2: my own CV sample
    
    # object initalization 
    cv_obj2 = cvparser.CV_parser(path=PATH2) 
    
    # save the parsed objects to csv or json 
    cand_df2 = cv_obj2.to_dataframe(savedir='../data_clean/', 
                                    filename='fetched_Name1_Name2_CV_English',
                                    defaultsave=False) 
    cand_df2 = cv_obj2.to_json(savedir='../data_clean/', 
                               filename='fetched_Name1_Name2_CV_English', 
                               defaultsave=False )

```
**Output:** 

```
Initializing...
processing file...
Fitting text to spaCY NLP model...
Done in 1.5814540386199951 seconds.

Parsing document...
self.doc.sents: <generator object at 0x000001FC4F91CA60>
         Field                                            Content
0        names      [Susan, Forsythe, Susan Forsythe\n\nSometown]
1       phones                                     [555.555.5555]
2       emails                                [sf@somedomain.com]
3       github                                                 []
4     linkedin                                                 []
5      degrees                                    [BusinessMajor]
6       skills                                                 []
7    education                                      [XYZ College]
8    languages                                                 []
9    addresses                                                 []
10  raw_resume  Susan Forsythe\n\nSometown, AZ 55555  |  555.5...
Initializing...
processing file...
Fitting text to spaCY NLP model...
Done in 1.3370723724365234 seconds.

Parsing document...
self.doc.sents: <generator object at 0x000001FC65E3AD30>
         Field                                            Content
0        names                        [NAME1, NAME2, NAME1 NAME2]
1       phones                           [999-999-9999, 014-2016]
2       emails             [enail1@outlook.com, email2@gmail.com]
3       github                    [https://github.com/Name1Name2]
4     linkedin  [https://www.linkedin.com/in/name1-name2-506ba...
5      degrees                                             [B.A.]
6       skills       [R/rstudio, Nlp, Postgresql, Sql, Ml, Mysql]
7    education                                [Staten University]
8    languages  [cantonese, chinese, english, french, italian,...
9    addresses                                                 []
10  raw_resume  Name1Name2\n\nMontreal, Quebec...
```

**JSON output:** 
```json
{
    "names": [
        "NAME1",
        "NAME2",
        "NAME1 NAME2"
    ],
    "phones": [
        "999-999-9999",
        "014-2016"
    ],
    "emails": [
        "email1@outlook.com",
        "email2@gmail.com"
    ],
    "github": [
        "https://github.com/Name1Name2"
    ],
    "linkedin": [
        "https://www.linkedin.com/in/name1-name2-529hc19b/"
    ],
    "degrees": [
        "B.A."
    ],
    "skills": [
        "R/rstudio",
        "Nlp",
        "Postgresql",
        "Sql",
        "Ml",
        "Mysql"
    ],
    "education": [
        "Staten University"
    ],
    "languages": [
        "cantonese",
        "chinese",
        "english",
        "french",
        "italian",
        "japanese",
        "korean",
        "mandarin",
        "portuguese",
        "russian",
        "spanish"
    ],
    "addresses": [],
    "raw_resume": "NAME1 NAME2\n\nMonterey [...]"
}
```

## Sources: 
- https://github.com/bjherger/ResumeParser/blob/master/bin/main.py 
- https://spacy.io/usage/processing-pipelines 
- https://medium.com/@divalicious.priya/information-extraction-from-cv-acec216c3f48 
- https://github.com/divapriya/Language_Processing/blob/master/resumeParser.py
- https://www.omkarpathak.in/2018/12/18/writing-your-own-resume-parser/ 

## TODO 
- Implement support for pdf documents
- Fix degrees parsing outputs styling
- Add hobbies extraction 
