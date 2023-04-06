#!/usr/bin/env python3.8
'''
Written by: Saksham Consul 04/05/2023
Script to list all profs of interest. 
'''
import pandas
from utils.data_handling import read_config
# TODO Extract from a CSV file

# Read the CSV file
df = pandas.read_csv(
    read_config['csv'])

# Get the name of professors
profs = df['Key Figure']
profs = profs.dropna()

# Replace spaces with +
for prof in profs:
    prof.replace(" ", "+")

profs = profs.tolist()

# Manual list of Stanford professors
# cs_profs = ["CD+Manning", "Jeannette+Bohg", "Emma+Brunskill", "Stefano+Ermon", "Chelsea+Finn", "Sergey+Levine", "Pieter+Abbeel", "Ron+Fedkiw", "Emily+Beth+Fox",
#             "Carlos+Guestrin", "Tatsunori+Hashimoto", "Noah+D.+Goodman", "Oussama+Khatib", "Dan+Jurafsky", "Doug+L+James", "Percy+Liang", "Li+Fei-Fei", "Jure+Leskovec",
#             "James+Landay", "Karen+Liu", "Christopher+Ré", "Jiajun+Wu", "Dorsa+Sadigh"
#             ]

# ee_profs = ["Benjamin+Van+Roy"]

# me_profs = ["Mark+Cutkosky", "Monroe+Kennedy+III", "Allison+Okamura"]

# aa_profs = ["Grace+Gao", "Mykel+Kochenderfer", "Marco+Pavone", "Mac+Schwager"]

# profs = cs_profs + ee_profs + me_profs + aa_profs
