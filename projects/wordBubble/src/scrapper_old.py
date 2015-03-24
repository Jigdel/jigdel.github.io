import requests
from lxml import etree
from io import StringIO
from lxml import html
#from lxml.etree import Element


root_url = 'http://www.savetibet.org'
index_url = root_url + '/resources/fact-sheets/self-immolations-by-tibetans/'


def get_names_age():
    response = requests.get(index_url)

    parser = etree.HTMLParser()
    
    # Parse and fix the broken html body into a tree
    tree = etree.parse(StringIO(response.text), parser)
    #result = etree.tostring(tree.getroot(), pretty_print=True, method="html")

    #print(result)
    #result = html.fromstring(response.text)
    '''
    # Perform xpaths on the tree
    h2 = tree.xpath('//h2', pretty_print=True)
    for element in h2:
        print('%s' % (element.text))
    
    #initializing dict with names as key
    names_list = soup.find_all('h2')
    for name in names_list:
        data[name.text] = {}
    '''    
    #xpath = '//h2/br'
    #xpath = '//div[@class="entry"]/p/b'
    xpath = '//h2 | //div[@class="entry"]/p/b'
    #xpath = '//div[@class="entry"]/p/child::text()'
    #xpath = '//div[@class="entry"]/p/child::node()'# | //div[@class="entry"]/p/child::text()'
    #xpath = '//div[@class="entry"]/child::*'
    dates = tree.xpath(xpath)
    #dates = result.xpath(xpath)
    #print(dates)
    print('*'*100)
    print('*'*100)
    print('*'*100)
    print('*'*100)
    print('*'*100)
    print('*'*100)
   # print(dates)
    '''
    for i in range(0,40):
        print(dates[i].text)
        
        try:
            print(dates[i].text)
        except(AttributeError):
            print(dates[i])
    '''    
    for element in dates:
        print('%s' % (element.text))
     
get_names_age()
