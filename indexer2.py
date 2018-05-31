import mysql.connector
from decimal import Decimal, getcontext
import sys
getcontext().prec = 5

if __name__ == "__main__":
        cnx = mysql.connector.connect(user='root', password='122BSQ',
                                      database='searchenginedb2')
        cursor = cnx.cursor()
        with open("data.txt", "r") as parsed_data:
            num_inserted = 0
            for line in parsed_data:
                num_inserted += 1
                split_line = line.split(",")
                insert_stmt = "INSERT INTO tokens(word, term_frequency, doc_id) VALUES(\"{}\", {}, \"{}\");".format(split_line[0], split_line[1], split_line[2])
            
                cursor.execute(insert_stmt)
                if(num_inserted % 1000 == 0):
                    cnx.commit()
                
                
                print "Percent complete: "+str((Decimal(num_inserted)/Decimal(5977899))*Decimal(100.0))+"%  \r",
                sys.stdout.flush()
        cursor.close()
        cnx.commit()
        cnx.close()
