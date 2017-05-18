import json
import re
import string

processed = list()

with open('scraped.json', 'r') as context:
    raw = json.load(context)

assert type(raw) == type([])

def process_subject(param):
    return param.replace('\n', '').replace(': ', '').replace('-', '').replace('&', 'and').lower().strip()

def process_type(param):
    temp = param
    if '&' in temp:
        temp = 'Test'
    temp = temp.lower()
    return temp

def process_url(param):
    temp = param
    if temp[:6] != 'http:/':
        temp =  r'http://www.mualphatheta.org' + temp
    return temp

def process(subject, test, url):
    subject = process_subject(subject)
    test = process_type(test)
    url = process_url(url)
    if ' theta ' in ' {} '.format(subject):
        division = 'theta'
    elif ' alpha ' in ' {} '.format(subject):
        division = 'alpha'
    elif ' mu ' in ' {} '.format(subject):
        division = 'mu'
    elif url.count('theta') > 2:
        division = 'theta'
    elif url.count('alpha') > 2:
        division = 'alpha'
    elif url.count('mu') > 2:
        division = 'mu'
    else:
        print('could not determine division for {}'.format(subject))
        return
    matches = re.findall(r'/\d+', url)
    year = 0
    if len(matches) > 0:
        year = int(matches[0][1:])
    if year < 1990 or year > 2020:
        print('year {} out of range'.format(year))
        return
    if not (subject is None or test is None or url is None):
        processed.append({'division': division, 'subject': subject, 'year': year, 'type': test, 'url': url})
def run():
    for value in raw:
        toextend = [dict()]
        content_length = min(len(value['type']), len(value['url']))
        if content_length > 3:
            continue
        for i in range(content_length):
            process(value['subject'], value['type'][i], value['url'][i])
    with open('processed.json', 'w') as context:
        json.dump(processed, context)


if __name__ == '__main__':
    run()
