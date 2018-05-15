import mysql.connector
import bs4
import re
import json

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

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

cnx = mysql.connector.connect(user='root', password='122BSQ',
                                  database='searchenginedb')

with open("WEBPAGES_RAW/bookkeeping.json", "r") as json_data:
    bookkeepingJson = json.load(json_data)

#FILE READING PARTS
percentComplete = 0;
for f in bookkeepingJson:
        percentComplete += 1
        print "Percent complete: "+str((percentComplete/len(bookkeepingJson))*100)+"%      \r",
        folderNum = f.split("/")[0]
        fileNum = f.split("/")[1]
        docID = folderNum+"_"+fileNum

        #this is your own location of folder and files!!
        htmlFile = open("WEBPAGES_RAW/"+folderNum+"/"+fileNum, "r")
        content = htmlFile.read()


        contentSoup = bs4.BeautifulSoup(content, "lxml")
        data = contentSoup.findAll(text=True)
        result = filter(visible, data)
        #this will read all the string contents within the HTML files and remove any unnecessary \n
        stringList = [(strings).encode('utf-8') for strings in result]

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

        #printDescendingByVal(wordsDictionary)
        #TO DOS, write the local dictionary into the database

        keys = wordsDictionary.keys()
        values = wordsDictionary.values()



        cursor = cnx.cursor()
        
        insert_statement = "insert into TOKENS(word, term_frequency, doc_id, file_name) VALUES (%s, %s, %s, %s)"
        
        for key in wordsDictionary:
            if len(str(wordsDictionary.get(key))) < 100:
                cursor.execute(insert_statement, (key,wordsDictionary.get(key), docID, bookkeepingJson[f]))

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
