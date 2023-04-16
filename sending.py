#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Algorants.com
"""
import pandas as pd

from algosdk import mnemonic
from algosdk.error import WrongChecksumError
from algosdk.future.transaction import AssetTransferTxn
from algosdk.v2client import algod


def send_reward (n, data_file, ASSET_ID, TRANSACTION_NOTE, SENDER_ADDRESS, mnemonic1, testnet=True):

    """
    Reading file and returning amount + wallet address
    """
    data = pd.read_csv(data_file, sep=';')
    wallet_reciever = data['Wallet'][n]
    amount_to_recieve = data['Amount'][n]
    
    pk = mnemonic.to_public_key(mnemonic1)
    sk = mnemonic.to_private_key(mnemonic1)

    """
    testnet or mainnet selection
    """
    if (testnet==True):
        algod_address = "https://api.testnet.algoexplorer.io"
    elif (testnet==False):
        algod_address = "https://api.algoexplorer.io"
        
    algod_token = ""
    algod_client = algod.AlgodClient(algod_token, algod_address, headers={'User-Agent': 'AlgorAnts'})

    def wait_for_confirmation(client, txid):
        """
        Utility function to wait until the transaction is
        confirmed before proceeding.
        """
        last_round = client.status().get('last-round')
        txinfo = client.pending_transaction_info(txid)
        while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
            last_round += 1
            client.status_after_block(last_round)
            txinfo = client.pending_transaction_info(txid)
        print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
        return txinfo

    params = algod_client.suggested_params()
    params.fee = 1000
    params.flat_fee = True
    note = TRANSACTION_NOTE
    decimals = algod_client.asset_info(ASSET_ID).get("params").get("decimals")
    amount = int(amount_to_recieve) * (10 ** decimals)
    reciever = wallet_reciever

    txn = AssetTransferTxn(
        SENDER_ADDRESS,
        params,
        reciever,
        amount,
        index=ASSET_ID,
        note=note.encode(),
        )

    # Sign with secret key of creator
    try:
        stxn = txn.sign(sk)
    except WrongChecksumError:
        return "Checksum failed to validate"
    except ValueError:
        return "Unknown word in passphrase"    
    
    # Send the transaction to the network and retrieve the txid.
    txid = algod_client.send_transaction(stxn)
    
    # Wait for the transaction to be confirmed
    wait_for_confirmation(algod_client,txid)
    
    try:
        algod_client.pending_transaction_info(txid)
    except Exception as e:
        print(e)

    print(f"Amount of {amount_to_recieve} sent to {reciever}")
    return ""