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
 
        self.output_folder = os.path.normpath(config.get("output_folder","./output"))
        self.data_folder = os.path.normpath(config.get("data_folder","./data"))
        self.training_file = os.path.normpath(os.path.join(self.data_folder, config.get("training_file","train")))
        self.dev_file = os.path.normpath(os.path.join(self.data_folder, config.get("dev_file","dev")))
        self.test_file = os.path.normpath(os.path.join(self.data_folder, config.get("test_file","test")))
        
        self.model_folder = os.path.normpath(os.path.join(self.output_folder, "models")) 
        self.model_name = args.model_name if args.model_name else config.get("model_name", "default_model")
        self.n_gram = args.n_gram if args.n_gram else config.get("n_gram", 1)
        self.lambda_val = int(config.get("lambda", 1))
        


