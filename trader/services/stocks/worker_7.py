from interfaces.tradeapp import TradeApp
import datetime, time, json

class Worker7(TradeApp):

    entered_tickers = set()
    ohlc_tickers = {}
    
    def entryStrategy(self):
        while True:
            now = datetime.datetime.now()
            # print(now)

            if now.time() >= datetime.time(hour=9, minute=16) and now.time() <= datetime.time(hour=9, minute=22):
                for ticker in self.stock_option_tickers:
                    
                    try:
                        live_data = self.getLiveData(ticker)
                    except:
                        continue
                    
                    if ticker not in self.ohlc_tickers:
                        self.ohlc_tickers[ticker] = live_data['ohlc']

                    ohlc = self.ohlc_tickers[ticker]
                    
                    

                    if ohlc['open'] == ohlc['low'] and 'CE' in ticker and ticker not in self.entered_tickers:
                        trade = self.generateLimitOrderBuyStockOption(ticker, 'ENTRY_STOCK')
                        self.sendTrade(trade)
                        self.entered_tickers.add(ticker)
                        print(json.dumps({
                            'ohlc': ohlc,
                            'ticker': ticker
                        }, indent=2))
                        # self.insertOrder(ticker, trade)

                    elif ohlc['open'] == ohlc['high'] and 'PE' in ticker and ticker not in self.entered_tickers:
                        trade = self.generateLimitOrderBuyStockOption(ticker, 'ENTRY_STOCK')
                        self.sendTrade(trade)
                        self.entered_tickers.add(ticker)
                        # self.insertOrder(ticker, trade)
                        
                        print('-'*10 + 'ENTRY CONDITION' + '-'*10)
                        print(json.dumps({
                            'ohlc': ohlc,
                            'ticker': ticker
                        }, indent=2))
                        print('-'*10 + 'ENTRY CONDITION' + '-'*10)
            else:
                print("Cant enter Worker 7")


            time.sleep(5)


    def exitStrategy(self):
        while True:
            orders = self.getAllOrders()
            
            for order in orders:
                print(order)
                ticker = order['ticker']
                entry_price = self.averageEntryprice(order['data'])
                live_data = self.getLiveData(ticker)
                ohlc = self.ohlc_tickers[ticker]

                pnl = self.getPnl(entry_price, live_data['last_price'])
                if pnl >= 4 or live_data['last_price'] < ohlc['low']:
                    print('-'*10 + 'EXIT' + '-'*10)
                    print(json.dumps({
                        'ticker': ticker,
                        'pnl': pnl,
                    }, indent=2))
                    print('-'*10 + 'EXIT' + '-'*10)

                    trade = self.generateLimitOrderSellStockOption(ticker, 'EXIT')
                    self.sendTrade(trade)
                    self.entered_tickers.discard(ticker)
                    self.deleteOrder(ticker)
            
            time.sleep(10)


def main():
    app = Worker7(name='worker_7')
    app.start()