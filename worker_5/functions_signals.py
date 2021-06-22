import json
from zerodha_functions import *
import websocket
from kiteconnect import KiteConnect

import os

PUBLISHER_HOST = os.environ['PUBLISHER_HOST']
PUBLISHER_PATH = os.environ['PUBLISHER_PATH']

PUBLISHER_URI = f'{PUBLISHER_HOST}{PUBLISHER_PATH}'

def send_notification(data):
    try:
        ws_publisher = websocket.create_connection(PUBLISHER_URI)
        ws_publisher.send(json.dumps(data))
        ws_publisher.close()
    except:
        pass

def start_trade(kite : KiteConnect, document, quantity):
    # flag = False
    
    CE_KEY = 'CE_Stikes'
    PE_KEY = 'PE_Stikes'
    PERCENTAGE = 5/100
    
    ce_documents = document[CE_KEY]
    pe_documents = document[PE_KEY]
    
    for strike in ce_documents:
        ltp_ce = ce_documents[strike]['lastPrice']
        min_ltp_ce = ltp_ce*(1-PERCENTAGE)
        max_ltp_ce = ltp_ce*(1+PERCENTAGE)
        
        for strike_ in pe_documents:
            ltp_pe = pe_documents[strike_]['lastPrice']
            
            if ltp_pe >= min_ltp_ce and ltp_pe <= max_ltp_ce:
                print(ce_documents[strike]['weekly_Options_CE'], pe_documents[strike_]['weekly_Options_PE'])
                market_buy_order(
                    kite=kite,
                    quantity=quantity,
                    tradingsymbol=ce_documents[strike]['weekly_Options_CE'],
                    exchange=kite.EXCHANGE_NFO
                )
                
                market_buy_order(
                    kite=kite,
                    tradingsymbol=pe_documents[strike_]['weekly_Options_PE'],
                    quantity=quantity,
                    exchange=kite.EXCHANGE_NFO
                )
                return
        
        
    for strike in pe_documents:
        ltp_pe = pe_documents[strike]['lastPrice']
        min_ltp_pe = ltp_pe*(1-PERCENTAGE)
        max_ltp_pe = ltp_pe*(1+PERCENTAGE)
        
        for strike_ in ce_documents:
            ltp_ce = ce_documents[strike_]['lastPrice']
            
            if ltp_ce >= min_ltp_pe and ltp_ce <= max_ltp_pe:
                print(ce_documents[strike_]['weekly_Options_CE'], pe_documents[strike]['weekly_Options_PE'])
                market_buy_order(
                    kite=kite,
                    tradingsymbol=ce_documents[strike_]['weekly_Options_CE'],
                    quantity=quantity,
                    exchange=kite.EXCHANGE_NFO
                )
                market_buy_order(
                    kite=kite,
                    tradingsymbol=pe_documents[strike]['weekly_Options_PE'],
                    quantity=quantity,
                    exchange=kite.EXCHANGE_NFO
                )
                return
    
    return