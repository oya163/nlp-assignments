#!/usr/bin/env python3

'''
    Implementation of Point-wise multiplication

    Course - NLP 673
    Assignment - 2
    Author - Oyesh Mann Singh
    Date - 08/11/2019

    Question 5

    How to Run:
    ./pmi.py -t <path-to-dataset> -w <optional-word-for-association> -l lambda
'''

import os
import argparse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
from itertools import groupby

parser = argparse.ArgumentParser(description='Zipfian arguments')
parser.add_argument('-t', '--train', required=True, metavar='FILE',
                    help='input train filename')
parser.add_argument('-w', '--word', type=str, metavar='STRING',
                    help='word association')
parser.add_argument('-l', '--lam', type=float, default=0.0, metavar='FLOAT',
                    help='lambda')


args = parser.parse_args()

# Return computed freq_dict
def file_reader(filename):
    words = []
    sents = []
    types = {}
    type_list = []
    with open(filename, 'r') as in_file:
        for line in enumerate(in_file):
            row = line[1].strip().split()
            if len(row) > 0 and row[0] != "#":
                word = row[1]
                words.append(word)
                type_list.append(word)
                if word in types:
                    types[word]+=1
                else:
                    types[word] = 1
            elif len(row) == 0:
                sents.append(' '.join(words))
                words = []

    freq_dict = dict(sorted(types.items(), key=lambda kv: kv[1], reverse=True))
    corpus_size = sum(types.values())

    return sents, freq_dict, corpus_size


def freq_counter(term, freq_dict, N):
    count = freq_dict[term]
    freq = count/N
    return freq

def get_top_10_prob():
    sents, freq_dict, N = file_reader(args.train)
    top_freq = list((k,(freq_dict[k]/N)) for k,v in freq_dict.items())
    return top_freq[:10]


def printer(item):
    if type(item) == list:
        for each in item:
            print(each)
    elif type(item) == dict:
        for k,v in item.items():
            print(k,v)


def calc_pmi(pair_prob, first_word_prob, second_word_prob):
    pmi = {}
    for word_pair, both_prob in pair_prob.items():
        first_prob = first_word_prob[word_pair[0]]
        second_prob = second_word_prob[word_pair[1]]
        pmi[word_pair] = math.log(both_prob/(first_prob * second_prob))

    return pmi
    

def interesting(pmi_list, gt=True):
    top_list = []
    if gt:
        pmi_list = pmi_list[::-1]

    for each in pmi_list:
        if gt and each[1] > 3:
            top_list.append(each)
        elif each[1] < 3:
            top_list.append(each)
        if len(top_list) > 10:
            break
    
    return top_list
            

def joint_freq():
    sents, freq_dict, N = file_reader(args.train)
    final_sents = []
    
    # Create bigrams from each sentence
    for sent in sents:
        text = sent.split()
        if args.word:
            if args.word in text:
                for i in range(0, len(text)-1):
                    final_sents.append((text[i], text[i+1]))
        else:
            for i in range(0, len(text)-1):
                final_sents.append((text[i], text[i+1]))

    # Count the bigrams
    counts = [(i, len(list(c))) for i,c in groupby(sorted(final_sents))]
    
    # Sort the bigrams in desc order
    counts.sort(key = lambda x:x[1], reverse=True)

    # Get top 10 pairs
    top_pairs = counts

    # Get probability of each pair
    top_pairs_prob = {}
    for each in top_pairs:
        top_pairs_prob[each[0]] = each[1]/N + args.lam
    
    top_pairs_prob_sorted = sorted(top_pairs_prob.items(), key = lambda x:x[1], reverse=True)
    top_pairs_dict = dict(top_pairs_prob_sorted)

    # Get probability of each top words from pair
    first_word_prob = {}
    second_word_prob = {}
    for each in top_pairs:
        words = each[0]
        first_word_prob[words[0]] = freq_dict[words[0]]/N + args.lam
        second_word_prob[words[1]] = freq_dict[words[1]]/N + args.lam

    first_word_prob_list = [(k,v) for k,v in first_word_prob.items()]
    second_word_prob_list = [(k,v) for k,v in second_word_prob.items()]

    print("Top pairs")
    printer(top_pairs_prob_sorted[:10])

    print("\nFirst word probability")
    printer(first_word_prob_list[:10])

    print("\nSecond word probability")
    printer(second_word_prob_list[:10])

    print("\nTop PMI")
    pmi = calc_pmi(top_pairs_dict, first_word_prob, second_word_prob)
    pmi_sorted = sorted(pmi.items(), key = lambda x:x[1], reverse=True)
    printer(pmi_sorted[:10])
    
    print("\nBottom PMI")
    printer(pmi_sorted[::-1][:10])


    print("\nTop 10 list where PMI greater than 3")
    pmi_gt_3 = interesting(pmi_sorted)
    #printer(pmi_gt_3)

    print("\nTop 10 list where PMI less than 3")
    pmi_gt_3 = interesting(pmi_sorted, gt=False)
    #printer(pmi_gt_3)


def main():
    joint_freq()
    

if __name__ == "__main__":
    main()

