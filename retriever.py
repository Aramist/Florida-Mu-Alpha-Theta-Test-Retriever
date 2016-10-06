import json
import urllib
import os
import difflib

from PyPDF2 import PdfFileMerger as Merger

class Test:
    def __init__(self, data):
        """
        rawdata: The raw json array
        year: the year in which the test took place
        event: the event (states or regional:mon)
        type: individual, team, circles and polygons, the list goes on
        test: the url of the test
        solutions: the url of the test's solutions
        """
        self.rawdata = data
        self.year = int(data[0])
        self.event = data[1].replace(":","-")
        self.type = data[2]
        self.test = data[3]
        self.solutions = data[4]
        self.testname = str(self.year) + "_" + str(self.event) + "_" + str(self.type) + ".pdf"
        self.solutionsname = str(self.year) + "_" + str(self.event) + "_" + str(self.type) + "s.pdf"
class Subject:
    def __init__(self, data):
        self.rawdata = data
        self.name = data['aliases'][0]
        self.aliases = data["aliases"]#[1:len(data["aliases"])]
        self.tests = [Test(a) for a in data["tests"]]
        self.testdict = dict()
        for test in self.tests:
            if test.year in self.testdict.keys():
                self.testdict[test.year].append(test)
            else:
                self.testdict[test.year] = [test]
        self.cache_tests()
    def cache_tests(self):
        print('Caching Tests (' + self.name + ')...')
        if not os.path.exists(self.name+"/"):
            os.makedirs(self.name + "/")
        for t in self.tests:
            #print('Attempting: ' + str(t.year) + ' ' + t.event)
            if (not os.path.isfile(self.name + "/" + t.testname)) and t.test != '':
                testdata = urllib.request.urlopen(t.test).read()
                testfile = open(self.name + "/" + t.testname, "wb")
                testfile.write(testdata)
                testfile.close()
            if (not os.path.isfile(self.name + "/" + t.solutionsname)) and t.solutions != '':
                testdata = urllib.request.urlopen(t.solutions).read() if t.solutions != "" else b''
                testfile = open(self.name + "/" + t.solutionsname, "wb")
                testfile.write(testdata)
                testfile.close()
    def as_string(self):
        fdict = {"aliases": str(self.aliases), "name": str(self.name), "tests": str(len(self.tests))}
        return "{name}:\n\tAliases: {aliases}\n\tTests: {tests}".format(**fdict)
def merge_files(files, destination):
    if len(files) == 0:
        return None
    if len(files) == 1:
        return files[0]
    merger = Merger()
    for f in files:
        merger.append(f)
    merger.write(destination)
    merger.close()
def str_ratio(s1,s2):
    return difflib.SequenceMatcher(a=s1.lower(),b=s2.lower()).ratio()
def indexOf(s1,arr):
    for s in arr:
        if s1 in s:
            return arr.index(s)
    return None

def replace_subject(string, subject):
    for a in subject.aliases:
        if (' ' + a) in string:
            print('Found ' + a + ' in query, replacing...')
            return string.replace(a, subject.name)
    return string

def run_main():
    with open('tests.json', 'r') as loadfile:
        testdata = json.load(loadfile)
        subjects = [Subject(_s_) for _s_ in testdata.values()]
        to_download = []
        query = ' ' + input('query: ').strip()
        for s in subjects:
            query = replace_subject(query, s)
        query = query.replace(' tests ', ' ').replace(' test ', ' ').replace(' from ', ' ').replace(' with ', ' ').replace(',', '')
        query = query.strip()
        if 'and' in query:
            query = query.split(' and ')
        else:
            query = [query]
        print(str(query))
        for subquery in query:
            subquery = ' ' + subquery + ' '
            for s in subjects:
                if ' ' + s.name + ' ' in subquery:
                    numbers = [int(i) for i in subquery.split() if i.isdigit()]
                    if len(numbers) == 0:
                        if ' all ' in subquery:
                            print('All ' + s.name + 'tests requested')
                        continue
                    elif len(numbers) == 1:
                        #only one year
                        print(s.name + ' ' + str(numbers[0]))
                    elif len(numbers) == 2:
                        #range of years
                        print(s.name + ' ' + str([year for year in range(min(numbers), max(numbers) + 1)]))
                    else:
                        print(s.name + ' ' + str([year for year in numbers]))
                        pass
if __name__ == '__main__':
    run_main()
			
