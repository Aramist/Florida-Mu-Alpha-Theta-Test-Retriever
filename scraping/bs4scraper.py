import requests
from bs4 import BeautifulSoup as BS

PAGE_URL = r'http://www.mualphatheta.org/index.php?chapters/national-convention/past-tests'
REQUEST = requests.get(PAGE_URL)
CONTENT = REQUEST.text

def filter(tag):
	if tag.name != u'a':
		return False
	if u'href' not in tag.attrs:
		return False
	

def run():
	test_array = list()
	site = BS(CONTENT, 'html.parser')
	for anchor in site.select('li > ul > li > a'):
		great_grandparent_text = a.parent.parent.parent.text
		if great_grandparent_text.lower() in ['individual', 'gemini', 'interschool test', 'individual tests', 'ciphering']:
			division = anchor.parent.text.lower()
			subject = great_grandparent_text.lower()
		else:
			division = great_grandparent_text.lower()