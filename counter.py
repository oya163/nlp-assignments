#!/usr/bin/env python3

'''
    NLP Fall 2019 Assignment

    Assignment 1 - Counter program
    Date - 09/02/2019
    Author - Oyesh Mann Singh

    Assignment PDF:
    https://www.csee.umbc.edu/courses/undergraduate/473/f19/content/materials/a1.pdf

    Basic Usage:
    python counter.py -q c -t <train_file> -d <development_file> -k 30 -a 10

        -q = question choice
        -t = training filename
        -d = development filename
        -k = topK value
        -a = appearance time for least common words
'''

import argparse

parser = argparse.ArgumentParser(description='Counter arguments')
parser.add_argument('-t', '--train', required=True, metavar='FILE',
                    help='input train filename')
parser.add_argument('-d', '--dev', metavar='FILE',
                    help='input dev filename')
parser.add_argument('-k', '--topk', metavar='N', type=int, default=20,
                    help='topk words')
parser.add_argument('-a', '--appear', metavar='N', type=int, default=1,
                    help='appearance times')
parser.add_argument('-q', '--question', metavar='C', type=str, default='a',
                    required=True, help='question number')

args = parser.parse_args()


# Prints number of sentences and average words/sentences
def solution_3a():
    sent_counter = 0
    total_word = 0
    word_counter = 0
    filename = args.train

    with open(filename, 'r') as in_file:
        for line in enumerate(in_file):
            row = line[1].strip().split()
            if len(row) > 0:
                if not row[0] == "#":
                    word_counter += 1
            else:
                sent_counter += 1
                total_word += word_counter
                word_counter = 0

    print("Number of sentences = ", sent_counter)
    print("Average number of words = {0:.5}".format(total_word/sent_counter))


# Helper function to get sorted_types, type_list and tokens_list
def file_reader(filename, reverse=True):
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

    sorted_types = sorted(types.items(), key=lambda kv: kv[1], reverse=reverse)

    return (sorted_types, type_list, set(type_list))


# Print statistics of Training set
def solution_3b():
    sorted_types, type_list, token_list = file_reader(args.train)
    print("Total number of types = ", len(type_list))
    print("Total number of tokens = ", len(token_list))
    

# Prints the topK words
def solution_3c():
    sorted_types,_,_ = file_reader(args.train)
    topk = sorted_types[:args.topk]
    print("The top {0} most common words in train file are".format(args.topk))
    for each in topk:
        print(each[0])
    

# Helper function to get least common words
def get_least_common():
    least_common = []
    sorted_types, num_of_types, num_of_tokens = file_reader(args.train, reverse=False)
    for each in sorted_types:
        if each[1] == args.appear:
            least_common.append(each[0])
        elif each[1] > args.appear:
            break
    return least_common


# Prints Least common words that appear specific number of times
def solution_3e():
    least_common = get_least_common()
    for each in least_common:
        print(each)
    print("There are {0} words that appear {1} times are".format(len(least_common), args.appear))


# Out-of-vocabulary statistics
# Training_set - Dev_set = OOV words
def solution_3f():
    train_sorted_types, train_types, train_tokens = file_reader(args.train)
    dev_sorted_types, dev_types, dev_tokens = file_reader(args.dev)
    print("*****Train statistics*****")
    print("Total number of types = ", len(train_types))
    print("Total number of tokens = ", len(train_tokens))
    print("*****Dev statistics*****")
    print("Total number of types = ", len(dev_types))
    print("Total number of tokens = ", len(dev_tokens))
    print("*****Out-of-vocabulary statistics*****")
    print("OOV = ", len(train_tokens - dev_tokens))


# Answers according to the choice
def main():
    input_choice = args.question
    if input_choice == 'a':
        solution_3a()
    elif input_choice == 'b':
        solution_3b()
    elif input_choice == 'c':
        solution_3c()
    elif input_choice == 'e':
        solution_3e()
    elif input_choice == 'f':
        solution_3f()
    else:
        print("That question cannot be answered here!!!")


if __name__ == "__main__":
    main()
    
   
