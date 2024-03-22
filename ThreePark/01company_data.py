import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import random


## sorting company by industry – we want to analyze by industry because there
## are industry standards for book to market, for example, that won't translate
## between industries
def sort_by_industry(df):
    by_industry = {}
    for index, row in df.iterrows():
        company = row['Symbol']
        industry = row['GICS Sector']

        if industry not in by_industry:
            by_industry[industry] = [company]
        else:
            by_industry[industry].append(company)

    return by_industry

by_industry = sort_by_industry(companies_df)
by_industry.keys()

## tested the code using pe_ratio, made up data for that here
## in real code, this piece of code will draw stock data and 
## combine that with imported data for other company and macro factors
def get_data(by_industry, factors):
    company_dataframes = {}

    for company_list in by_industry.values():
        for company in company_list:

            ticker = yf.Ticker(company)
            end_date = datetime.today()
            start_date = end_date - timedelta(days=365)

            stock_data = yf.download(company, start=start_date, end=end_date)

            info = ticker.info
            pe_ratio = info.get('trailingPE', None)

            if pe_ratio is None:
                print(f"No P/E ratio data for {company}")
                continue

            stock_data_with_pe = stock_data.copy()
            stock_data_with_pe['pe_ratio'] = pe_ratio

            for i in range(2, len(stock_data)):
                stock_data_with_pe.at[stock_data_with_pe.index[i], 'pe_ratio'] = \
                stock_data_with_pe.at[stock_data_with_pe.index[i-1], 'pe_ratio'] * random.uniform(0.95, 1.05)

            close_prices_with_pe = stock_data_with_pe[[factors]].copy() 
            
            company_dataframes[company] = close_prices_with_pe

    return company_dataframes

## creating company dataframes for each company in our list of companies
factors = ['Close', 'pe_ratio']
company_dataframes = get_data(by_industry, factors)