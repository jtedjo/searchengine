import mysql.connector
import bs4
import re
import json
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#SELECT COUNT(DISTINCT(doc_id) from tokens; <-- N
#SELECT word, COUNT(*) FROM tokens GROUP BY word; <-- rs
#INSERT INTO idf VALUES(rs->word, log(N/rs->count(*))

cnx = mysql.connector.connect(user='user1', password='password', database="searchenginedb")
#cnx = mysql.connector.connect(user='root', password='122BSQ', database="searchenginedb")

num_docs = cnx.cursor()
num_docs_str = "SELECT COUNT(DISTINCT(doc_id)) from tokens;"
num_docs.execute(num_docs_str)

N = num_docs.fetchall()[0][0]

token_doc_count = cnx.cursor()
token_doc_str = "SELECT word, COUNT(*) FROM tokens GROUP BY word;"
token_doc_count.execute(token_doc_str)

results = token_doc_count.fetchall()

insert_into_idf = cnx.cursor()
insert_into_idf_str = "INSERT INTO idf(word, counts) VALUES(%s, %s);"

for result in results:
    print(result[0] + " " + str(math.log(N/int(result[1]))))
    insert_into_idf.execute(insert_into_idf_str, (result[0], str(math.log(N/int(result[1])))))

cnx.commit()

