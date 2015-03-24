#!/usr/bin/env python

"""Word frequency calculated for text files in input folder"""

from collections import Counter
from collections import OrderedDict
import sys
import os
import re
import urllib.request
from timeit import default_timer
from bs4 import BeautifulSoup
import cgi

__author__ = "Jigdel K"
__copyright__ = "See license"
__credits__ = ["Python for Data Analysis - Wes Mckinney", "Intro to Data Science - Udacity", "Stack Overflow members"]
__license__ = "MIT License"
__version__ = "1.0"
__maintainer__ = "Jigdel K"
__email__ = "jigdel.k@gmail.com"
__status__ = "Always improving"


def cleanFile(file):
    """Strip/split/combine the html page """
    # split the words (starting with letters, numbers ignored per FAQ)
    file = re.split(r'[^A-Za-z]', file)
    return(file)

def writeFile(dict, file_name):
    """Write word frequency list to wc_output.txt"""
    # write in utf-8 to avoid future decoding issues (easier to parse)
    with codecs.open(file_name, 'w', 'utf-8') as f_out:
        for k, v in dict.items():
            # tab separated as mentioned in FAQs
            f_out.write("{}\t{} \n".format(k,v))
            
def main():
    # url - get url from site form
    root_url = 'http://www.savetibet.org'

    output_file = './output/word_freq.tsv'
    
    form = cgi.FieldStorage()
    root_url = form.getValue('websiteAddress')
    # index_url = root_url + '/resources/fact-sheets/self-immolations-by-tibetans/'

    # Unblock common non-browser user agents strings
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    #url = "http://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers"
    headers={'User-Agent':user_agent,}

    # The assembled request
    request=urllib.request.Request(root_url, None, headers)
    
    # use BeautifulSoup to scrape the page
    with urllib.request.urlopen(request) as url:
        page = url.read()
        soup = BeautifulSoup(page)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    # get text
    text = soup.get_text()

    # word freq counter declaration
    word_freq = Counter()
    word_freq.update(cleanFile(text))

    remove_words = ["the", "to", "for", "a", "", "an", "on", "and", "in", "from", "http", "as"]
    
    """
    # remove words
    for word in word_freq.keys():
        if word in remove_words:
            del word_freq[word]
    """
    # Beautiful Code - Raymond Hettinger
    word_freq = {k : word_freq[k] for k in word_freq if not k in remove_words}

    # write to wc_result.txt
    writeFile(word_freq, output_file)
    
    # plot it :)
    # pass the array/list to charts.js
    
# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    main()

"""
def clean_texts(element):
    #Clean page of any javascripts or html tags 
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True
"""
