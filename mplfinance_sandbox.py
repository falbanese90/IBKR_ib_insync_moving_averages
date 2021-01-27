from ib_insync import *
import pandas as pd
from statistics import stdev
from datetime import datetime
import mplfinance as mpf
from datetime import date
today_date = date.today().strftime('%m-%d-%y')
import os
from stock_buckets import *

def fetch_data(ticker, prime_exch, data_barcount):
    stock = Stock(ticker, 'SMART', 'USD', primaryExchange = prime_exch)
    bars = ib.reqHistoricalData(
        stock, endDateTime='', durationStr=data_barcount, #365days max
        barSizeSetting='1 day', whatToShow='MIDPOINT', useRTH=True)
    bars = util.tree(bars)
    return bars

def extract_closing(singlestock_bardata):
    closing_prices = []
    for day in range(len(singlestock_bardata)):
        closing_prices.append((singlestock_bardata[day]['BarData']['close']))
    return closing_prices

def create_masubplot(length, closing_prices):
    ma_length = length
    i = 0
    averages = {'data':[]}
    while i < len(closing_prices) - ma_length + 1:
        this_window = closing_prices[i : i + ma_length]
        window_average = round(sum(this_window) / ma_length, 2)
        averages['data'].append(window_average)
        i += 1
    return averages

def create_upperbb_subplot(closing_prices, period, std):
    length = period
    i = 0
    bb = {'data':[]}
    while i < len(closing_prices) - length + 1:
        this_window = closing_prices[i : i + length]
        window_bb = round((sum(this_window) / length) + (2.5 * stdev(this_window)), 2)
        bb['data'].append(window_bb)
        i += 1
    return bb

def create_lowerbb_subplot(closing_prices, period, std):
    length = period
    i = 0
    bb = {'data':[]}
    while i < len(closing_prices) - length + 1:
        this_window = closing_prices[i : i + length]
        window_bb = round((sum(this_window) / length) - (2.5 * stdev(this_window)), 2)
        bb['data'].append(window_bb)
        i += 1
    return bb

def reformat_IBdata(fetched_data, numofdays):
    reformatted_data = {}
    reformatted_data['Date'] = []
    reformatted_data['Open'] = []
    reformatted_data['High'] = []
    reformatted_data['Low'] = []
    reformatted_data['Close'] = []
    for dict in range(len(fetched_data)-numofdays,len(fetched_data)):
        reformatted_data['Date'].append(datetime.strptime(str(fetched_data[dict]['BarData']['date']), '%Y-%m-%d'))
        reformatted_data['Open'].append(fetched_data[dict]['BarData']['open'])
        reformatted_data['High'].append(fetched_data[dict]['BarData']['high'])
        reformatted_data['Low'].append(fetched_data[dict]['BarData']['low'])
        reformatted_data['Close'].append(fetched_data[dict]['BarData']['close'])
    # print("reformatted data:", reformatted_data)
    pdata = pd.DataFrame.from_dict(reformatted_data)
    pdata.set_index('Date', inplace=True)
    return pdata
    print(pdata)

def plot_d(pdata, sma9, sma20, sma50, sma200, lowerbb, upperbb, numofdays, ticker, defining_ma):
    sma9dict = mpf.make_addplot(sma9['data'][-numofdays:], color='#c87cff')
    sma20dict = mpf.make_addplot(sma20['data'][-numofdays:], color='#f28c06')
    sma50dict = mpf.make_addplot(sma50['data'][-numofdays:], color='#3a7821')
    sma200dict = mpf.make_addplot(sma200['data'][-numofdays:], color='#483e8b')
    lowerbbdict = mpf.make_addplot(lowerbb['data'][-numofdays:], color='#b90c0c')
    upperbbdict = mpf.make_addplot(upperbb['data'][-numofdays:], color='#b90c0c')
    mpf.plot(pdata[-numofdays:], type='candle', style='charles',
                addplot=[sma9dict, sma20dict, sma50dict, sma200dict, lowerbbdict, upperbbdict],
                figscale=.9,
                tight_layout=False,
                savefig=f'''/Users/mike/Desktop/ibkr_ma_chart/9-200SMA_{today_date}/{ticker}_{defining_ma}_{today_date}.pdf''')

def plot_j1(pdata, sma9, sma20, sma50, lowerbb, upperbb, numofdays, ticker, defining_ma):
    sma9dict = mpf.make_addplot(sma9['data'][-numofdays:], color='#c87cff')
    sma20dict = mpf.make_addplot(sma20['data'][-numofdays:], color='#f28c06')
    sma50dict = mpf.make_addplot(sma50['data'][-numofdays:], color='#3a7821')
    lowerbbdict = mpf.make_addplot(lowerbb['data'][-numofdays:], color='#b90c0c')
    upperbbdict = mpf.make_addplot(upperbb['data'][-numofdays:], color='#b90c0c')
    mpf.plot(pdata[-numofdays:], type='candle', style='charles',
                addplot=[sma9dict, sma20dict, sma50dict, lowerbbdict, upperbbdict],
                figscale=.9,
                tight_layout=False,
                savefig=f'''/Users/mike/Desktop/ibkr_ma_chart/9-200SMA_{today_date}/{ticker}_{defining_ma}_{today_date}.pdf''')

