#!/usr/bin/env python3

'''
	Dataloader for Universal Dependencies
'''

import io
import operator

class Dataloader():
    def __init__(self, filename, n_gram, unk_thres):
        self.filename = filename
        self.n_gram = n_gram
        self.sorted_types = {}
        self.type_list = []
        self.token_list = []
        self.BOS = '<BOS>'
        self.EOS = '<EOS>'
        self.UNK = '<UNK>'
        self.unk_thres = unk_thres
        self.total_sents = []


    def read_file(self):
        types = {}
        tokens = 0
        sents = []
        bos = True
        with open(self.filename, 'r') as in_file:
            # Store everything in a list
            for line in enumerate(in_file):
                row = line[1].strip().split()
                if len(row) > 0 and row[0] != "#":
                    if bos:
                        sents.append(self.BOS)
                    sents.append(row[1])
                    bos = False
                if len(row) == 0:
                    sents.append(self.EOS)
                    self.total_sents.append(sents)
                    sents = []
                    bos = True

            # Count based on n-gram
            if self.n_gram == 1:
                for sent in self.total_sents:
                    for word in sent:
                        self.type_list.append(word)
                        types[word] = types.get(word, 0) + 1
            elif self.n_gram == 2:
                for sent in self.total_sents:
                    for (w1, w2) in zip(sent[:-1], sent[1:]):
                        self.type_list.append((w1, w2))
                        types[(w1, w2)] = types.get((w1, w2), 0) + 1
                
        self.sorted_types = dict(sorted(types.items(), key=lambda kv: kv[1]))

        # Remove items having count less that UNK_THRESHOLD
        #self.final_types = {k:v for k,v in self.sorted_types.items() if v > self.unk_thres}
        #self.final_types[self.UNK] = 1

        self.token_list = set(self.type_list)
        return (self.total_sents, self.sorted_types, self.type_list, set(self.type_list))


    def print_statistics(self):
        self.total_sents, self.sorted_types, self.type_list, self.token_list = self.read_file()
        print("Total number of types = ", len(self.type_list))
        print("Total number of tokens = ", len(self.token_list))


    def get_types(self):
       return self.sorted_types

    def get_type_list(self):
       return self.type_list

    def get_token_list(self):
       return self.token_list
