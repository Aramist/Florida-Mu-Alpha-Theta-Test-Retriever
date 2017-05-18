import json
from os import path
from os import remove

json_path = path.abspath(path.join('..', 'resources/new.json'))

old, injection = None, None

with open(json_path, 'r') as context:
    old = json.load(context)

with open('processed.json', 'r') as context:
    injection = json.load(context)

assert not None in (old, injection)

def get_index(array, test_type):
    for num,obj in enumerate(array):
        if obj['type'] == test_type:
            return num
    return None

for test_obj in injection:
    division,subject,year,_type,url = test_obj['division'],test_obj['subject'],test_obj['year'],test_obj['type'],test_obj['url']
    if division not in old['nationals']:
        print('Could not find division {}, skipping.'.format(division))
        continue
    if str(year) not in old['nationals'][division]:
        old['nationals'][division][str(year)] = list()
    if _type == 'test':
        old['nationals'][division][str(year)].append({'type': subject, 'test': url})
    if _type == 'solutions':
        temp = old['nationals'][division][str(year)]
        index = get_index(temp, subject)
        if index is None:
            print('Could not find index for {}, skipping'.format(subject))
            continue
        temp[index]['solutions'] = url

with open('newer.json', 'w') as context:
    json.dump(old, context)
