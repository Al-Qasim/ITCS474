import csv
import nltk
import sys
import math
from nltk.corpus import stopwords
from tqdm import tqdm
import re
#-- declare important local variables
maxInt = sys.maxsize
stop_words = set(stopwords.words('english'))
tfidf_dict={}
index= {}
doc_freq={}
num_of_docs=0
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


def index_terms(tweet, docID):
    global index
    tokens= nltk.word_tokenize(tweet)
    #print("\nIndexing Terms\n")
    for token in tokens:
        if re.match("^[a-zA-Z]+$", token):
            if token not in index.keys():
                index[token]={} 
                index[token].update({""+str(docID): tweet.count(token)})
            else:
                index[token].update({""+str(docID): tweet.count(token)})   

def find_doc_freq(word):
    global doc_freq, index
    doc_freq[word]=len(index[word]) 

def tfidf(term, tweets):
    global doc_freq, index, num_of_docs, tfidf_dict
    appearance=[key for key in index[term].keys()]
    tf=0
    for doc_id in appearance:
            tf=index[term].get(doc_id)
    if tf > 0:    
        #print("Got tf>0")
        tfidf_dict[term]= 1+math.log(tf) * math.log(num_of_docs/1+doc_freq[term])
    else: 
        tfidf_dict[term]=0 

if __name__ == "__main__":
    extracted_tweets= extract_tweets("Tweets.csv")
    num_of_docs=len(extracted_tweets)  
    doc_id=1
    for tweet in extracted_tweets:
        index_terms(tweet.lower(), doc_id)
        doc_id+= 1
    #del extracted_tweets  
    #print("\nClaculating Document frequencies:\n")
    for token in index.keys():
        find_doc_freq(token)   
    #print("\nClaculating TF-IDfs:\n")
    for token in index.keys():
        tfidf(token, extracted_tweets)  
    del extracted_tweets        