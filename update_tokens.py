import mysql.connector
from decimal import Decimal, getcontext
import sys
getcontext().prec = 5

cnx = mysql.connector.connect(user='user1', password='password',
                                  database='searchenginedb')

get_idf = cnx.cursor()
get_idf_str = "SELECT * from idf;"
get_idf.execute(get_idf_str)
results = get_idf.fetchall()
get_idf.close()

update_tfidf = cnx.cursor()
update_tfidf_str = "UPDATE tokens as t set tfandidf=%s*t.term_frequency where t.word=%s;"
num_updated = 0
for result in results:
    update_tfidf.execute(update_tfidf_str, (result[1], result[0]))
    num_updated += 1
    if(num_updated % 10000 == 0):
        cnx.commit()
    print "Percent complete: "+str((Decimal(num_updated)/Decimal(5977899))*Decimal(100.0))+"%  \r",
    sys.stdout.flush()

cnx.commit()
update_tfidf.close()
cnx.close()
