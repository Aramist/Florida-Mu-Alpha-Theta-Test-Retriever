import json

from bs4 import BeautifulSoup as BS
import requests

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
	site = BS(CONTENT, 'html5lib')
	counter = 0
	for anchor in site.select('li > ul > li > a'):
		if len(list(anchor.children)) == 0:
			continue
		if anchor.span is not None:
			continue
		if anchor.b is not None:
			continue
		great_grandparent_text = anchor.parent.parent.parent.text
		if great_grandparent_text.lower() in ['individual', 'gemini', 'interschool test', 'individual tests', 'ciphering']:
			division = anchor.parent.text.lower().replace(':', '').strip()
			subject = great_grandparent_text.lower().replace(':', '').strip()
			url = anchor.attrs['href']
			variant = anchor.string.lower().strip()
		else:
			division = great_grandparent_text.lower().replace(':', '').strip()
			subject = anchor.parent.text.lower().replace(':', '').strip()
			url = anchor.attrs['href']
			variant = anchor.string.lower().strip()
		if len(division) > 30:
			continue
		if len(variant) > 30:
			continue
		if len(subject) > 30:
			continue
		obj = {'division': division, 'subject': subject, 'variant': variant, 'url': url}
		test_array.append(obj)
		counter += 1
	with open('output.json', 'w') as context:
		json.dump(test_array, context)
		print(counter)

if __name__ == '__main__':
	run()
