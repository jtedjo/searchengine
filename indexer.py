import mysql.connector
import bs4

file = open("WEBPAGES/WEBPAGES_RAW/0/1", "r")
content = file.read()
contentSoup = bs4.BeautifulSoup(content, "lxml")
outputLinks = [link['href'] for link in contentSoup('a') if 'href' in link.attrs]
print outputLinks

cnx = mysql.connector.connect(user='user1', password='password',
                              database='searchenginedb')


cursor = cnx.cursor()

file.close()
cursor.close()
cnx.close()