def plot_j2(pdata, sma9, sma20, lowerbb, upperbb, numofdays, ticker, defining_ma):
    sma9dict = mpf.make_addplot(sma9['data'][-numofdays:], color='#c87cff')
    sma20dict = mpf.make_addplot(sma20['data'][-numofdays:], color='#f28c06')
    lowerbbdict = mpf.make_addplot(lowerbb['data'][-numofdays:], color='#b90c0c')
    upperbbdict = mpf.make_addplot(upperbb['data'][-numofdays:], color='#b90c0c')
    mpf.plot(pdata[-numofdays:], type='candle', style='charles',
                addplot=[sma9dict, sma20dict, lowerbbdict, upperbbdict],
                figscale=.9,
                tight_layout=False,
                savefig=f'''/Users/mike/Desktop/ibkr_ma_chart/9-200SMA_{today_date}/{ticker}_{defining_ma}_{today_date}.pdf''')

def plot_j3(pdata, sma9, sma20, lowerbb, upperbb, numofdays, ticker, defining_ma):
    sma9dict = mpf.make_addplot(sma9['data'][-numofdays:], color='#c87cff')
    sma20dict = mpf.make_addplot(sma20['data'][-numofdays:], color='#f28c06')
    lowerbbdict = mpf.make_addplot(lowerbb['data'][-numofdays:], color='#b90c0c')
    upperbbdict = mpf.make_addplot(upperbb['data'][-numofdays:], color='#b90c0c')
    mpf.plot(pdata[-numofdays:], type='candle', style='charles',
                addplot=[sma9dict, sma20dict, lowerbbdict, upperbbdict],
                figscale=.9,
                tight_layout=False,
                savefig=f'''/Users/mike/Desktop/ibkr_ma_chart/9-200SMA_{today_date}/{ticker}_{defining_ma}_{today_date}.pdf''')

def plot_total(bucket, bucket_nickname):
    try:
        plot_d(pdata, sma9, sma20, sma50, sma200, lowerbb, upperbb, 120, bucket[security][0], bucket_nickname)
    except ValueError:
        try:
            plot_j1(pdata, sma9, sma20, sma50, lowerbb, upperbb, 120, bucket[security][0], bucket_nickname)
        except ValueError:
            try:
                plot_j2(pdata, sma9, sma20, lowerbb, upperbb, 120, bucket[security][0], bucket_nickname)
            except ValueError:
                try:
                    plot_j3(pdata, sma9, sma20, lowerbb, upperbb, 40, bucket[security][0], bucket_nickname)
                except ValueError:
                    print(f'''pdata: {len(pdata[-40:])}''')
                    print(f'''Closings: {len(closing_prices[-40:])}''')
                    print(f'''9SMA: {len(sma9['data'][-40:])}''')
                    print(f'''20SMA: {len(sma20['data'][-40:])}''')
                    print(f'''50SMA: {len(sma50['data'][-40:])}''')
                    print(f'''200SMA: {len(sma200['data'][-40:])}''')
                    print(f'''lowerBB: {len(lowerbb['data'][-40:])}''')
                    print(f'''upperBB: {len(upperbb['data'][-40:])}''')

hits = []


ib = IB()
ib.connect('127.0.0.1', 4001, clientId=1)

# path = os.getcwd()
# print(path)
path = f'''/Users/mike/Desktop/ibkr_ma_chart/9-200SMA_{today_date}'''
os.mkdir(path)

