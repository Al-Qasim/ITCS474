import csv
import nltk
import re
import numpy
from sklearn.feature_extraction.text import CountVectorizer
import json
import sys
import os
import io
from tqdm import tqdm

corp={}
tfidf_collection={}
def extract_tweets(filename):
    '''[summary]
            Extract tweet column from all lines in comma separated values (csv) file and return a list of these tweets
    Arguments:
        filename {string} -- name of the csv file of the used data set
    
    Returns:
        [list] -- A list of tweets
    '''

    #tweets_set=()
    tweets=[]
    with open(filename, 'r', encoding='utf-8') as csvfile:    
        csvreader= csv.reader(csvfile, delimiter=',', quotechar='|', dialect='excel')
        print("\nExtracting tweets...\n")# message for user to know progress
        for line in csvreader:
            if len(line)<10: #we know that tweets are at the 11th column of the csv, some lines may not be that long and produce an error
                continue
            else:    
                tweets.append(line[10])
    #tweets_set=(tweets)
    return tweets



def Index_Corpus():
    global corp
    print("\n it seems that the tftidf collection and/or the doc list do(es) not exist in the current directory, it/they will have to be indexed before begining: \n")
    data_set = extract_tweets("Tweets2.csv")
    listt=tokenize_by_doc(data_set) 
    corp=data_sett(listt) 
    print("\nDoc Frequency Calculation:\n")
    for token in tqdm(corp):    
        doc_frequencies= doc_frequency(token, corp, data_set)
    print("\nInverse Doc Frequency Calculation:\n")
    for token in corp:    
        idf_collection= inverse_doc_freq(token, corp, len(data_set))
    with io.open("tfidf_collection.json", 'w', encoding='utf-8') as jsonfile:
        json.dump(idf_collection, jsonfile, sort_keys = True, indent = 4, ensure_ascii = False)
    with io.open("Extracted_Tweets.json", 'w', encoding='utf-8') as jsonfile:
        json.dump(data_set, jsonfile, indent = 4, ensure_ascii = False)
    del doc_frequencies, idf_collection    


def tokenize_by_doc(tweets):
    docID=1
    list_of_docs=[]
    print("\nTerm Freq Calculation:\n")
    for tweet in tqdm(tweets):
        tokens= nltk.word_tokenize(tweet.lower())
        dict_tokens={token:0 for token in tokens if re.match("^[a-zA-Z]+$", token)}
        for token in tokens:
            if token not in dict_tokens.keys() and re.match("^[a-zA-Z]+$", token):    
                dict_tokens[token]=[(tweet.count(token)/len(tokens),docID)]
            elif token in dict_tokens.keys() and re.match("^[a-zA-Z]+$", token):
                dict_tokens.update({token:[(tweet.count(token)/len(tokens),docID)]})
               
        list_of_docs.append(dict_tokens)
        docID+=1
    return list_of_docs    
 
def data_sett(listw): 
    corpus={}
    for w in listw:
        corpus.update(w)
    return corpus    

def doc_frequency(term, corpus, docs):
    doc_freq=0
    for doc in docs:
        if doc.lower().count(term):
            doc_freq+=1
    pair=corpus[term][0]
    tuple_new=(pair[0], pair[1],doc_freq)
    corpus.update({term: [tuple_new]})
    #print(term+": ")
    #print(corpus[term])  
    return corpus  

def doc_frequency_q(term, docs):
    doc_freq=0
    for doc in docs:
        if doc.lower().count(term):
            doc_freq+=1
    return doc_freq  

def inverse_doc_freq(term, corpus, collection_size):
    idf=  numpy.log10(collection_size/corpus[term][0][2])
    tuple_old=corpus[term][0]
    tuple_new= tuple_old + (idf,)
    corpus.update({term: [tuple_new]})
    #print(term+": ")
    #print(corpus[term])  
    return corpus
    
