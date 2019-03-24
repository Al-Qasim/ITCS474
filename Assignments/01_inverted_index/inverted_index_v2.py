import dill
import os
import re
from collections import defaultdict
 

def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    :param dir:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files

 
class invertedindex:
    '''[summary]
    ''' 

    def __init__(self):
        '''[summary]
        Initializes the postings list

        Arguments:
        postings_list {dictionary} -- [Contains all words] 
        '''

        self.postings_list={}

    def read_from_file(self, file_name):
        #files=get_files()
        #for file in files:
        with open(file_name) as opened_file:
            for loc, line in enumerate(opened_file, 1):
                for word in re.finditer("[^\s\d()<>;:,.?�!%\/\-_\[\]\"\n]+", line):
                    if type(word) == str: 
                        word= word.lower()
                    if word not in self.postings_list:
                        self.postings_list[word]={file_name:[loc]}
                    else:
                        self.postings_list[word][file_name].append(loc)    
 
def merge_ii(ii_list):
    d = defaultdict(list) 
    for myd in ii_dict:   
        for k, v in myd.postings_list.items(): 
            d[k].append(v)
    return d        

if __name__ == "__main__":
    """[summary]
    """
    os.chdir(r"C:\\Users\\AlQasim\\Documents\\Python\\Practice for IR lab01\\ShakePlays\\plays")
    wdir=os.getcwd() #same
    listings= get_files(wdir, '.txt')
    ii_dict=[]
    listk=[]
    for file in listings:
        ii= invertedindex() 
        ii.read_from_file(file) ; ii_dict.append(ii)
        
        #for word, inverted_index in ii.postings_list.items():
                #print('%s\t%d' %(word, len(inverted_index)))  
    res=merge_ii(ii_dict)
    #with open( "%s.idx" %('inverted_index'), "wb") as ofile:
        #dill.dump(ii_dict,ofile) 
                                                 


