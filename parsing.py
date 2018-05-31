import os
import errno
import bs4
import re
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numbers
from math import log
from decimal import Decimal, getcontext
import sys
getcontext().prec = 5

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def htmlFileContents(location):
    html_file = open(location, "r")
    content = html_file.read()
    html_file.close()
    return content

if __name__ == "__main__":
    with open ("../../../Desktop/WEBPAGES_RAW/bookkeeping.json", "r") as json_data:
        bookkeeping_json = json.load(json_data)

    #FILE READING PARTS
    num_read = 0
    for f in bookkeeping_json:
        num_read += 1
        print "Reading File: "+ f + "\tPercent complete: "+str((Decimal(num_read)/Decimal(len(bookkeeping_json)))*Decimal(100.0))+"%  \r", 
        sys.stdout.flush()
        
        content_soup = bs4.BeautifulSoup(htmlFileContents("../../../Desktop/WEBPAGES_RAW/"+f), "lxml")
        
        #this will read all the string contents within the HTML files and remove any unnecessary \n
        #string_list = ",".join([(strings).strip() for strings in filter(visible, content_soup.find_all(text=True)) if (strings != u"")])
        data_string = ",".join([(strings) for strings in filter(visible, content_soup.find_all(text=True)) if strings != u'\n'])
        
        #print(data_string.split(","))
        
        filename = "../../../Desktop/WEBPAGES_PARSED/"+f
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        
        with open(filename, "w") as f:
            f.write(data_string.encode('utf-8'))

