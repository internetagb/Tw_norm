import enchant
from Dictionaries.dicts import dicts
from treetaggerwrapper import TreeTagger, make_tags

class OOVclassifier(object):

    def __init__(self):
        dictionaries = dicts()
        path = '/home/alangb/TWPP'
        self.ND = dictionaries.norm.copy()
        self.SD = dictionaries.lemario.copy()
        # self.VD = dictionaries.verbs.copy()
        self.PND = dictionaries.names.copy()
        self.tagger = TreeTagger(TAGLANG='es', TAGDIR=path)

    def dictionary_lookup(self, word):
        if word == '':
            result = False
            nd = ''
        else:
            key = word[0]
            nd = ''
            if word in self.ND.keys():
                result = True
                nd = self.ND[word]
            else:
                result = (word in self.SD.get(key, {})
                          or word in self.PND.get(key, {})
                          # or word in self.VD.get(key, {})
                          )
        return (result, nd)

    def affix_check(self, word):
        result = False
        if word.islower() or word.istitle():
            lemma = make_tags(self.tagger.tag_text(word))[0].lemma
            result = self.dictionary_lookup(lemma)[0]
        # print("el lema de", word, "es:", lemma)
        return result
        # return False

    def check(self, word):
        d_lookup = self.dictionary_lookup(word)
        return (d_lookup[0] or self.affix_check(word), d_lookup[1])

    def check_NoES(self, word):
        d = enchant.Dict("en_EN")
        return d.check(word)

    def classify(self, word):
        if self.check(word):
            result = 1
        elif self.NoES:
            result = 2
        else:
            result = 0
        return result