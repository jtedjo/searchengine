import mysql.connector
import bs4
import re
import json

cnx = mysql.connector.connect(user='root', password='122BSQ',
                                  database='searchenginedb')
cursor = cnx.cursor()

with open("../../../Desktop/WEBPAGES_RAW/bookkeeping.json", "r") as json_data:
    bookkeepingJson = json.load(json_data)

search_stmt_str = "SELECT doc_id FROM tokens WHERE word LIKE %(search_term)s ORDER BY tfandidf LIMIT 10;"


while(True):
    input_query = raw_input("Enter a search term: ")
    #print(input_query)
    cursor.execute(search_stmt_str, {"search_term":"%"+input_query+"%"})
    results = cursor.fetchall()
    i = 0
    for result in results:
        print("Result " + str(i)+": "+bookkeepingJson[result[0]])
        i += 1


