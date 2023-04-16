#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Algorants.com
"""
import time

import pandas as pd

from sending import send_reward

#define data
data_file = r"C:/folder/file.csv" #location csv
testnet=True #change to False for mainnet
mnemonic1 = "" #fill in mnemonic of sending wallet
ASSET_ID = "" #fill in asset id to sent
TRANSACTION_NOTE = "Airdrop" #fill in transaction note
SENDER_ADDRESS = "" #sending wallet address
n = 0 #line to start


#get number of lines to run & Sleep interval. DO NOT CHANGE
data = pd.read_csv(data_file, sep=';') #reading the csv with panda, if you use a comma seperated file change ; to ,
SLEEP_INTERVAL = 1 # AlgoExplorer limit for public calls


for n in range(0,len(data)):
    time.sleep(SLEEP_INTERVAL)
    response = send_reward(n, data_file, ASSET_ID, TRANSACTION_NOTE, SENDER_ADDRESS, mnemonic1, testnet)
    n = n + 1