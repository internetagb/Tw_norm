from Dictionaries.dicts import dicts

dicts = dicts()
norm = dicts.norm
names = dicts.names
lemario = dicts.lemario
verbs = dicts.verbs
alldicts = [lemario, verbs, names]

file = open('tweet.txt', 'r')
new = open('correct_tweet.txt', 'w')
OOV = set()
for line in file.read().split('\n'):
    for word in line.split(' '):
        p = word[0]
        b = False
        for dic in alldicts:
            b = b or word in dic.get(p, {})
            if b:
                break
        if not b:
            OOV.add(word)
            if word in norm.keys():
                line = line.replace(word, norm[word])

    new.write(line+'\n')
new.write('\nOOV = '+ str(OOV))
file.close()
new.close()
