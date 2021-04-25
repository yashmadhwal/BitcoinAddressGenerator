#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 17:16:58 2020

@author: yashmadhwal
"""
import os
import ecdsa
import hashlib
import base58
import binascii

#Defining Function For Hashing: 1. Sha256 and 2. Ripemd160
def hashing(a,flag):
    first_sha256 = hashlib.sha256(a)
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(first_sha256.digest())
    return_0 = ripemd160.digest()
    return_1 = bytes.fromhex("00") + ripemd160.digest()
    return_2 = bytes.fromhex("6f") + ripemd160.digest()

    if flag == 'Testnet':
        return return_0, return_2

    elif flag == 'Mainnet':
        return return_0,return_1

#Function for Checksum
def checksum(b):
    checksum_full = hashlib.sha256(hashlib.sha256(b).digest()).digest()
    new_checksum = checksum_full[:4]
    return b + new_checksum

#Function to convert to base58
def to_base58(c):
    return base58.b58encode(c).decode('utf-8')

def compressed_key(d):
    a = d.hex()

    if a[-1] == '0' or a[-1] == '2' or a[-1] == '4' or a[-1] == '6' or a[-1] == '8' or a[-1] == 'a' or a[-1] == 'c' or a[-1] == 'e':
        return bytes.fromhex("02") + d

    else:
        return bytes.fromhex("03") + d


class BitcoinTestAddress:

    def __init__(self,**kwargs):
        if 'private_key' in kwargs.keys():
            self.__private_key = kwargs['private_key']
        else:
            self.__private_key = BitcoinTestAddress.__generate_private_key()
        self.__public_key = self.__generate_public_key()
        self.__address = self.__generate_address()


    def __generate_private_key():
        private_key = os.urandom(32).hex()
        return private_key


    def __generate_public_key(self):
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(self.__private_key), curve = ecdsa.SECP256k1)
        verification_key = sk.verifying_key
        public_key = bytes.fromhex("04") +  verification_key.to_string()
        return public_key.hex()


    def __generate_address(self):
        decoded_pubkey, testnet_pubkey = hashing(bytes.fromhex(self.__public_key),flag = 'Testnet')
        #checksum
        checksum_test_pubkey = checksum(testnet_pubkey)
        test_address = to_base58(checksum_test_pubkey)
        return test_address

    @property
    def private_key(self):
        return self.__private_key

    @property
    def public_key(self):
        return self.__public_key

    @property
    def address(self):
        return self.__address



class BitcoinMainAddress:

    def __init__(self,**kwargs):
        if 'private_key' in kwargs.keys():
            self.__private_key = kwargs['private_key']
        else:
            self.__private_key = BitcoinMainAddress.__generate_private_key()
        self.__public_key = self.__generate_public_key()
        self.__address = self.__generate_address()


    def __generate_private_key():
        private_key = os.urandom(32).hex()
        return private_key


    def __generate_public_key(self):
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(self.__private_key), curve = ecdsa.SECP256k1)
        verification_key = sk.verifying_key
        public_key = bytes.fromhex("04") +  verification_key.to_string()
        return public_key.hex()


    def __generate_address(self):
        decoded_pubkey, testnet_pubkey = hashing(bytes.fromhex(self.__public_key),flag = 'Mainnet')
        #checksum
        checksum_test_pubkey = checksum(testnet_pubkey)
        test_address = to_base58(checksum_test_pubkey)
        return test_address

    @property
    def private_key(self):
        return self.__private_key

    @property
    def public_key(self):
        return self.__public_key

    @property
    def address(self):
        return self.__address




import json
import sys
from web3 import Web3, HTTPProvider
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    a = BitcoinMainAddress()


    private_key = a.private_key
    public_key = a.public_key
    public_address = a.address

    return render_template('index.html', private_key= private_key, public_key=public_key,public_address=public_address)


if __name__ == '__main__':
    app.run(debug=True)
