from collections import defaultdict
import pickle


class Selector(object):

    def __init__(self, model):
        """
        model -- n-gram model.
        """
        # create structures
        print("Init Selector")
        self.probs = probs = defaultdict(dict)
        self.sorted_probs = sorted_probs = defaultdict(dict)
        self.n = n = model.n
        counts = model.counts
        # initialize structures
        for words in counts.keys():
            if len(words) == n:
                token = words[n-1]
                prev_tokens = words[:n-1]
                if prev_tokens not in probs:
                    probs.update({prev_tokens: defaultdict(dict)})
                    sorted_probs.update({prev_tokens: []})
                current_prob = model.cond_prob(token, list(prev_tokens))
                probs[prev_tokens].update({token: current_prob})
                sorted_probs[prev_tokens].append((token, current_prob))
                sorted_probs[prev_tokens] = sorted(sorted_probs[prev_tokens],
                                                   key=lambda x: (-x[1], x[0]))
        print("Finish Init")

    def choose(self, prev_tokens, candidates):
        assert len(prev_tokens) == self.n - 1
        winner = list(candidates)[0]
        pairs = self.sorted_probs.get(prev_tokens, [])
        if pairs != []:
            tokens, probs = zip(*pairs)
            max_prob = 0.0
            for i in range(len(tokens)):
                c_token = tokens[i]
                c_prob = probs[i]
                if c_token in candidates and c_prob > max_prob:
                    max_prob = probs[i]
                    winner = c_token
        return winner

# open model file
path = '/home/alangb/Escritorio/ngram2'
file = open(path, 'rb')
# load model file
model = pickle.load(file)
print("Finish pickle")
selector = Selector(model)
print("Finish Selector")
while 1:
    input1 = (input(),)
    input2 = input().split(' ')
    input2 = {x for x in input2}
    selection = selector.choose(input1, input2)
    print(selection)