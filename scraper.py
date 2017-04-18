import requests
from bs4 import BeautifulSoup

PAGE = requests.get(r'http://www.mualphatheta.org/index.php?chapters/national-convention/past-tests')

def run():
    if PAGE.status_code != 200:
        raise Exception('Failed to grab page')
    soup = BeautifulSoup(PAGE.content, 'html.parser')
    print(soup.find_all('li'))

if __name__ == '__main__':
    run()
