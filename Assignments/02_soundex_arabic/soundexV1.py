import sys
import os
import re
import pyarabic.araby as araby
sys.stdout.reconfigure(encoding='utf-8')

def extract_poem():
    """[summary]
    might not be using it
    Returns:
        [type] -- [description]
        dict    --  postings lists of arabic words
    """

    postings_list={}
    tokens=[]
    with open("short story.txt", encoding='utf-8') as ofile:
        
        for loc, line in enumerate(ofile, 1):
            
            
            words= araby.tokenize(araby.strip_tashkeel(line))
            tokens.extend(words)
            for word in words:    
                if(araby.is_tatweel(word)):
                    word= araby.strip_tatweel(word)
                
                # if word not in postings_list: 
                    
                #     postings_list[word]=[loc] 
                
                # else:
                    
                #     postings_list[word].append(loc) 
            
    #return postings_list 
    return tokens 

def soundex(sentence):
    '''
    - blanks and and spaces are deleted,
    - long vowels are deleted,
    - if two adjacent letters are identical, only one of the two is
        kept,
    - to each word’s letter are associated two numbers:

        1. the first one corresponds to the letter’s main category’s
        code. It is represented by an integer N of two bits, such as N
        E={0, 1, 2}.
        
        2. the second one corresponds to the letter’s sub-category’s
        code. It is represented by an integer n of four bits, such as:
        n SE= {0,...,10}.
        Thus :
            Given a word w, w=w 1 ...w n .
                w=w- {blanks and long vowels}=w’ 1 ... w’ n .
                f(w)=f(w’)=f(w’ 1 ... w’ n )=N 1 n 1 ... N n n n =X.
                The phonetic code generated X, can be used as a hash key
                for classifying and indexing purposes.
    
    Returns:
        [type] -- [description]
    '''
    words= araby.tokenize(sentence)
    for word in words:
        if type(word) != str:
           word= word.decode('utf-8')
        else:
           word= word.encode('utf-8')
        loc=0
        for i in word[0:]:
           if araby.is_tatweel(i):
               word= araby.strip_tatweel(word)
           if loc < len(word) and loc != 0 and re.match("[\u0627\u064a\u0648]", str(word[loc])):
               word= word[:loc] + word[loc+1:]
           if loc < len(word) and re.match("[\u0640]", str(word[loc])):
               word= word[:loc] + word[loc+1:]
           loc+=1   
    print(words)             
  

if __name__ == "__main__":
    print("to fill the void")
    pos=extract_poem()
    soundex(pos[-29])
