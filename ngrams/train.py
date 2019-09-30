#!/usr/bin/env python3

import os
import io
import argparse
from utils.configs import Configuration

def get_config():
    parser = argparse.ArgumentParser("N-gram models Argument Parser")

    parser.add_argument("-cf", "--config_file", default="./configs/hyperparameters.json", metavar="PATH", help="Configuration file path .json")

    parser.add_argument("-of", "--output_folder", default="./output", metavar="PATH", help="Output folder path")

    parser.add_argument("-d", "--data_folder", default="./data", metavar="PATH", help="Configuration file path .json")

    parser.add_argument("-m", "--model_name", default="mle_1", help="The name to save the final state of the model as a file")
 
    parser.add_argument("-n", "--n_gram", default=1, help="N-grams")

    parser.add_argument("-l", "--lambda_val", default=1, help="Lambda for smoothing")

    args = parser.parse_args()

    return Configuration(args)

def main():
    config = get_config()
    print(config.n_gram)

if __name__ == "__main__":
    main()
