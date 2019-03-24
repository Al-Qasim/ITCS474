import sys
import os
import re

def extract_poem():
    """[summary]
    might not be using it
    Returns:
        [type] -- [description]
        dict    --  postings lists of arabic words
    """

    postings_list={}
    with open("Ibn_maleks_mille.txt", encoding='utf-8') as ofile:
        
        for loc, line in enumerate(ofile, 1):
            
            for word in re.split("[^\u0621-\u064a\ufb50-\ufdff\ufe70-\ufefc]", line):
                
                if word not in postings_list: 
                    
                    postings_list[word]=[loc] 
                
                else:
                    
                    postings_list[word].append(loc) 
    
    return postings_list 

def soundex(self):
    return 0


if __name__ == "__main__":
    #words=extract_poem() 
    print('to fill the void')
