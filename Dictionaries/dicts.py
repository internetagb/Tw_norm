from os import path
from collections import defaultdict


class dicts(object):

    def __init__(self):

        filepath = path.split(path.abspath(__file__))[0] + '/txt/'

        # create normalization dict
        d = defaultdict(str)
        normfile = open(filepath + 'sms.txt', 'r')
        lines = normfile.read().split('\n')
        for use, correct in [line.split(':') for line in lines]:
            d[use] = correct
        normfile.close()

        # create dict of all verbs (infinitive + conjugated)
        v = defaultdict(set)
        verbsfile = open(filepath + 'verbs.txt', 'r')
        lines = verbsfile.read().split('\n')
        for word in lines:
            v[word[0]].add(word)
        verbsfile.close()

        # create dict of spanish names
        n = defaultdict(set)
        namesfile = open(filepath + 'proper_nouns.txt', 'r')
        lines = namesfile.read().split('\n')
        for word in lines:
            n[word[0]].add(word)
        namesfile.close()

        # create dict of spanish lemario
        l = defaultdict(set)
        lemfile = open(filepath + 'lemario.txt', 'r')
        lines = lemfile.read().split('\n')
        for word in lines:
            l[word[0]].add(word)
        lemfile.close()

        # set class attributes
        self.norm = dict(d)
        self.verbs = dict(v)
        self.lemario = dict(l)
        self.names = dict(n)