import json

processed = list()

with open('unprocessed.json', 'r') as context:
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
    if not (subject is None or test is None or url is None):
        processed.append({'subject': subject, 'type': test, 'url': url})
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
