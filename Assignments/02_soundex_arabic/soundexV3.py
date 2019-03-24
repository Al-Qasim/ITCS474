'''[NAME]
    SAYED ALQASIM DHEYA ALI ABDULLA SALEM
    [I.D.]
    20147349
    [Assignment #02]
'''

import re
import json
import sys
import io
import os
import pyarabic.araby as araby

'''

    dental {list} --category of letters
    velar {list} -- category of letters
    labial {list} -- category of letters
    word_db {dict} -- dictionary to hold encodings and corresponding terms
    
'''

dental= [araby.QAF, araby.KAF, araby.SHEEN, araby.JEEM, araby.YEH,
         araby.DAD, araby.LAM, araby.REH, araby.TEH, araby.DAL,
         araby.TAH, araby.SEEN, araby.ZAIN, araby.SAD, araby.THEH,
         araby.THAL, araby.ZAH, araby.NOON]

velar= [araby.ALEF_HAMZA_ABOVE, araby.HEH, araby.HAH, araby.AIN, araby.GHAIN,
        araby.KHAH]

labial= [araby.FEH, araby.BEH, araby.MEEM, araby.WAW]                 

word_db={}
def soundex(surname):
    '''
    encodes passed argument and saves results in a file.
    
    Arguments:
        surname {str} -- [string to encode]
    '''

    global dental, velar, labial, word_db 
    outstring= ""
    for i in range (0, len(surname)):
            nextletter = surname[i]
            if nextletter in dental:
                '''
                Find if the letter belongs to the dental letters category.
                '''

                outstring = outstring + '00'
                if nextletter == dental[0]:
                    outstring = outstring + '0000'
                elif nextletter == dental[1]:
                    outstring = outstring + '0001'
                elif nextletter == dental[2] or nextletter == dental[3] or nextletter == dental[4]:
                    outstring = outstring + '0010'
                elif nextletter == dental[5]:
                    outstring = outstring + '0011'
                elif nextletter == dental[6]:
                    outstring = outstring + '0100'
                elif nextletter == dental[7]:
                    outstring = outstring + '0101'
                elif nextletter == dental[8] or nextletter == dental[9] or nextletter == dental[10]:
                    outstring = outstring + '0110'
                elif nextletter == dental[11] or nextletter == dental[12] or nextletter == dental[13]:
                    outstring = outstring + '0111'
                elif nextletter == dental[14] or nextletter == dental[15] or nextletter == dental[16]:
                    outstring = outstring + '1000'
                elif nextletter == dental[17]:
                    outstring = outstring + '1001'

            elif nextletter in velar:
                '''
                Find if the letter belongs to the velar letters category.
                '''
                outstring = outstring + '01'
                if nextletter == velar[0]  or nextletter == velar[1]:
                    outstring = outstring + '0000'
                elif nextletter == velar[2] or nextletter == velar[3]:
                    outstring = outstring + '0001'
                elif nextletter == velar[4] or nextletter == velar[5]:
                    outstring = outstring + '0010'

            elif nextletter in labial:
                '''
                Find if the letter belongs to the labial letters category.
                '''
                outstring = outstring + '10'
                if nextletter == labial[0] or nextletter == labial[1] or nextletter == labial[2]:
                    outstring = outstring + '0000'
                elif nextletter == labial[3]:
                    outstring = outstring + '0001'
    if outstring != "":
        ''' sometimes empty strings crawl in here and create errors '''
        if str(int(outstring, 2)) not in word_db.keys() and not re.match("[\d]", surname):
            word_db[str(int(outstring, 2))]= [surname[::-1]]
            print("code: "+str(int(outstring, 2)))
            with io.open("result.txt", 'a', encoding='utf-8') as res:
                for i in word_db[str(int(outstring, 2))]: 
                    res.write("code: "+str(int(outstring, 2)) + ", word: "+surname[::-1]+"\n")
        else: 
            if surname[::-1] not in word_db[str(int(outstring, 2))]:
                word_db[str(int(outstring, 2))].append(surname[::-1])
                with io.open("result.txt", 'a', encoding='utf-8') as res:
                    for i in word_db[str(int(outstring, 2))]:
                        res.write("code: "+str(int(outstring, 2)) + ", word: "+surname[::-1]+"\n")



if __name__ == "__main__":
    tokens=[]
    temptokens=[]
    if len(sys.argv) > 1:    
        ''' work if user provides an input filename '''
        path= os.getcwd()+"\\"+sys.argv[1]
        if os.path.exists(path):
            ''' if file is valid continue '''
            with io.open(sys.argv[1], encoding="utf-8") as doc:
                for line in doc: 
                    ''' tokenized lines in input file '''
                    temptokens.extend(araby.tokenize(line))
                for token in temptokens:
                    ''' attempt at removing long vowels from tokens (did not work as anticipated)'''
                    #if len(token) >= 2 and araby.is_arabicrange(token):
                        #token= re.sub("[\u0621-\u064a\ufb50-\ufdff\ufe70-\ufefc]+(\u0627)[\u0621-\u064a\ufb50-\ufdff\ufe70-\ufefc]+", '', token)
                        #token= token.replace('\u0621', '\u0627') 
                        #token= token.replace('\u0621\u0621', '\u0627') 
                        #token= re.sub("[\u0648$]", '', token) 
                        #token= re.sub("[\u064a$]", '', token)
                        #print(len(token))
                    if len(token) >= 2 and araby.is_arabicrange(token):
                        ''' remove any non-arabic letters '''
                        tokens.append(araby.strip_tashkeel(araby.strip_tatweel(token)))                    
                del temptokens #free space
                for token in tokens:
                    soundex(token[::-1])  #encode tokens in list
                del tokens # free space
                ''' inform user about success of the program and output file name. '''
                print("\n\n Successfully finished encoding the input term(s). Check \"result.txt\"")
        else:
            ''' inform user that the supplied file name is invalid '''
            print("invalid filename.")
    else:
        ''' inform user of correct usage of the program '''  
        print("Usage:\t python\tsoundexV3.py\t\t\"<input_file_name>\" ")
    