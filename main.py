from os import path
from oov_picker import OOVpicker
from oov_classifier import OOVclassifier
from variants_generation import PrimaryCandidates, SecondaryCandidates
# from candidate_selection import Selector

tweets_file = path.split(path.abspath(__file__))[0] + '/Tweets/tweet2.txt'

picker = OOVpicker(tweets_file)
classifier = OOVclassifier()
primary = PrimaryCandidates()
secondary = SecondaryCandidates()
# selector = Selector()
oovs = picker.OOV
correct = oovs.copy()

for i, tweet in oovs.items():
    for j, sent in tweet.items():
        correct[i][j] = []
        for word, pos in sent:
            class_number = classifier.classify(word)
            if class_number == 0:
                IVcandidates = primary.generate(word)
                if len(IVcandidates) == 0:
                    IVcandidates = secondary.generate(word)
                if len(IVcandidates) == 0:
                    correct_word = word
                else:
                    correct_word = selector.choose(IVcandidates)
            else:
                correct_word = word
            correct[i][j].append((correct_word, pos))

