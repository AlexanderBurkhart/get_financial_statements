- [Automate Retrieval of Financial Statements](#automate-retrieval-of-financial-statements)
  - [Set Up](#set-up)
    - [Dependencies](#dependencies)
      - [Install Python Dependencies](#install-python-dependencies)
  - [How To Use](#how-to-use)
    - [Arguments](#arguments)
  - [Financial Statements of a Group of Stocks](#financial-statements-of-a-group-of-stocks)
    - [Set Up File](#set-up-file)
    - [Run Automation](#run-automation)
  - [Financial Statements of One Stock](#financial-statements-of-one-stock)
  - [Financial Statements of an Index](#financial-statements-of-an-index)
  - [Excel Sheet](#excel-sheet)
  - [Time Period](#time-period)

# Automate Retrieval of Financial Statements
## Set Up
### Dependencies
Install Python 3.4<= [here](https://www.python.org/downloads/).

#### Install Python Dependencies
Run command in terminal to install required dependencies:

```pip install -r requirements.txt```

## How To Use
### Arguments
```
Options:
  -h, --help            show this help message and exit
  --s=STOCK, --stock=STOCK
                        Singular stock to get fundamentals, type in the
                        ticker. (e.g. For apple type in: AAPL)
  --i=INDEX, --index=INDEX
                        Get all stocks from list of indexes. Supported ones
                        are SP500 and DOW.
  --f=STOCK_FILE, --stock_file=STOCK_FILE
                        Destination to file of listed stocks.
  --e=EXCEL_NAME, --excel_name=EXCEL_NAME
                        Specify the name of the excel file of all financial
                        data.
  --t=TIME_PERIOD, --time_period=TIME_PERIOD
                        Time period for financials. Type in q for quarter.
                        Type in a for annual.
```

## Financial Statements of a Group of Stocks
### Set Up File
First, set up a text file with each line filled with one ticker of a stock of your choice. Example stocks.txt file is provided.

Example:
```
AAPL
MSFT
TSLA
AMD
NVDA
```

### Run Automation
Run the following command to get all financial statements of the group of stocks.
```
python3 main.py --f path_to_file_name_here
```

Example:
```
python3 main.py --f stocks.txt
```

## Financial Statements of One Stock
Run the following command to get the financial statements of a stock:
```
python3 main.py --s ticker_of_stock_here
```

Example:
```
python3 main.py --s AAPL
```

## Financial Statements of an Index
NOTE: Only supported indexes are the SP500 and Dow.
Run the following command to get the financial statements of all stocks in a supported index:
```
python3 main.py --s index_name_here
```

Example:
```
python3 main.py --i Dow
```

## Excel Sheet
After every execution, an excel file will be outputted with all the financial statements able to be retrieved.

The excel file by default is created in the same directory and will be named AutoFinancials.xlsx by default.

To change the name of the excel file add the following argument to the command:
```
--e new_excel_name_here.xlsx
```

Example:
```
python3 main.py --s AAPL --e newSheet.xlsx
```

## Time Period
Can retrieve either annual or quarterly data of a group of stocks. By default, the quarterly financial statements are being retrieved.

To specify either annual or quarterly data, add the following argument to the command:
For annual:
```
--t a
```
For quarter:
```
--t q
```

Example
```
python3 main.py --s AAPL --t a
```
