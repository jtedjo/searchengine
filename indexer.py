import mysql.connector
import bs4
import re
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numbers
from math import log
from decimal import Decimal, getcontext
import sys
getcontext().prec = 5


#FUNCTION DEFINITIONS
def stringsInvalid(string):
    contain_letter = False;
    contain_number = False;
    for letter in string:
        if letter.isalpha():
            contain_letter = True
        if letter.isdigit():
            contain_number= True
            if letter == '0': #starts with 0, do not add as tokens
                return True
        if contain_letter and contain_number:
            return True
    if contain_number:
        if int(string) > 3000 or int(string) < 500:
            return True #if the number is not too large, 500-3000 expectations to be useful
    return False

def printDescendingByVal(dictionary):
    sorted_list = sorted(dictionary.iteritems(), key=lambda (k, v): (-v, k))
    for index,i in enumerate(sorted_list):
        print sorted_list[index][0], "-", sorted_list[index][1]

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def htmlFileContents(location):
    html_file = open(location, "r")
    content = html_file.read()
    html_file.close()
    return content

def getDictionary(string_list, stopwords):
    words_dictionary = {}
    words = "";

    for i, sentence in enumerate(string_list):
        #sometimes special character can screw up the input. AKA "more" and "more(special character) would not be "unique" by mysql
        sentence = re.sub(r'[^a-zA-Z0-9]', ' ', sentence)
        split_string = word_tokenize(sentence);
        for words in split_string:
            if words =='':
                pass
            if not stringsInvalid(words):
                words = words.lower();
                #check if number type, then anything greater than 3000 is prob uninformative
                if words not in stopwords and len(words) < 35 and len(words) >2:
                    if not words in words_dictionary:
                        words_dictionary[words] = 1
                    # otherwise increment
                    else:
                        words_dictionary[words] += 1
    return words_dictionary

### Main Function ###

if __name__ == "__main__":
    #cnx = mysql.connector.connect(user='user1', password='password',
    #                                  database='searchenginedb')

    cnx = mysql.connector.connect(user='root', password='122BSQ',
                                      database='searchenginedb')

    #with open("WEBPAGES_RAW/bookkeeping.json", "r") as json_data:
    #    bookkeepingJson = json.load(json_data)

    with open ("../../../Desktop/WEBPAGES_RAW/bookkeeping.json", "r") as json_data:
        bookkeeping_json = json.load(json_data)

    db_data_file = open("data.txt", "w")
    data_to_write = ""
    #FILE READING PARTS
    num_read = 0
    for f in bookkeeping_json:
            num_read += 1
            print "Reading File: "+ f + "\tPercent complete: "+str((Decimal(num_read)/Decimal(len(bookkeeping_json)))*Decimal(100.0))+"%  \r",
            sys.stdout.flush()
            
            #Write the tokens of the last file to data.txt and reset the data string
            if((num_read % 50) == 0):
                db_data_file.write(data_to_write)
                data_to_write = ""

            content_soup = bs4.BeautifulSoup(htmlFileContents("../../../Desktop/WEBPAGES_RAW/"+f), "lxml")
            
            #this will read all the string contents within the HTML files and remove any unnecessary \n
            string_list = [(strings) for strings in filter(visible, content_soup.find_all(text=True))]
            
            #Create a dictionary of the tokens and iterate over them, appending to the data string as we go
            words_dictionary = getDictionary(string_list, set(stopwords.words('English')))
            for key in words_dictionary:
                tf = Decimal(1+log(words_dictionary.get(key))) + Decimal(0.0) #Decimal + Decimal to display correct precision
                data_to_write += (key + "," + str(tf) + "," + f + "\n")
                    
    #Create insertion statement and execute
    insert_statement = "LOAD DATA LOCAL INFILE 'data.txt' INTO TABLE searchenginedb.tokens FIELDS TERMINATED BY ','  LINES STARTING BY '';"
    cursor = cnx.cursor() 
    cursor.execute(insert_statement)
    cnx.commit()
    
    #Clean up
    cursor.close()
    db_data_file.close()
    cnx.close()