def inverse_doc_freq_q(term, corpus, collection_size):
    tuple_old=tuple(corpus[term][0])
    #print(tuple_old)
    corpus.update({term: [tuple_old]}) 
    return corpus

def TFIDF_calc(query, tweets):
    global corp, tfidf_collection
    idf_query=0    
    tfidf=0
    for w in nltk.word_tokenize(query_sample.lower()):
        if corp == {}:
            corp= tfidf_collection 
        for token in corp.keys():
            if re.match("[a-zA-Z]*"+w+"[a-zA-Z]*", token):
                idf_query= inverse_doc_freq_q(w, corp, len(tweets))
                """ print(q_frequency)
                print(idf_query[w][0][0])
                print(idf_query[w][0][3])
                 """
                tfidf= idf_query[token][0][0] * idf_query[token][0][3]
                tuple_old=tuple(corp[token][0])
                tuple_new= tuple_old + (tfidf,)
                corp.update({token: [tuple_new]})
                print("\n"+token+": \n")
                #print("\n"+str(corp[token])+"\n")
                print("\n"+str(tweets[idf_query[token][0][1]-1])+"\n")



if __name__ == "__main__":
    if(len(sys.argv)>1):
            if type(sys.argv[1])==str and len(sys.argv[1])>0:
                if os.path.exists("tfidf_collection.json") and os.stat("tfidf_collection.json").st_size != 0:
                    print("\nfound the tfidf collection, your query will be processed momentarily:\n")
                    if os.path.exists("Extracted_Tweets.json") and os.stat("Extracted_Tweets.json").st_size != 0:
                        with open("tfidf_collection.json", 'r', encoding='utf-8') as jsonfile:
                            tfidf_collection= json.load(jsonfile)  
                        with open("Extracted_Tweets.json", 'r', encoding='utf-8') as jsonfile:  
                            data_set= json.load(jsonfile)
                        query=sys.argv[1]
                        query_sample="happy"
                        TFIDF_calc(query_sample, data_set)
                    else:
                        
                        Index_Corpus()
                else:
                    Index_Corpus()
    else:
        print('\nDesclaimer:\t This program was written considering the Airline Sentiment Analysis data set.\n \t\tOther data sets may give incorrect results.')  
        print('\nUsage:\t python TFIDFV2.py <Query_inbetween_quotes>\t- make sure target file exists name exists.\n') 
    """ try:
        if(len(sys.argv)>1):
            if type(sys.argv[1])==str and len(sys.argv[1])>0:
                if os.path.exists("tfidf_collection.json") and os.stat("tfidf_collection.json").st_size != 0:
                    print("\nfound the tfidf collection, your query will be processed momentarily:\n")
                    if os.path.exists("Extracted_Tweets.json") and os.stat("Extracted_Tweets.json").st_size != 0:
                        tfidf_collection= json.load("tfidf_collection.json", encoding='utf-8')    
                        data_set= json.load("Extracted_Tweets.json", encoding='utf-8')
                        query=sys.argv[1]
                        query_sample="was happy"
                        TFIDF_calc(query_sample, data_set)
                    else:
                        
                        Index_Corpus()
                else:
                    Index_Corpus()
        else:
                print('\nDesclaimer:\t This program was written considering the Airline Sentiment Analysis data set.\n \t\tOther data sets may give incorrect results.')  
                print('\nUsage:\t python TFIDFV2.py <Query_inbetween_quotes>\t- make sure target file exists name exists.\n')  
     except:
        print("\nFatal Error! Make sure to use the tweets from the airline sentiment analysis data set!\n")    """             

""" 
data_set = extract_tweets("Tweets2.csv")
vectorizer = CountVectorizer(stop_words='english')

vectorizer.fit_transform(data_set)
print(vectorizer)

smatrix = vectorizer.transform(data_set)
print(smatrix)

from sklearn.feature_extraction.text import TfidfTransformer
tfidf = TfidfTransformer() #by default norm = "l2"
tfidf.fit(smatrix)
print("IDF:", tfidf.idf_)  """