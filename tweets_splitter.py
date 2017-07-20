from collections import defaultdict


class Tw_Splitter(object):
    def __init__(self, filepath):
        file = open(filepath, 'r')
        lines = file.read().split('\n')
        texts = dict()
        corrections = defaultdict(list)
        for line in lines:
            splitted = line.split('\t')
            if line[0] != '\t':
                tweet_id, tweet_text = splitted
                texts[tweet_id] = tweet_text
                current_id = tweet_id
            else:
                o, t, c = splitted[1].split(' ')
                corrections[current_id].append((o, t, c))
        self.texts = texts
        self.corrections = dict(corrections)
