import pickle
from nltk.data import load


class Selector(object):

    def __init__(self):
        """
        model -- n-gram model.
        """
        path = '/home/alangb/Escritorio/bo3'
        # open model file
        file = open(path, 'rb')
        # load model file
        model = pickle.load(file)

        self.model = model
        self.n = model.n

    def choose(self, prev_tokens, candidates):
        """
            return the most probable next token for prev_tokens
        """
        model = self.model
        cands = list(candidates)
        probs = [model.cond_prob(c, prev_tokens) for c in cands]
        max_prob = max(probs)
        index = probs.index(max_prob)
        winner = cands[index]

        return winner

    def prev_tokens(self, pair, tokenized):
        n = self.n
        index = tokenized.index(pair)
        prev_tokens = tuple()
        for i in range(index - n + 1, index):
            if i < 0:
                prev_tokens += ('<s>',)
            else:
                prev_tokens += (tokenized[i][0],)
        return prev_tokens


# if __name__ == '__main__':
#     selector = Selector(model)

#     for _ in range(5):
#         inp1 = input("ingrese prev tokens: ")
#         prev_tokens = tuple(inp1.split(','))
#         inp2 = input("ingrese candidates: ")
#         candidates = set(inp2.split(','))
#         print(selector.choose(prev_tokens, candidates))
