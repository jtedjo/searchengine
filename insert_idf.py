import mysql.connector
import math
from decimal import Decimal, getcontext
import sys
getcontext().prec = 5


#SELECT COUNT(DISTINCT(doc_id) from tokens; <-- N
#SELECT word, COUNT(*) FROM tokens GROUP BY word; <-- rs
#INSERT INTO idf VALUES(rs->word, log(N/rs->count(*))

#cnx = mysql.connector.connect(user='user1', password='password', database="searchenginedb")

cnx = mysql.connector.connect(user='root', password='122BSQ', database="searchenginedb2")

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

num_inserted = 0
for result in results:
    insert_into_idf.execute(insert_into_idf_str, (result[0], str(math.log(N/int(result[1])))))
    
    num_inserted += 1
    if(num_inserted % 10000 == 0):
        cnx.commit()
    print "Percent complete: "+str((Decimal(num_inserted)/Decimal(5977899))*Decimal(100.0))+"%  \r",
                sys.stdout.flush()

insert_into_idf.close()
cnx.commit()
cnx.close()

