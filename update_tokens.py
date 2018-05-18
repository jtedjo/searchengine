#UPDATE tokens as t set tfandidf=rs->idf*t.tf where t.word=rs->word;

import mysql.connector
import bs4
import re
import json

cnx = mysql.connector.connect(user='root', password='122BSQ',
                                  database='searchenginedb')

get_idf = cnx.cursor()
get_idf_str = "SELECT * from idf;"
get_idf.execute(get_idf_str)
results = get_idf.fetchall()

update_tfidf = cnx.cursor()
update_tfidf_str = "UPDATE tokens as t set tfandidf=%s*t.term_frequency where t.word=%s;"
for result in results:
    #print (result[1])
    update_tfidf.execute(update_tfidf_str, (result[1], result[0]))

cnx.commit() 
