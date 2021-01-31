from ib_insync import *
# research Adaptive Algo Order
from stock_buckets import *

# connect to IBKR api
ib = IB()
ib.connect('127.0.0.1', 4001, clientId=1)

googl = Stock('GOOGL', 'SMART', 'USD', primaryExchange = 'NASDAQ')
details = ib.reqContractDetails(googl)
details_dict = util.tree(details)
print(details_dict)


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
