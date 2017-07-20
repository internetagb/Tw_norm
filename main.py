from os import path
from oov_picker import OOVpicker
from oov_classifier import OOVclassifier
from variants_generation import PrimaryCandidates, SecondaryCandidates
from candidate_selection import Selector

tweets_file = path.split(path.abspath(__file__))[0] + '/Tweets/tweet2.txt'

picker = OOVpicker(tweets_file)
classifier = OOVclassifier()
primary = PrimaryCandidates()
secondary = SecondaryCandidates()
selector = Selector()
oovs = picker.OOV
correct = defaultdict(dict)

for tweet_id, tweet in oovs.items():
    for j, sent in tweet.items():  # j is number of the sent
        correct[tweet_id][j] = []
        for word, pos in sent:
            # class_number = primary.cf.classify(word)
            class_number = classifier.classify(word)
            # if class is variant
            if class_number == 0:
                IVcandidates = primary.generate(word)
                # if no primary candidates generated
                if len(IVcandidates) == 0:
                    IVcandidates = secondary.generate(word)
                # if no secondary candidates generated
                if len(IVcandidates) == 0:
                    class_number = 1
                    correct_word = word
                else:
                    correct_word = selector.choose(IVcandidates)
            # if class is correct or NoES
            else:
                correct_word = word
            correct[tweet_id][j].append((class_number, correct_word, pos))

# dejo el classifier o uso el del primario?
# agregué class number to correct
# que hago ahora. Armo tweets corregidos y palabras corregidas?
# uso tokenizer de language modeling?
# abreviaturas con o sin punto
# para nombres, hago split y que tomen parte??
# cambio en dic look y affix
# busqueda en ND??
# check sound....la h?? ejemplo Shanto da santo
# spelling if termina con b, c
# como hago lo del sms.txt
# en secondary agrego algo de reps
# hago memoria de candidatos?