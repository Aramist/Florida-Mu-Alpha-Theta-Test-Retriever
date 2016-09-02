import json
import urllib
from urllib import request
import os
from os import path
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
        self.year = data[0]
        self.event = data[1].replace(":","-")
        self.type = data[2]
        self.test = data[3]
        self.solutions = data[4]
        self.testname = str(self.year) + "_" + str(self.event) + "_" + str(self.type) + ".pdf"
        self.solutionsname = str(self.year) + "_" + str(self.event) + "_" + str(self.type) + "s.pdf"
class Subject:
    def __init__(self, data):
        self.rawdata = data
        self.name = data["aliases"][0]
        self.aliases = data["aliases"]#[1:len(data["aliases"])]
        self.tests = [Test(a) for a in data["tests"]]
        self.cache_tests()
    def cache_tests(self):
        if not os.path.exists(self.name+"/"):
            os.makedirs(self.name + "/")
        for t in self.tests:
            if not os.path.isfile(self.name + "/" + t.testname):
                testdata = urllib.request.urlopen(t.test).read() if t.test != "" else b''
                testfile = open(self.name + "/" + t.testname, "wb")
                testfile.write(testdata)
                testfile.close()
                testdata.close()
            if not os.path.isfile(self.name + "/" + t.solutionsname):
                testdata = urllib.request.urlopen(t.solutions).read() if t.solutions != "" else b''
                testfile = open(self.name + "/" + t.solutionsname, "wb")
                testfile.write(testdata)
                testfile.close()
                testdata.close()
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
testdata = json.loads(open("tests.json", "r").read())

calculusdata = testdata["calculus"]
precalculusdata = testdata["precalculus"]
algebradata = testdata["algebraII"]
geometrydata = testdata["geometry"]

calculus = Subject(calculusdata)
precalc = Subject(precalculusdata)
algebra = Subject(algebradata)
geometry = Subject(geometrydata)

subjects = [calculus,precalc,algebra,geometry]

print(calculus.as_string())
print(precalc.as_string())
print(algebra.as_string())
print(geometry.as_string())

class InterestObject:
    def __init__(self, desc = '', index = 0, data = None):
        self.description = desc
        self.index = index

def run():
    query = input("Request: ")
    sentence = query.split(" ")
    similarwords = {"test":["tests","quiz","quizzes"]}

    keywords = ['all','and','from','through', 'to', 'with', 'without']
    interest = []


    for word in sentence:
        length = len(sentence)
        index = sentence.index(word)
        if word.lower() in keywords:
            if word.lower() == "all":
                interest.append(InterestObject('all', index, sentence[index:]))
                continue
            if word.lower() == "and" and not index == length - 1:
                interest.append(InterestObject('and', index, sentence[:index]+sentence[index+1:]
                continue
            if index < length - 1 and not index == 0:
                interest.append(InterestObject(word.lower, index, (sentence[index-1],sentence[index+1])
            
            


    similaritydict = {s.name: max([str_ratio(w, a) for a in s.aliases for w in sentence]) for s in subjects}

    print("Similarity:")
    [print("\t" + a + ': ' + str(b)) for a,b in similaritydict.items()]

    for a,b in similaritydict.items():
        if(b >= 0.7):
            interest.append(InterestObject(a + " found in sentence", indexOf(a, sentence)))

    print("Interests")
    [print("\t" + str(i.index) + ": " + i.description) for i in interest]

    for n in interests:
        if 'comma' in n.description.lower():
        if 'all' in n.description.lower():
        if 'and' in n.description.lower():

if __name__ == '__main__':
    run()

			
