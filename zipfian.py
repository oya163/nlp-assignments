#!/usr/bin/env python3

'''
    Exploring how well Zipf's law holds
    for two languages from Universal Dependency data

    Course - NLP 673
    Assignment - 2
    Author - Oyesh Mann Singh
    Date - 08/11/2019

    Question 4
'''

import os
import argparse
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')

parser = argparse.ArgumentParser(description='Zipfian arguments')
parser.add_argument('-t', '--train', required=True, metavar='FILE',
                    help='input train filename')


args = parser.parse_args()

# Return computed freq_dict
def file_reader(filename):
    types = {}
    tokens = 0
    type_list = []
    with open(filename, 'r') as in_file:
        for line in enumerate(in_file):
            row = line[1].strip().split()
            if len(row) > 0 and row[0] != "#":
                type_list.append(row[1])
                if row[1] in types:
                    types[row[1]]+=1
                else:
                    types[row[1]] = 1

    freq_dict = sorted(types.items(), key=lambda kv: kv[1], reverse=True)
    rank_dict = sorted(types.items(), key=lambda kv: kv[1], reverse=False)

    return (freq_dict, rank_dict)


def get_freq(dictionary):
    ret_list = []
    for each in dictionary:
        ret_list.append(each[1])

    return ret_list


def calculate_freq(filename):
    freq_dict, rank_dict = file_reader(filename)
    freq_list = get_freq(freq_dict)
    rank_list = get_freq(rank_dict)

    return freq_list, rank_list
    

def plot():
    freq, rank = calculate_freq(args.train)
    


def main():
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    plt.show()

if __name__ == "__main__":
    main()

