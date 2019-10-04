#!/usr/bin/env python3

'''
	Maximum Likelihood Estimation
	Unigram or Bigram
'''

import numpy as np
from utils.dataloader import Dataloader

# DataModule to load data
class DataModule():
    def __init__(self, train_file, dev_file, n_gram, unk_threshold, unk_val):
        self.train_file = train_file
        self.dev_file = dev_file
        self.n_gram = n_gram
        self.unk_threshold = unk_threshold
        self.unk_val = unk_val
        
        self.train_dl = Dataloader(self.train_file, self.n_gram, self.unk_threshold)
        self.dev_dl = Dataloader(self.dev_file, self.n_gram, self.unk_threshold)
        self.t_sents, self.t_items, self.t_types, self.t_tokens = self.train_dl.read_file()
        self.d_sents, self.d_items, self.d_types, self.d_tokens = self.dev_dl.read_file()

        self.t_prob = {}
        self.d_prob = {}

        # Subtracting two because it contains <BOS> and <EOS>
        self.t_total_types = len(self.t_types) - 2
        self.d_total_types = len(self.d_types) - 2

        self.t_total_tokens = len(self.t_tokens) - 2
        self.d_total_tokens = len(self.d_tokens) - 2
    

    # Print general stats of the dataset    
    def print_stat(self):
        print("**********DATA STATISTICS********")
        print("Length of type list in train_file", self.t_total_types)
        print("Length of type list in dev_file", self.d_total_types)
        print("Length of token list in train_file", self.t_total_tokens)
        print("Length of token list in dev_file", self.d_total_tokens)
        print("OOV = ", self.t_total_tokens - self.d_total_tokens)
        

# Maximum Likelihood Estimation LM
class MLE(DataModule):
    def __init__(self, train_file, dev_file, n_gram, unk_threshold, unk_val):
        super().__init__(train_file, dev_file, n_gram, unk_threshold, unk_val)
        self.t_prob = {}
        self.d_prob = {}

    # prob(X) = count(X)/count(total_types)
    def train(self):
        self.t_prob = {k: v/self.t_total_types for k, v in self.t_items.items()}
        return self.t_prob

    # Calculate Perplexity
    def eval(self):
        prob_list = []
        for k,v in self.d_items.items():
            self.d_prob[k] = self.t_prob.get(k, self.unk_val)
            prob_list.append(self.d_prob[k])
        return np.exp(-np.mean(np.log(prob_list)))
                

# Laplace LM
class Laplace(DataModule):
    def __init__(self, train_file, dev_file, n_gram, unk_threshold, unk_val, lambda_val):
        super().__init__(train_file, dev_file, n_gram, unk_threshold, unk_val)
        self.lambda_val = lambda_val
        self.t_total_length = self.t_total_types + (self.t_total_tokens * lambda_val)
        
    # prob(X) = count(X)/count(total_types) + lambda
    def train(self):
        self.t_prob = {k: (v + self.lambda_val)/self.t_total_length for k, v in self.t_items.items()}
        return self.t_prob

    # Calculate Perplexity
    def eval(self):
        prob_list = []
        for k,v in self.d_items.items():
            self.d_prob[k] = self.t_prob.get(k, self.unk_val + self.lambda_val)
            prob_list.append(self.d_prob[k])
        return np.exp(-np.mean(np.log(prob_list)))



# Backoff LM
class Backoff(DataModule):
    def __init__(self, train_file, dev_file, n_gram, unk_threshold, unk_val, lambda_val, discount, norm_const):
        super().__init__(train_file, dev_file, n_gram, unk_threshold, unk_val)
        self.lambda_val = lambda_val
        self.discount = discount
        self.norm_const = norm_const
        self.t_total_length = self.t_total_types + (self.t_total_tokens * self.lambda_val)

        if self.n_gram == 2:
            self.uni_train_dl = Dataloader(self.train_file, 1, self.unk_threshold)
            self.uni_dev_dl = Dataloader(self.dev_file, 1, self.unk_threshold)

            self.ut_sents, self.ut_items, self.ut_types, self.ut_tokens = self.uni_train_dl.read_file()
            self.ud_sents, self.ud_items, self.ud_types, self.ud_tokens = self.uni_dev_dl.read_file()

            self.ut_total_types = len(self.ut_types) - 2
            self.ut_total_tokens = len(self.ut_tokens) - 2

            self.ut_total_length = self.ut_total_types + (self.ut_total_tokens * self.lambda_val)

        
    # prob(X) = count(X)/count(total_types) + lambda
    def train(self):
        self.t_prob = {k: (v + self.lambda_val)/self.t_total_length for k, v in self.t_items.items()}
        if self.n_gram == 2:
            self.ut_prob = {k: (v + self.lambda_val)/self.ut_total_length for k, v in self.ut_items.items()}
        return self.t_prob


    # Calculate Perplexity
    def eval(self):
        prob_list = []
        for k,v in self.d_items.items():
            if k in self.t_prob:
                self.d_prob[k] = self.t_prob[k] - self.discount
            elif self.n_gram == 2:
                word = k[1]
                self.d_prob[k] = self.norm_const * self.ut_prob.get(k, self.unk_val + self.lambda_val)
            else:
                self.d_prob[k] = self.unk_val + self.lambda_val
            prob_list.append(self.d_prob[k])

        return np.exp(-np.mean(np.log(prob_list)))




