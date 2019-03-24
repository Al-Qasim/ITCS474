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

dental= [araby.QAF, araby.KAF, araby.SHEEN, araby.JEEM, araby.YEH,
         araby.DAD, araby.LAM, araby.REH, araby.TEH, araby.DAL,
         araby.TAH, araby.SEEN, araby.ZAIN, araby.SAD, araby.THEH,
         araby.THAL, araby.ZAH, araby.NOON]

velar= [araby.ALEF_HAMZA_ABOVE, araby.HEH, araby.HAH, araby.AIN, araby.GHAIN,
        araby.KHAH]

labial= [araby.FEH, araby.BEH, araby.MEEM, araby.WAW]                 

word_db={}
def soundex(surname):
    global dental, velar, labial, word_db
    outstring= ""
    for i in range (0, len(surname)):
            nextletter = surname[i]
            if nextletter in dental:
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
                outstring = outstring + '01'
                if nextletter == velar[0]  or nextletter == velar[1]:
                    outstring = outstring + '0000'
                elif nextletter == velar[2] or nextletter == velar[3]:
                    outstring = outstring + '0001'
                elif nextletter == velar[4] or nextletter == velar[5]:
                    outstring = outstring + '0010'

            elif nextletter in labial:
                outstring = outstring + '10'
                if nextletter == labial[0] or nextletter == labial[1] or nextletter == labial[2]:
                    outstring = outstring + '0000'
                elif nextletter == labial[3]:
                    outstring = outstring + '0001'
    if outstring != "":
        #print(len(outstring))
        if str(int(outstring, 2)) not in word_db.keys() and not re.match("[\d]", surname):
            word_db[str(int(outstring, 2))]= [surname[::-1]]
        else:
            if surname[::-1] not in word_db[str(int(outstring, 2))]:
                word_db[str(int(outstring, 2))].append(surname[::-1])
        #print("\t\t\t\t\t\t"+surname[::-1])
        #print("\tencoded word (binary): "+ outstring)
        #print("\tencoded word (dec): "+ str(int(outstring, 2)))



if __name__ == "__main__":
    #print("to fill the void")
    tokens=[]
    temptokens=[]
    """ 
    if len(sys.argv) > 1:
        cdir= os.getcwd()+"\\"+sys.argv[1]
        print(cdir)
        if os.path.exists(cdir):
            with io.open(sys.argv[1], encoding="utf-8") as doc:
                for line in doc:
                    tokens.extend(araby.tokenize(line))
        for token in tokens:
            if len(token) > 1:
                soundex(token)    """   
    with io.open("nouns.masdarv2.txt", encoding="utf-8") as doc:
        for line in doc:
            temptokens.extend(araby.tokenize(line))
        for token in temptokens:  
            if len(token) >= 2 and araby.is_arabicrange(token):
               token= token.replace("\u0627", '')
               token= token.replace('\u0621', '\u0627') 
               token= token.replace('\u0621\u0621', '\u0627') 
               token= token.replace("\u0648", '') 
               token= token.replace("\u064a", '')
               if len(token) >= 2:
                tokens.append(araby.strip_tashkeel(araby.strip_tatweel(token)))                    
        del temptokens
        for token in tokens:
            soundex(token[::-1])  
        del tokens                        
    soundex(araby.MEEM+araby.DAL+araby.KAF) #sample word, backwards because it is processed LTR
    soundex(araby.BEH+araby.TEH+araby.KAF) #sample word, backwards because it is processed LTR
    soundex(araby.FEH+araby.TEH+araby.KAF) #sample word, backwards because it is processed LTR
    soundex(araby.FEH+araby.NOON+araby.ALEF_HAMZA_ABOVE) #sample word, backwards because it is processed LTR
    with open("db.json", 'w') as database:
        database.write(json.dumps(word_db))