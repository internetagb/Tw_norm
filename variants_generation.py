# from string import ascii_lowercase as lcase
from oov_classifier import OOVclassifier


class PrimaryCandidates(object):

    def __init__(self):
        self.candidates = set()
        self.cf = OOVclassifier()

    def upper_lower(self, word):
        candidates = set()
        cf = self.cf
        cands = []
        if word.islower():
            cands = [word.upper(), word.title()]
        elif word.isupper():
            cands = [word.lower(), word.title()]
        elif word.istitle():
            cands = [word.lower(), word.upper()]
        else:
            cands = [word.lower(), word.upper(), word.title()]
        for c in cands:
            if cf.dictionary_lookup(c) or cf.affix_check(c):
                candidates.add(c)
        self.candidates = self.candidates.union(candidates)

    def accent_mark(self, word):
        candidates = set()
        cf = self.cf
        n = len(word)
        vowels = 'aeiou' #  analizo äëïöüâêîôû???
        m_vowels = 'áéíóú'
        for i in range(n):
            cl = word[i]  # current letter
            if cl in vowels:
                m_index = vowels.index(cl)
                cand = word[:i] + m_vowels[m_index] + word[i+1:]
                if cf.check(cand):
                    candidates.add(cand)
        self.candidates = self.candidates.union(candidates)

    def spelling_error(self, word):
        # analiza solo un error
        # ejemplo: kaza me da caza y kasa (casa no)
        candidates = set()
        cf = self.cf
        change = {'v': ['b'], 'b': ['v'], 'c': ['s', 'z', 'k'], 's': ['c', 'z'],
                  'z': ['s', 'c'], 'll': ['y', 'sh'], 'y': ['ll', 'sh'],
                  'sh': ['ll', 'y'], 'x': ['ch'], 'h': [''],
                  'k':['c','qu']}
        for i in range(len(word)):
            cl = word[i]  # current word
            pair = word[i:i+2]  # pair of letters for 'll' and 'sh' cases
            for new in change.get(cl, {}):
                cand1 = word[:i] + new + word[i+1:]
                if cf.check(cand1):
                    candidates.add(cand1)
            for new in change.get(pair, {}):
                cand2 = word[:i] + new + word[i+2:]
                if cf.check(cand2):
                    candidates.add(cand2)
        self.candidates = self.candidates.union(candidates)

    def all(self, word):
        self.upper_lower(word)
        self.spelling_error(word)
        self.accent_mark(word)


class SecondaryCandidates(object):
    def __init__(self):
        self.candidates = set()
        self.cf = OOVclassifier()

    def edit_distance(self, word):
        candidates = set()
        cf = self.cf
        n = len(word)
        abc = 'abcdefghijklmnñopqrstuvwxyzáéíóú'
        # abc = lcase[:14] + 'ñ' + lcase[14:] + 'áéíóú'
        for i in range(n):
            # delete i-th letter
            cand = word[:i] + word[i+1:]
            if cf.check(cand):
                candidates.add(cand)
            # swap i-th letter for i+1-th letter
            if i > 0:
                swap = word[i] + word[i-1]
                cand = word[:i-1] + swap + word[i+1:]
                if cf.check(cand):
                    candidates.add(cand)
            for x in abc:
                # replace i-th letter for x
                cand = word[:i] + x + word[i+1:]
                if cf.check(cand):
                    candidates.add(cand)
                # insert x in i-th position
                cand = word[:i] + x + word[i:]
                if cf.check(cand):
                    candidates.add(cand)
        for x in abc:
            # insert x at the end of word
            cand = word + x
            if cf.check(cand):
                candidates.add(cand)
        self.candidates = self.candidates.union(candidates)
