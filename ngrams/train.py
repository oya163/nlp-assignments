#!/usr/bin/env python3

"""
	Evaluating Count-based Language Modelling
	 - Maximum Likelihood Estimation
         - Laplace
         - Backoff
        Author - Oyesh Mann Singh
        Assignment - 3
"""

import os
import io
import argparse
from utils.configs import Configuration
from models import MLE, Laplace, Backoff

def get_config():
    parser = argparse.ArgumentParser("N-gram models Argument Parser")

    parser.add_argument("-cf", "--config_file", default="./configs/hyperparameters.json", metavar="PATH", help="Configuration file path .json")

    parser.add_argument("-of", "--output_folder", default="./output", metavar="PATH", help="Output folder path")
    
    parser.add_argument("-tf", "--train_file", default="../data/en_ewt-ud-train.conllu", metavar="PATH", help="Train file path")
    
    parser.add_argument("-df", "--dev_file", default="../data/en_ewt-ud-dev.conllu", metavar="PATH", help="Dev file path")

    parser.add_argument("-m", "--model_name", default="mle", choices=["mle", "laplace", "backoff"], help="The name to save the final state of the model as a file")
 
    parser.add_argument("-n", "--n_gram", default=1, choices=[1, 2], type=int, help="N-grams")

    parser.add_argument("-l", "--lambda_val", default=1, type=float, help="Lambda for smoothing")

    args = parser.parse_args()

    return Configuration(args)

def main():
    config = get_config()
    config.print_stat()
    if config.model_name == "mle":
        print("*********MLE MODEL***************")
        model = MLE(config.train_file, config.dev_file, config.n_gram, config.unk_threshold, config.unk_val)
    elif config.model_name == "laplace":
        print("*********LAPLACE MODEL***************")
        model = Laplace(config.train_file, config.dev_file, config.n_gram, config.unk_threshold, config.unk_val, config.lambda_val)
    elif config.model_name == "backoff":
        print("*********BACKOFF MODEL***************")
        model = Backoff(config.train_file, config.dev_file, config.n_gram, config.unk_threshold, config.unk_val, 
                        config.lambda_val, config.discount, config.norm_const)
    model.print_stat()
    model.train()
    print("Perplexity of {0} = {1}".format(config.model_name, model.eval()))
    
    
if __name__ == "__main__":
    main()
