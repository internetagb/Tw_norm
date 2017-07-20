from os import path
from tweets_splitter import Tw_Splitter
from oov_picker import OOVpicker
from collections import defaultdict

tweets_dir = path.split(path.abspath(__file__))[0]
tweets_dir += '/Tweets/tweet-norm-dev100_annotated.txt'
splitter = Tw_Splitter(tweets_dir)
picker = OOVpicker(splitter.texts)

oov = defaultdict(set)
for tid in picker.OOV.keys():
    for l in picker.OOV[tid].values():
        for x in l:
            oov[tid].add(x[0])

m, k, j, ig, df = 0, 0, 0, 0, 0
no_pick = dict()
for tid in splitter.corrections.keys():
    a = oov[tid]
    b = {x[0] for x in splitter.corrections[tid]}
    result = (a == b)
    if not result:
        print(tid)
        if len(b) > len(a):
            print("PICKER FAIL")
            no_pick[tid] = (a^b)
            if (a^b) != (b - a):
                df += 1
                for _ in range(50):
                    print("DIFFERENCE ERROR")
                print("Causing problems:", no_pick[tid])
            k += 1
        if len(b) < len(a):
            j += 1
        print("Suggest:", a)
        print("Gold:", b)
        print('\n')
        m += 1
    else:
        ig += 1

print("Iguales:", ig)
print("Distintos:", m)
print("Picker fail:", k)
print("Picker extra:", j)
print("Difference error:", df)
