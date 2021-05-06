#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 09:48:00 2021

@author: yashmadhwal
"""

from telegram import *
from telegram.ext import *

#Imporing Bitcoin class and addresses
from BitcoinKeyPairs import BitcoinTestAddress, BitcoinMainAddress

#creating bot variable for initialing bot. //BitcoinAddressGenerator

#get token Id
token = '1716172449:AAFNghthU-LSMXI6UEeJm7zUzMU7ZPpVZfY'
bot = Bot(token)
print(bot.get_me())

#creating updater variable, to update what ever we do without bot.
updater = Updater(token,use_context = True)

#Dispatcher variable will update to our telegram bot

dispatcher = updater.dispatcher


def start(update:Update,context:CallbackContext):
    bot.sendMessage(
        chat_id = update.effective_chat.id,
        text = '''
Hello, Beautiful People..
Welcome to my channel, here you will receive bitcoin's Address for both mainnet and testnet.

So, are you ready??
Please choose, which key pair address you want to receive?
1. /Mainnet
2. /Testnet
        ''',
        )
    
def Mainnet(update:Update,context:CallbackContext):
    
    a = BitcoinMainAddress()
    private_key = a.private_key
    public_key = a.public_key
    public_address = a.address
    
    bot.sendMessage(
        chat_id = update.effective_chat.id,
        text = f'''
PrivateKey : `{private_key}`
PublicKey  : `{public_key}`
Address    : `{public_address}`

Save it in a safe place\.\.\.\.
Once saved if you want\. /GoToMainMenue       
''',
        parse_mode=ParseMode.MARKDOWN_V2
        )
    
def Testnet(update:Update,context:CallbackContext):
    
    a = BitcoinTestAddress()
    private_key = a.private_key
    public_key = a.public_key
    public_address = a.address
    
    bot.sendMessage(
        chat_id = update.effective_chat.id,
        text = f'''
PrivateKey : `{private_key}`
PublicKey  : `{public_key}`
Address    : `{public_address}`

Save it in a safe place\.\.\.\.
Once saved if you want\. /GoToMainMenue       
''',
        parse_mode=ParseMode.MARKDOWN_V2
        )
    

start_value = CommandHandler('start', start)
Mainnet = CommandHandler('Mainnet', Mainnet)
Testnet = CommandHandler('Testnet', Testnet)

Main = CommandHandler('GoToMainMenue',start)

dispatcher.add_handler(start_value)
dispatcher.add_handler(Mainnet)
dispatcher.add_handler(Testnet)
dispatcher.add_handler(Main)

updater.start_polling()