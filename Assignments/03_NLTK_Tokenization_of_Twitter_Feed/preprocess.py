import csv
import nltk
from nltk.corpus import stopwords
import re
import sys

maxInt = sys.maxsize
stop_words = set(stopwords.words('english'))
tweets=[]
filtered_tweets=[]
while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

def extract_tweets(filename):
    global tweets
    with open(filename, 'r', encoding='utf-8') as csvfile:    
        csvreader= csv.reader(csvfile, delimiter=',', quotechar='|', dialect='excel')
        for line in csvreader:
            if len(line)<10: #we know that tweets are at the 11th column of the csv, some lines may not be that long and produce an error
                continue
            else:    
                tweets.append(line[10])
    return tweets

def preprocess_tweets(tweet_text):
    tokens=[]
    filtered_tokens=[]
    for msg in tweet_text:
        temp=nltk.word_tokenize(msg)
        tokens.extend(temp) 
    for token in tokens: 
        if re.match("[a-zA-Z\d]+", token) and not re.match("[a-zA-Z]{1}'[a-zA-Z]{1}", token) and len(token)>=3:
            filtered_tokens.append(str.lower(token)) 
    filtered_tokens_v2 = [w for w in filtered_tokens if not w in stop_words]
    #filtered_tweets.extend([w for w in tweets if not w in stop_words])
    return filtered_tokens_v2 
 
def stem_tokens(tokens_in):
    for token in tokens_in:
        if token[-3:] is "ies" and len(token[:-3]) >= 2:
            token= token[:-3] + "y"
        if token[-1] == "s" and len(token[:-1]) > 3:
            token= token[:-1]
        if len(token[:-3]) >= 4 and token[-3:] == "ing":
            token= token[:-4]
    return tokens_in            
if __name__ == "__main__":
    #print("to fill the void.")
    tweets_text= extract_tweets("Tweets.csv")
    tokens= preprocess_tweets(tweets_text)
    del tweets_text
    tokens_stemmed= stem_tokens(tokens) 
    del tokens
    #with open("Extracted_tweets.json")