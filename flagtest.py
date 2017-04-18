from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

SUBJECTS = 'precalculus,calculus,algebra II,geometry,statistics,theta,alpha,mu,\
conic sections,circles'.split(',')

class FlagFinder(object):

    def __init__(self):
        pass

    def get_flags(self, string):
        string = ' {} '.format(string.strip().lower())
        sentence = string.split(' ')
        for sub in SUBJECTS:
            