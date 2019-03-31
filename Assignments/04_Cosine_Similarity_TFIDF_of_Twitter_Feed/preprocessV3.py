from tqdm import tqdm
import csv
import math

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

if __name__ == "__main__":
    tweets=extract_tweets("Tweets.csv") 
