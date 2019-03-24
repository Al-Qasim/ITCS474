'''[NAME]
    SAYED ALQASIM DHEYA ALI ABDULLA SALEM
    [I.D.]
    20147349
    [Assignment #01]
'''

import pickle #to dump data to files
import nltk #to tokenize words
from nltk.corpus import stopwords #to remove unnecessary words
import os #to access directories
import sys #to handle system arguments passed in CLI
from collections import defaultdict
import time #to be used by tqdm
from tqdm import tqdm #nice progress bar
 
def get_files(dir, suffix):
    '''[summary]
            Returns all the files in a folder ending with chosen suffix
    Arguments:
        dir {[string]} -- [directory to search in]
        suffix {[string]} -- [file extension to search for]
    
    Returns:
        [list] -- [contains names of files in current working directory]
    '''
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files



class invertedindex:
    '''[summary]
        holds indexing information of passed file
    '''

    def __init__(self):
        self.postings_list={} 
        
 
    def read_from_file(self, file_name):
        with open(file_name) as opened_file:
            for loc, line in enumerate(opened_file, 1):
                tokens=nltk.word_tokenize(line)
                stopWords = set(stopwords.words('english'))
                stopWords.update(['','<','>','0','1','2','3','4','5','6','7','8','9','.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
                filtered_tokens=[]
                for token in tokens:
                    if token not in stopWords: 
                        filtered_tokens.append(token)

                for token in filtered_tokens:
                    token= token.lower()
                    if token not in self.postings_list:
                        self.postings_list[token]={file_name:[loc]}
                    else:
                        self.postings_list[token][file_name].append(loc)    


def merge_ii(ii_list):
    '''[summary]
        merges matching postings list terms in different files
    Arguments:
        ii_list {[list]} -- [list of invertedindex type objects]
    
    Returns:
        [defaultdictionary] -- [dictionary of dictionaries]
    '''

    d = defaultdict(list)
    for myd in ii_dict: 
        for k, v in myd.postings_list.items(): 
            for k2,v2 in v.items():
                d[k].append({k2:v2})
    return d        



if __name__ == "__main__":
    '''[summary]
        When passed a folder name, list all files in directory and read through them
        while creating an inverted index object for each file. Return a merged dictionary containing 
        every enumerated file's postings list.

        Arguments:
            wdir {[string]} :
                a string of the path of the current working directory
            ii_dict {[list]} :
                a list to contain objects of type invertedindex
            listings {[list]} :
                a list to contain filenames in the target directory
            ii {[invertedindex]} : 
                temporary invertedindex type object used in a loop to describe the iteration item
            d {[dict]} : 
                a dictionary to hold all terms in all enumerated files as keys and a dictionary as value
                holding as key the filename of the file in which it appears and as value the postings list
    '''
    if len(sys.argv) > 1 and os.path.isdir(os.getcwd()+'\\'+sys.argv[1]):
    #os.chdir(r"C:\\Users\\AlQasim\\Documents\\Python\\Practice for IR lab01\\ShakePlays\\plays") #for direct testing 
        os.chdir(os.getcwd()+'\\'+sys.argv[1]) #for finalized code to use command line passed args
        #listings=os.listdir() #for testing
        wdir=os.getcwd() 
        listings= get_files(wdir, '.txt') 
        ii_dict=[] 
        for file_item in tqdm(listings): 
            print('\n\n\treading: '+file_item+': ')
            ii= invertedindex()
            ii.read_from_file(file_item)
            ii_dict.append(ii)
            print('\n')
                
        #ans=merge_ii(ii_dict) 
        d = merge_ii(ii_dict)
        print('\nCreating a master index file: "invertedIndex.idx"....\n')
        pickle.dump( d, open( "invertedIndex.idx", "wb"), 2) 
        print('\nSuccessfully created a master index file: "invertedIndex.idx"\n')
    else:
        print('\nUsage:\t python indexer.py <target_folder_name>\t- make sure target folder name exists.\n')
                                                 


