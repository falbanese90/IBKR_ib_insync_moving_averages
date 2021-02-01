from ib_insync import *
# research Adaptive Algo Order
from stock_buckets import *

# connect to IBKR api
ib = IB()
ib.connect('127.0.0.1', 4001, clientId=2)

# create dictionary of account and portfolio values for risk management
def accountAndPositions():
    acct = util.tree(ib.accountSummary())
    acctSum = {}
    for index in (20, 9, 13, 32):
        acctSum[acct[index]['tag']] = acct[index]['value']
    positions = util.tree(ib.positions())
    acctSum['Positions'] = acctPos = {}
    for index in range(len(positions)):
        acctPos[positions[index]['contract']['Option']['symbol']] = [
            positions[index]['contract']['Option']['secType'],
            positions[index]['contract']['Option']['strike'],
            positions[index]['contract']['Option']['right'],
            positions[index]['contract']['Option']['lastTradeDateOrContractMonth']
        ]
    return acctSum

# googl = Stock('GOOGL', 'SMART', 'USD', primaryExchange = 'NASDAQ')
# details = ib.reqContractDetails(googl)
# details_dict = util.tree(details)
# print(details_dict)



