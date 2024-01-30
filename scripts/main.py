# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 00:27:20 2020

@author: jairp

DRIVER SCRIPT 
"""

##############################################################################
### 1. Import ### 
##############################################################################

import cvparser
import importlib 
importlib.reload(cvparser)

##############################################################################
### 2. Driver script ### 
##############################################################################

if __name__ == "__main__": 
    
    # Provide paths to the documents to be parsed 
    PATH1 = '../data_raw/collegestudent.docx' ## Sample 1
    PATH2 = '../data_raw/Hair_Parra_CV_English.docx' ## Sample 2 
    
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
                                    filename='fetched_Hair_Parra_CV_English',
                                    defaultsave=False) 
    cand_df2 = cv_obj2.to_json(savedir='../data_clean/', 
                               filename='fetched_Hair_Parra_CV_English', 
                               defaultsave=False )
    
    


