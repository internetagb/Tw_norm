import enchant
from collections import defaultdict
from nltk.tokenize import TweetTokenizer, sent_tokenize


class OOVpicker(object):

    def __init__(self):
        twt = TweetTokenizer()
        known_word = enchant.Dict("es_ES")
        OOV = defaultdict(lambda: defaultdict(list))
        file = open('Tweets/tweet2.txt', 'r')
        # split tweets by tweet separator
        tweets = file.read().split('---|||---|||---')
        for i, tweet in enumerate(tweets):
            # separate tweet sentences
            sents = sent_tokenize(tweet)
            # tokenize each sentence
            tokenized_sents = [twt.tokenize(sent) for sent in sents]
            for j, sent in enumerate(tokenized_sents):
                # enumerate sent to know word's position
                e = enumerate(sent)
                # list of (word, pos) where word is alphanumeric and not digit
                wp_list = [p[::-1] for p in e if (p[1].isalnum() and
                                                  not p[1].isdigit())]
                for word, pos in wp_list:
                    # check if word is In Vocabulary
                    if not known_word.check(word):
                        # add (word, pos) at j-th sent of i-th tweet
                        OOV[i][j].append((word, pos))
        self.OOV = dict(OOV)
