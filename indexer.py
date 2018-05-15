import mysql.connector
import bs4
import re

#FUNCTION DEFINITIONS
#prob not the best functions, but if you have better, feel free to change it!
def tokenize (str):
    #str_sub = re.sub(r'[^a-zA-Z0-9]', ' ', str)
    split_string = re.split(r'[^a-zA-Z0-9]', str)
    return split_string

def printDescendingByVal(dict):
    sortedList = sorted(dict.iteritems(), key=lambda (k, v): (-v, k))
    for index,i in enumerate(sortedList):
        print sortedList[index][0], "-", sortedList[index][1]


#FILE READING PARTS
folder = 1;
file = 2;
docID = folder *1000 + file;

#this is your own location of folder and files!!
file = open("C:\Users\Jonathan Tedjo\Desktop\UCI\Spring 2018\Information Retrieval\Homework\Homework3\WEBPAGES\WEBPAGES_RAW\\%d\\%d" %(folder, file), "r")
content = file.read()


contentSoup = bs4.BeautifulSoup(content, "lxml")

#this will read all the string contents within the HTML files and remove any unnecessary \n
stringList = [(strings).encode('utf-8') for strings in contentSoup.findAll(text=True)]

wordsDictionary ={}
words = "";

for i, sentence in enumerate(stringList):
    # result = re.sub(r'[^a-zA-Z0-9]', ' ', sentence)
    # split_string = result.split(" ")
    split_string = tokenize(sentence);
    for words in split_string:
        words = words.lower();
        if words == '': #beautiful soup have 'u' to indicate unicode, need to be passed
            pass
        # if it does not exist in dictionary, initialize
        elif not words in wordsDictionary:
            wordsDictionary[words] = 1
        # otherwise increment
        else:
            wordsDictionary[words] += 1

printDescendingByVal(wordsDictionary)
#TO DOS, write the local dictionary into the database

keys = wordsDictionary.keys()
values = wordsDictionary.values()


cnx = mysql.connector.connect(user='user1', password='password',
                              database='searchenginedb')


cursor = cnx.cursor()

insert_statement = """ insert into TOKENS(word, term_frequency, doc_id) VALUES (%s, %s, %s)"""

for key in wordsDictionary:
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




file.close()
cursor.close()
cnx.close()