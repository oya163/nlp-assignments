#!/usr/bin/env python3

import io
import json
import os

class Configuration:
    def __init__(self, args):
        config = {}

        if args.config_file is None:
            print("Config not provided for the program.")
        else:
            if not os.path.exists(args.config_file):
                print("Config file not found in" + args.config_file)
            else:
                with io.open(args.config_file, encoding='utf-8') as f:
                    config = json.load(f)
 
        self.output_folder = args.output_folder
        self.train_file = args.train_file
        self.dev_file = args.dev_file
        
        self.model_folder = os.path.normpath(os.path.join(self.output_folder, "models")) 
        self.model_name = args.model_name if args.model_name else config.get("model_name", "default_model")
        self.n_gram = args.n_gram if args.n_gram else config.get("n_gram", 1)
        self.lambda_val = int(config.get("lambda_val", 1))
        self.unk_threshold = int(config.get("unk_threshold", 1))
        self.unk_val = int(config.get("unk_val", 0))
        self.discount = int(config.get("discount", 0))
        self.norm_const = int(config.get("norm_const", 0))
    

    def print_stat(self):
        print("*********Hyperparameter stat********")
        print("Output folder: 	", self.output_folder)
        print("Train file: 	", self.train_file)
        print("Dev file: 	", self.dev_file)
        print("Model folder: 	", self.model_folder)
        print("Model name: 	", self.model_name)
        print("n-gram: 		", self.n_gram)
        print("Lambda value: 	", self.lambda_val)
        print("UNK threshold: 	", self.unk_threshold)
        print("UNK initial value: ", self.unk_val)
        print("Discount for backoff: ", self.discount)
        print("Norm constant: ", self.norm_const)
        


