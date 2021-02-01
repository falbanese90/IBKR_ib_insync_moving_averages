from ib_insync import *
# research Adaptive Algo Order
from stock_buckets import *

# connect to IBKR api
ib = IB()
ib.connect('127.0.0.1', 4001, clientId=1)

# googl = Stock('GOOGL', 'SMART', 'USD', primaryExchange = 'NASDAQ')
# details = ib.reqContractDetails(googl)
# details_dict = util.tree(details)
# print(details_dict)

# broad account metrics
acct = util.tree(ib.accountSummary())
acctSum = {}
for index in (20, 9, 13, 32):
    acctSum[acct[index]['tag']] = acct[index]['value']
print(acctSum)

# portfolio metrics
positions = util.tree(ib.positions())
# print(positions)
acctSum['Positions'] = acctPos = {}
for index in range(len(positions)):
    acctPos[positions[index]['contract']['option']['symbol']] = positions[index]['contract']['option']['secType']
print(acctSum)

















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
