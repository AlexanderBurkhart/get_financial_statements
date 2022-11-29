import yahoo_fin.stock_info as si
import yahooquery as yq
from tqdm import tqdm
import math
import re
import sys
import time
import pandas as pd
from optparse import OptionParser

parser = OptionParser()
parser.add_option('--s', '--stock', dest='stock', help='Singular stock to get fundamentals, type in the ticker. (e.g. For apple type in: AAPL)', default='')
parser.add_option('--i', '--index', dest='index', help='Get all stocks from list of indexes. Supported ones are SP500 and Dow.', default='')
parser.add_option('--f', '--stock_file', dest='stock_file', help='Destination to file of listed stocks.', default='stocks.txt')
parser.add_option('--e', '--excel_name', dest='excel_name', help='Specify the name of the excel file of all financial data.', default='AutoFinancials.xlsx')
parser.add_option('--t', '--time_period', dest='time_period', help='Time period for financials. Type in q for quarter. Type in a for annual.', default='q')

(options, args) = parser.parse_args()
if len(options.stock) == 0 and len(options.index) == 0 and len(options.stock_file) == 0:
    print('ERROR: Please specify either a stock, index, or file of stock names you want for financial data')
    sys.exit()

def camel_to_spaces_cols(df):
    df.columns = pd.Index([re.sub("([a-z])([A-Z])","\g<1> \g<2>",col) for col in df.columns])

time_period = options.time_period.replace(' ', '')
if time_period != 'a' and time_period != 'q':
    print('ERROR: Please specify a proper timeperiod. Type in q for quarter and a for annual.')
    sys.exit()

# get all sp500 tickers
if len(options.stock_file) != 0:
    # read file
    try:
        with open(options.stock_file) as f:
            all_stocks = [line.replace(' ', '').replace('\n', '') for line in f]
    except Exception as e:
        print(e)
        print('Error when reading stock file, make sure the path to the file is correct and that the file is a valid text file of a list of stock names with one stock per line')
elif len(options.index) != 0:
    index = options.index.lower().replace(' ', '')
    if index == 'sp500':
        all_stocks = si.tickers_sp500()
    elif index == 'dow':
        all_stocks = si.tickers_dow()
    else:
        print('ERROR: %s not recognized as valid index, use one of the three valid options: SP500 DOW NASDAQ')
        sys.exit()
else:
    all_stocks = [options.stock.replace(' ', '')]

if len(all_stocks) > 100:
    print('WARNING: Reading many stocks\' financials may take some time.')

# loop through all tickers and get financials from each one
# maximum stocks to grab at once for data
SUBSET_LENGTH = 10
try:
    start = 0
    all_financials = None
    for i in tqdm(range(math.ceil(len(all_stocks)/SUBSET_LENGTH))):
        end = start+SUBSET_LENGTH
        if end > len(all_stocks):
            end = len(all_stocks)
        
        tickers = yq.Ticker(all_stocks[start:end])
        print('Getting balance sheets...')
        balance_sheets = tickers.balance_sheet(time_period)
        camel_to_spaces_cols(balance_sheets)
        print('Got balance sheets.\n')
        
        print('Getting income statements...')
        income_statements = tickers.balance_sheet(time_period)
        camel_to_spaces_cols(income_statements)
        print('Got income statements.\n')
        
        print('Getting cash flows...')
        cash_flows = tickers.cash_flow(time_period)
        camel_to_spaces_cols(cash_flows)
        print('Got cash flows.\n')
        
        stocks_financials = {
            'balance sheets': balance_sheets,
            'income statements': income_statements,
            'cash flows': cash_flows
        }
        if all_financials:
            all_financials['balance sheets'] = all_financials['balance sheets'].append(stocks_financials['balance sheets'])
            all_financials['income statements'] = all_financials['income statements'].append(stocks_financials['income statements'])
            all_financials['cash flows'] = all_financials['cash flows'].append(stocks_financials['cash flows'])
        else:
            all_financials = stocks_financials
        start = end
        time.sleep(5)
except Exception as e:
    print(e)
    print('ERROR: Issue reading some of the stocks (check your stock file if you are reading from one), could also be an API issue (run again if thats true)')
    sys.exit()

print('Creating excel file...')
# port to excel
with pd.ExcelWriter(options.excel_name, engine='xlsxwriter') as writer:
    for i in tqdm(range(len(all_stocks))):
        stock = all_stocks[i]
        all_financials['balance sheets'].loc[stock].T.to_excel(writer, na_rep = '-', sheet_name='%s Balance Sheet' % stock)
        
        all_financials['income statements'].loc[stock].T.to_excel(writer, na_rep = '-', sheet_name='%s Income Statement' % stock)
        
        all_financials['cash flows'].loc[stock].T.to_excel(writer, na_rep = '-', sheet_name='%s Cash Flows' % stock)
print('Excel file created.\n')
print('Downloaded all financial data in %s!' % options.excel_name)