'''[NAME]
    SAYED ALQASIM DHEYA ALI ABDULLA SALEM
    [I.D.]
    20147349
    [Assignment #04]
'''
#--import necessary modules--
import math # simplifies the application of mathmatical formulas
import csv # to read through csv files
import nltk  # Natural Language Processing Toolkit for tokenization and stemming
from nltk.corpus import stopwords
import re # for regular expressions
import sys  # to check arguments passed to the program through CLI and use them
import json # to dump result
import os # to use OS filesystem related functions
from tqdm import tqdm # for user experience this adds loading bars

#-- declare important local variables
maxInt = sys.maxsize
stop_words = set(stopwords.words('english'))

def extract_tweets(filename):
    '''[summary]
            Extract tweet column from all lines in comma separated values (csv) file and return a list of these tweets
    Arguments:
        filename {string} -- name of the csv file of the used data set
    
    Returns:
        [list] -- A list of tweets
    '''

    tweets=[]
    with open(filename, 'r', encoding='utf-8') as csvfile:    
        csvreader= csv.reader(csvfile, delimiter=',', quotechar='|', dialect='excel')
        print("\nExtracting tweets...\n")# message for user to know progress
        for line in tqdm(csvreader):
            if len(line)<10: #we know that tweets are at the 11th column of the csv, some lines may not be that long and produce an error
                continue
            else:    
                tweets.append(line[10])
    return tweets

def preprocess_tweets(tweet_text):
    '''[summary]
            Tokenize every element of the input tweet list and return a list comprising them
    Arguments:
        tweet_text {list} -- 
    
    Returns:
        list -- A list of tokens from the input list of tweets
    '''

    global stop_words
    tokens=[]
    filtered_tokens=[] 
    print("\nTokenizing tweets...\n") # message for user to know progress
    for msg in tqdm(tweet_text):
        temp=nltk.word_tokenize(msg)
        tokens.extend(temp) 
    print("\nNormalizing tokens...\n") # message for user to know progress
    for token in tqdm(tokens):  
        if re.match("[a-zA-Z\d]+", token) and not re.match("[a-zA-Z]{1}'[a-zA-Z]{1}", token) and len(token)>=3:
            filtered_tokens.append(str.lower(token)) 
    filtered_tokens_v2 = [w for w in filtered_tokens if not w in stop_words]
    return filtered_tokens_v2 
 
def stem_tokens(tokens_in):
    '''[summary]
            return a list of stemmed tokens
    Arguments:
        tokens_in {list} -- Input list of tokens
    
    Returns:
        [list] -- A list of stemmed tokens
    '''
    ps= nltk.PorterStemmer()  # create obj of PorterStemmer
    stemmed= [] # create empty list for stemmed tokens
    print("\nStemming tokens...\n") # message for user to know progress
    stemmed= [ps.stem(w) for w in tqdm(tokens_in)] # return using list comprehension the stemmed form of every token
    return stemmed  



if __name__ == "__main__":
    '''[summary]
        When passed a folder name, list all files in directory and read through them
        while creating an inverted index object for each file. Return a merged dictionary containing 
        every enumerated file's postings list.

        Arguments:
            tweets_text {list} :
                a list of full tweets extracted from the csv in question
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
    try:
        if len(sys.argv) > 1:
            if os.path.exists(sys.argv[1]):
                if not sys.argv[1].endswith(".csv"):
                    print("\nThe file specified is not comma separated values!\n")
                else:
                    tweets_text= extract_tweets(sys.argv[1])
                    tokens= preprocess_tweets(tweets_text)
                    del tweets_text # delete full tweets to save memory
                    tokens_stemmed= stem_tokens(tokens) # stem tokens using porter's algorithm
                    del tokens # delete unstemmed tokens to save memory
                    with open('result.json', 'w') as output:
                        json.dump(tokens_stemmed, output)
                    print("\nProgram was successful. Check results.json file in program directory.\n")        
            else:
                print('\nError:\t The filename entered is wrong or file does not exist.\n')  
                print('\nUsage:\t python preprocess.py <target_csv_filename>\t- make sure target file exists name exists.\n')                
        else:
            print('\nDesclaimer:\t This program was written considering the .\n Other data sets may give incorrect results.')  
            print('\nUsage:\t python preprocess.py <target_csv_filename>\t- make sure target file exists name exists.\n')  
    except:
        print("Fatal Error! Make sure to use the tweets from the airline sentiment analysis data set!")            