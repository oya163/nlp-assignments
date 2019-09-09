#!/usr/bin/env python3

'''
    Implementation of Point-wise multiplication

    Course - NLP 673
    Assignment - 2
    Author - Oyesh Mann Singh
    Date - 08/11/2019

    Question 5
'''

import os
import argparse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='Zipfian arguments')
parser.add_argument('-t', '--train', required=True, metavar='FILE',
                    help='input train filename')


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


def freq_counter(term):
    sents, freq_dict, N = file_reader(args.train)
    count = freq_dict[term]
    freq = count/N

    return freq


def joint_freq(term1, term2):
    count1 = freq_counter(term1)
    count2 = freq_counter(term2)
    
    sents, freq_dict, N = file_reader(args.train)

    for each in sents:
        
    

    

def main():
    term = 'is'
    print("The frequency of {0} is {1}".format(term, freq_counter(term)))
    

if __name__ == "__main__":
    main()

