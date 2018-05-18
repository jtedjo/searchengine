import mysql.connector
import bs4
import re
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numbers


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


cnx = mysql.connector.connect(user='user1', password='password',
                                  database='searchenginedb')


#cnx = mysql.connector.connect(user='root', password='122BSQ',
#                                  database='searchenginedb')


with open("WEBPAGES_RAW/bookkeeping.json", "r") as json_data:
    bookkeepingJson = json.load(json_data)

#FILE READING PARTS
percentComplete = 0;
for f in bookkeepingJson:
        #percentComplete += 1
        #print "Percent complete: "+str((percentComplete/len(bookkeepingJson))*100)+"%      \r",
        folderNum = f.split("/")[0]
        fileNum = f.split("/")[1]
        docID = folderNum+"/"+fileNum
        print ("folder ID = " + docID)

        #this is your own location of folder and files!!
        htmlFile = open("WEBPAGES_RAW/"+folderNum+"/"+fileNum, "r")
        content = htmlFile.read()


        contentSoup = bs4.BeautifulSoup(content, "lxml")
        data = contentSoup.findAll(text=True)
        result = filter(visible, data)
        #this will read all the string contents within the HTML files and remove any unnecessary \n
        stringList = [(strings) for strings in result]
        stop_words = set(stopwords.words('English'))

        wordsDictionary ={}
        words = "";

        for i, sentence in enumerate(stringList):
            # result = re.sub(r'[^a-zA-Z0-9]', ' ', sentence)
            # split_string = result.split(" ")
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

        #printDescendingByVal(wordsDictionary)
        #TO DOS, write the local dictionary into the database

        keys = wordsDictionary.keys()
        values = wordsDictionary.values()



        cursor = cnx.cursor()
        
        insert_statement = "insert into TOKENS(word, term_frequency, doc_id) VALUES (%s, %s, %s)"
        
        for key in wordsDictionary:
            #divide by total amount of words within a file to normalize the term frequency
            cursor.execute(insert_statement, (key,wordsDictionary.get(key), docID))

        cnx.commit()
        #try:
         #   cursor.executemany(insert_statement, keys, values)
         #   cnx.commit()
        #except:
        #    cnx.rollback()

        #MYSQL:
        #tokens(word VARCHAR(250), term_frequency INT, doc_id INT, tfandidf INT)
        #idf(word VARCHAR(250), counts DECIMAL(6,2)) probably should rename counts to idfscore

        #testers code for MYSQL insertions
        #cursor.execute("Insert into tokens VALUES ('Darkness', 52  , 2, null)")

        htmlFile.close()
        cursor.close()
cnx.close()
