from ib_insync import *
# research Adaptive Algo Order
from buckets import *

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

googl = Stock('GOOGL', 'SMART', 'USD')
print(util.tree(ib.qualifyContracts(googl)))



# print(util.tree(ib.reqSecDefOptParams('GOOGL', '', 'STK', 208813719)))








# googl = Stock('GOOGL', 'SMART', 'USD', primaryExchange = 'NASDAQ')
# details = ib.reqContractDetails(googl)
# details_dict = util.tree(details)
# print(details_dict)

















# # append lowerBB_securities with industry_category_subcategory items
# for security in range(len(lowerBB_securities)):
#     try:
#         stock = Stock(lowerBB_securities[security][0], 'SMART', 'USD', primaryExchange = lowerBB_securities[security][1])
#         details = ib.reqContractDetails(stock)
#         details_dict = util.tree(details)
#         lowerBB_securities[security].append(details_dict[0]['ContractDetails']['industry'])
#         lowerBB_securities[security].append(details_dict[0]['ContractDetails']['category'])
#         lowerBB_securities[security].append(details_dict[0]['ContractDetails']['subcategory'])
#     except IndexError:
#         lowerBB_securities[security].append('')
#         lowerBB_securities[security].append('')
#         lowerBB_securities[security].append('')
#     except KeyError:
#         lowerBB_securities[security].append('')
#         lowerBB_securities[security].append('')
#         lowerBB_securities[security].append('')
# print(lowerBB_securities)
