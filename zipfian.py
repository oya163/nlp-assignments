#!/usr/bin/env python3

'''
    Exploring how well Zipf's law holds
    for two languages from Universal Dependency data

    Course - NLP 673
    Assignment - 2
    Author - Oyesh Mann Singh
    Date - 08/11/2019

    Question 4

    How to run:
    ./zipfian.py -t <data-path>

'''

import os
import argparse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from math import log

from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score


parser = argparse.ArgumentParser(description='Zipfian arguments')
parser.add_argument('-t', '--train', required=True, metavar='FILE',
                    help='input train filename')


args = parser.parse_args()

# Returns computed freq_dict
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

    return freq_dict


# Returns frequency list
def get_freq(dictionary):
    ret_list = []
    for each in dictionary:
        ret_list.append(each[1])

    return ret_list


# Returns frequency and rank of words
def calculate_freq(filename):
    freq_dict = file_reader(filename)
    freq_list = get_freq(freq_dict)

    return (freq_list, np.arange(1, len(freq_list)+1))


# Computes linear regression
def regression():
    freq, rank = calculate_freq(args.train)
    y = np.asarray([log(z,10) for z in freq])
    x = np.asarray([log(i,10) for i in rank])
    x = x.reshape(-1, 1)           # Single feature used so reshaping

    regr = linear_model.LinearRegression()
    regr.fit(x, y)
    y_pred = regr.predict(x)

    mse = mean_squared_error(y, y_pred)
    var = r2_score(y, y_pred)

    return (x, y, y_pred, mse, var)

    
# Plots the scatter plot and linear regression line
def plot():
    x, y, y_pred, mse, var = regression()
    print("Mean Squared Error: ", mse)
    print("Variance score: ", var)

    plt.scatter(x, y, color='black', s=1)
    plt.plot(x, y_pred, color='blue', linewidth=1)
    plt.ylabel('log10freq')
    plt.xlabel('log10rank')
    plt.show()



def main():
    plot()


if __name__ == "__main__":
    main()

