import requests
from bs4 import BeautifulSoup

PAGE = requests.get(r'http://www.mualphatheta.org/index.php?chapters/national-convention/past-tests')

def run():
    if PAGE.status_code != 200:
        raise Exception('Failed to grab page')
    soup = BeautifulSoup(PAGE.content, 'html.parser')
    links = list(soup.find_all('h2'))
    for year_header in links:
        year = list(year_header.children)[0].get('name')[5:]
        top_level_tests = list(year_header.next_sibling.children)[0:4]
        topic_tests = list(year_header.next_sibling.children)[4]
        for top_level in top_level_tests:
            

if __name__ == '__main__':
    run()
