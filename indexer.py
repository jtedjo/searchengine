import mysql.connector
import bs4
import re
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numbers
from math import log
from decimal import Decimal
from decimal import getcontext
import sys
getcontext().prec = 5


#FUNCTION DEFINITIONS
def stringsInvalid(string):
    containLetter = False;
    containNumber = False;
    for letter in string:
        if letter.isalpha():
            containLetter = True
        if letter.isdigit():
            containNumber= True
            if letter == '0': #starts with 0, do not add as tokens
                return True
        if containLetter and containNumber:
            return True
    if containNumber:
        if int(string) > 3000 or int(string) < 500:
            return True #if the number is not too large, 500-3000 expectations to be useful
    return False


def printDescendingByVal(dict):
    sortedList = sorted(dict.iteritems(), key=lambda (k, v): (-v, k))
    for index,i in enumerate(sortedList):
        print sortedList[index][0], "-", sortedList[index][1]

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def readHTMLFile(f, location):
    htmlFile = open(location+f, "r")
    content = htmlFile.read()
    htmlFile.close()
    return content

def getDictionary(stringList, stopwords):
    wordsDictionary = {}
    words = "";

    for i, sentence in enumerate(stringList):
        #sometimes special character can screw up the input. AKA "more" and "more(special character) would not be "unique" by mysql
        sentence = re.sub(r'[^a-zA-Z0-9]', ' ', sentence)
        split_string = word_tokenize(sentence);
        for words in split_string:
            if words =='':
                pass
            if not stringsInvalid(words):
                words = words.lower();
                #check if number type, then anything greater than 3000 is prob uninformative
                if words not in stop_words and len(words) < 35 and len(words) >2:
                    if not words in wordsDictionary:
                        wordsDictionary[words] = 1
                    # otherwise increment
                    else:
                        wordsDictionary[words] += 1
    return wordsDictionary


#cnx = mysql.connector.connect(user='user1', password='password',
#                                  database='searchenginedb')

if __name__ == "__main__":
    cnx = mysql.connector.connect(user='root', password='122BSQ',
                                      database='searchenginedb')

    #with open("WEBPAGES_RAW/bookkeeping.json", "r") as json_data:
    #    bookkeepingJson = json.load(json_data)

    with open ("../../../Desktop/WEBPAGES_RAW/bookkeeping.json", "r") as json_data:
        bookkeepingJson = json.load(json_data)

    db_data = open("data.txt", "w")

    #FILE READING PARTS
    numRead = 0;
    for f in bookkeepingJson:
            numRead += 1
            print "Reading File: "+ f + "\tPercent complete: "+str((Decimal(numRead)/Decimal(len(bookkeepingJson)))*Decimal(100.0))+"%  \r",
            sys.stdout.flush()
            
            content = readHTMLFile(f, "../../../Desktop/WEBPAGES_RAW/")

            contentSoup = bs4.BeautifulSoup(content, "lxml")
            data = contentSoup.findAll(text=True)
            result = filter(visible, data)
            #this will read all the string contents within the HTML files and remove any unnecessary \n
            stringList = [(strings) for strings in result]
            stop_words = set(stopwords.words('English'))

            wordsDictionary = getDictionary(stringList, stop_words)
            
            keys = wordsDictionary.keys()
            values = wordsDictionary.values()
            cursor = cnx.cursor()
            
            for key in wordsDictionary:
                #divide by total amount of words within a file to normalize the term frequency
                #cursor.execute(insert_statement, (key, 1+log(wordsDictionary.get(key)), docID))
                tf = Decimal(1+log(wordsDictionary.get(key))) + Decimal(0.0) #Decimal + Decimal to display correct precision
                db_data.write(key + "," + str(tf) + "," + f + "\n")
                    

    insert_statement = "LOAD DATA LOCAL INFILE 'data.txt' INTO TABLE searchenginedb.tokens FIELDS TERMINATED BY ','  LINES STARTING BY '';"
    
    cursor.execute(insert_statement)
    cnx.commit()
    cursor.close()
    db_data.close()
    cnx.close()
