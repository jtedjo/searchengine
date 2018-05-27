import mysql.connector
import bs4
import re
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import operator

def queryWordList(strings):
    stop_words = set(stopwords.words('English'))
    words_list = strings.lower().split(" ")
    filtered_list = [word for word in words_list if not word in stop_words]
    return filtered_list


cnx = mysql.connector.connect(user='user1', password='password',
                                  database='searchenginedb')
cursor = cnx.cursor()

with open("WEBPAGES_RAW/bookkeeping.json", "r") as json_data:
    bookkeepingJson = json.load(json_data)

search_stmt_str = "SELECT doc_id, tfandidf FROM tokens WHERE word LIKE %(search_term)s ORDER BY tfandidf DESC LIMIT 100;"


while(True):
    document_dictionary = {}
    input_query = raw_input("Enter a search term: ")
    #print(input_query)
    input_list = queryWordList(input_query)
    for query in input_list:
        cursor.execute(search_stmt_str, {"search_term":query})
        results = cursor.fetchall()
        i = 0
        for result in results:
            doc_id, tfandidf = result
            if not doc_id in document_dictionary:
                document_dictionary[doc_id] = tfandidf
            # otherwise increment
            else:
                document_dictionary[doc_id] += tfandidf

    sorted_dictionary = sorted(document_dictionary.items(), key=operator.itemgetter(1), reverse = True)
    for i in range(10):
        print("Result " + str(i)+": "+bookkeepingJson[sorted_dictionary[i][0]])


