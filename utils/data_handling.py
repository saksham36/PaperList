#!/usr/bin/env python3
'''
Written by: Saksham Consul 04/05/2023
Scripts needed for data handling
'''

import yaml
import pickle


def read_config():
    '''Reads config.yaml file and returns a dictionary of the contents'''
    with open("config.yaml", "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)


def load_pickle(filename):
    '''Loads the pickle file and returns the list of papers'''
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data


def save_pickle(data, filename):
    '''Saves the list of papers to a pickle file'''
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