while True:
    for security in range(len(SMA9_securities)):
        ib.sleep(1)
        fetched_data = fetch_data(SMA9_securities[security][0], SMA9_securities[security][1], '365 D')
        closing_prices = extract_closing(fetched_data)
        sma9 = create_masubplot(9, closing_prices)
        if closing_prices[len(closing_prices)-1] < (1 * sma9['data'][len(sma9['data'])-1]):
            hits.append(SMA9_securities[security][0])
            sma20 = create_masubplot(20, closing_prices)
            sma50 = create_masubplot(50, closing_prices)
            sma200 = create_masubplot(200, closing_prices)
            lowerbb = create_lowerbb_subplot(closing_prices, 20, 2.5)
            upperbb = create_upperbb_subplot(closing_prices, 20, 2.5)
            pdata = reformat_IBdata(fetched_data, 120)
            plot_total(SMA9_securities, '9SMA')
        else:
            print(f'''{SMA9_securities[security][0]} not in buying range.''')
    print(hits)

    for security in range(len(SMA20_securities)):
        ib.sleep(1)
        fetched_data = fetch_data(SMA20_securities[security][0], SMA20_securities[security][1], '365 D')
        closing_prices = extract_closing(fetched_data)
        sma20 = create_masubplot(20, closing_prices)
        if closing_prices[len(closing_prices)-1] < (1 * sma20['data'][len(sma20['data'])-1]):
            hits.append(SMA20_securities[security][0])
            sma9 = create_masubplot(9, closing_prices)
            sma50 = create_masubplot(50, closing_prices)
            sma200 = create_masubplot(200, closing_prices)
            lowerbb = create_lowerbb_subplot(closing_prices, 20, 2.5)
            upperbb = create_upperbb_subplot(closing_prices, 20, 2.5)
            pdata = reformat_IBdata(fetched_data, 120)
            plot_total(SMA20_securities, '20SMA')
        else:
            print(f'''{SMA20_securities[security][0]} not in buying range.''')
    print(hits)

    for security in range(len(SMA50_securities)):
        ib.sleep(1)
        fetched_data = fetch_data(SMA50_securities[security][0], SMA50_securities[security][1], '365 D')
        closing_prices = extract_closing(fetched_data)
        sma50 = create_masubplot(50, closing_prices)
        if closing_prices[len(closing_prices)-1] < (1 * sma50['data'][len(sma50['data'])-1]):
            hits.append(SMA50_securities[security][0])
            sma9 = create_masubplot(9, closing_prices)
            sma20 = create_masubplot(20, closing_prices)
            sma200 = create_masubplot(200, closing_prices)
            lowerbb = create_lowerbb_subplot(closing_prices, 20, 2.5)
            upperbb = create_upperbb_subplot(closing_prices, 20, 2.5)
            pdata = reformat_IBdata(fetched_data, 120)
            plot_total(SMA50_securities, '50SMA')
        else:
            print(f'''{SMA50_securities[security][0]} not in buying range.''')
    print(hits)

    for security in range(len(SMA200_securities)):
        ib.sleep(1)
        fetched_data = fetch_data(SMA200_securities[security][0], SMA200_securities[security][1], '365 D')
        closing_prices = extract_closing(fetched_data)
        sma200 = create_masubplot(200, closing_prices)
        if closing_prices[len(closing_prices)-1] < (1 * sma200['data'][len(sma200['data'])-1]):
            hits.append(SMA200_securities[security][0])
            sma9 = create_masubplot(9, closing_prices)
            sma20 = create_masubplot(20, closing_prices)
            sma50 = create_masubplot(50, closing_prices)
            lowerbb = create_lowerbb_subplot(closing_prices, 20, 2.5)
            upperbb = create_upperbb_subplot(closing_prices, 20, 2.5)
            pdata = reformat_IBdata(fetched_data, 120)
            plot_total(SMA200_securities, '200SMA')
        else:
            print(f'''{SMA200_securities[security][0]} not in buying range.''')
    print(hits)

    for security in range(len(lowerBB_securities)):
        ib.sleep(1)
        fetched_data = fetch_data(lowerBB_securities[security][0], lowerBB_securities[security][1], '365 D')
        closing_prices = extract_closing(fetched_data)
        lowerbb = create_lowerbb_subplot(closing_prices, 20, 2.5)
        if closing_prices[len(closing_prices)-1] < (1 * lowerbb['data'][len(lowerbb['data'])-1]):
            hits.append(lowerBB_securities[security][0])
            sma9 = create_masubplot(9, closing_prices)
            sma20 = create_masubplot(20, closing_prices)
            sma50 = create_masubplot(50, closing_prices)
            sma200 = create_masubplot(200, closing_prices)
            upperbb = create_upperbb_subplot(closing_prices, 20, 2.5)
            pdata = reformat_IBdata(fetched_data, 120)
            plot_total(lowerBB_securities, 'LowerBB')
        else:
            print(f'''{lowerBB_securities[security][0]} not in buying range.''')
    print(hits)

    for security in range(len(upperBB_securities)):
        ib.sleep(1)
        fetched_data = fetch_data(upperBB_securities[security][0], upperBB_securities[security][1], '365 D')
        closing_prices = extract_closing(fetched_data)
        upperbb = create_upperbb_subplot(closing_prices, 20, 2.5)
        if closing_prices[len(closing_prices)-1] > (1 * upperbb['data'][len(upperbb['data'])-1]):
            hits.append(upperBB_securities[security][0])
            sma9 = create_masubplot(9, closing_prices)
            sma20 = create_masubplot(20, closing_prices)
            sma50 = create_masubplot(50, closing_prices)
            sma200 = create_masubplot(200, closing_prices)
            lowerbb = create_lowerbb_subplot(closing_prices, 20, 2.5)
            pdata = reformat_IBdata(fetched_data, 120)
            plot_total(upperBB_securities, 'UpperBB')
        else:
            print(f'''{upperBB_securities[security][0]} not in buying range.''')
    print(hits)

