# from string import ascii_lowercase as lcase
import re
from oov_classifier import OOVclassifier


class PrimaryCandidates(object):

    def __init__(self, n):
        self.candidates = set()
        self.cf = OOVclassifier()
        self.n_errors = n

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
            check, nword = cf.check(c)
            if check:
                if nword != '':
                    c = nword
                candidates.add(c)
        self.candidates = self.candidates.union(candidates)

    def accent_mark(self, word):
        candidates = set()
        cf = self.cf
        n = len(word)
        vowels = 'aeiou'  # analizo äëïöüâêîôû???
        m_vowels = 'áéíóú'
        for i in range(n):
            cl = word[i]  # current letter
            if cl in vowels:
                m_index = vowels.index(cl)
                cand = word[:i] + m_vowels[m_index] + word[i+1:]
                check, nword = cf.check(cand)
                if check:
                    if nword != '':
                        cand = nword
                    candidates.add(cand)
        self.candidates = self.candidates.union(candidates)

    def check_sound(self, word):
        cands = self.candidates
        print(cands)
        len_w = len(word)
        for i in range(len_w-1):
            cl = word[i]
            nl = word[i+1]
            to_compare = [cand for cand in cands if len(cand) == len_w 
                                                    and cand[i] != cl]
            if cl == 'c' and nl in 'eiéí':
                for c in to_compare:
                    if c[i] not in 'Csz':
                        cands.discard(c)
            elif cl == 'c' and nl in 'aouáóú':
                for c in to_compare:
                    if c[i] not in 'Ck':
                        cands.discard(c)

            elif cl == 's' and nl in 'eiéí':
                for c in to_compare:
                    if c[i] not in 'Scz':
                        cands.discard(c)
            elif cl == 's' and nl in 'aouáóú':
                for c in to_compare:
                    if c[i] not in 'Szk':
                        cands.discard(c)

        self.candidates = cands

    def change_letters(self, word):
        candidates = set()
        change = {'v': ['b'], 'b': ['v'], 'c': ['s', 'z', 'k'],
                  's': ['c', 'z'], 'z': ['s', 'c'], 'll': ['y', 'sh'],
                  'y': ['ll', 'sh'], 'sh': ['ll', 'y'], 'x': ['ch'],
                  'h': [''], 'k': ['c', 'qu'], 'qu': ['k']}
        for i in range(len(word)):
            cl = word[i]  # current word
            pair = word[i:i+2]  # pair of letters for 'll' and 'sh' cases
            for new in change.get(cl, {}):
                cand1 = word[:i] + new + word[i+1:]
                candidates.add(cand1)
            for new in change.get(pair, {}):
                cand2 = word[:i] + new + word[i+2:]
                candidates.add(cand2)
        return candidates

    def spelling_error(self, word, n):
        temp_cand = {word}
        candidates = set()
        f_candidates = set()
        cf = self.cf
        for _ in range(n):
            changes = set()
            for w in temp_cand:
                words = self.change_letters(w)
                changes = changes.union(words)
            temp_cand = changes.copy()
            candidates = candidates.union(changes)
        for c in candidates:
            check, nword = cf.check(c)
            self.accent_mark(c)
            if check:
                if nword != '':
                    c = nword
                f_candidates.add(c)
        self.candidates = self.candidates.union(f_candidates)

    def char_rep(self, word):
        cf = self.cf
        rep2 = re.sub(r'(.)\1+', r'\1\1', word)
        no_rep = re.sub(r'(.)\1+', r'\1', word)
        candidates = {no_rep}
        rep2_tmp = list(rep2)
        for i in range(len(rep2_tmp) - 1):
            if rep2_tmp[i] == rep2_tmp[i+1]:
                rep2_tmp[i+1] = '-'
        for i in range(len(rep2) - 1):
            if rep2[i] == rep2[i+1]:
                cand_list = rep2_tmp[:i] + [rep2[i]] + rep2_tmp[i:]
                cand = ''.join(cand_list).replace('-', '')
                candidates.add(cand)
        for c in candidates:
            self.spelling_error(c, self.n_errors)
            self.accent_mark(c)
            check, nword = cf.check(c)
            if check:
                if nword != '':
                    c = nword
                self.candidates.add(c)

    def all(self, word):
        self.char_rep(word)
        self.upper_lower(word)
        self.spelling_error(word, self.n_errors)
        self.accent_mark(word)
        self.check_sound(word)

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
            check, nword = cf.check(cand)
            if check:
                if nword != '':
                    cand = nword
                candidates.add(cand)
            # swap i-th letter for i+1-th letter
            if i > 0:
                swap = word[i] + word[i-1]
                cand = word[:i-1] + swap + word[i+1:]
                check, nword = cf.check(cand)
                if check:
                    if nword != '':
                        cand = nword
                    candidates.add(cand)
            for x in abc:
                # replace i-th letter for x
                cand = word[:i] + x + word[i+1:]
                check, nword = cf.check(cand)
                if check:
                    if nword != '':
                        cand = nword
                    candidates.add(cand)
                # insert x in i-th position
                cand = word[:i] + x + word[i:]
                check, nword = cf.check(cand)
                if check:
                    if nword != '':
                        cand = nword
                    candidates.add(cand)
        for x in abc:
            # insert x at the end of word
            cand = word + x
            check, nword = cf.check(cand)
            if check:
                if nword != '':
                    cand = nword
                candidates.add(cand)
        self.candidates = self.candidates.union(candidates)

for _ in range(5):
    a = PrimaryCandidates(3)
    inp = input()
    a.all(inp)
    c = a.candidates
    print(c)
    if c == set():
        b = SecondaryCandidates()
        b.edit_distance(inp)
        print(b.candidates)
