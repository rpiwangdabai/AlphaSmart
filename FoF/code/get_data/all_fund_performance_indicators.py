#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 00:48:01 2020

@author: Roy
"""

from dataapi_win36 import Client
import sys
import json
import pandas as pd

class fund_data():
    """
    Return the data of the fund.
    
    Input
    -------------

        ticker : list
            fund ticker.
    
    Output
    -------------
        DataFrame:
            Fund performance.
            Fund Info
    """
    def __init__(self,tickers):
        self.tickers = tickers
        self.data = None
        self.data_df = None
        self.ticker = None
    
    def get_data(self,url):
        try:
            client = Client()
            client.init('1baefd826e7832aa413a1ee278342380fcbc6302fc5ae371d56d0573fd228cfa')
            url1 = url
            code, result = client.getData(url1)
            if code == 200:
                self.data = result.decode('utf-8')
                return self.data
            else:
                try:
                    sys.exit(0)
                except:
                    print('Program is dead.')
                    print (code)
                    print (result) 
        except Exception as e:
            #traceback.print_exc()
            raise e
           
    def row_data_transform_init(self):
        ls = json.loads(self.data)
        data_dict = ls['data'][0]
        self.data_df = pd.DataFrame(columns = data_dict.keys())
        self.data_df = self.data_df.append(data_dict, ignore_index = True)
        return 
    
    def row_data_transform_extend(self):
        ls = json.loads(self.data)
        data_dict = ls['data'][0]
        self.data_df = self.data_df.append(data_dict, ignore_index = True)
        return
    
    def fund_perf(self):
        # create datafram by using first fund in fund list 
        self.ticker = str(self.tickers[0])
        self.ticker = self.ticker.zfill(6)
        url = '/api/fund/getFundPerfIndic.json?field=&beginDate=20180327&endDate=20180327&secID=&ticker=' + self.ticker + '&dataDate=&window=8'
        self.get_data(url)
        self.row_data_transform_init()
        # append rest fund in fund list
        tickers = self.tickers
        for ticker in tickers[1:]:
            try:
                self.ticker = str(ticker).zfill(6)
                url = '/api/fund/getFundPerfIndic.json?field=&beginDate=20180327&endDate=20180327&secID=&ticker=' + self.ticker + '&dataDate=&window=8'
                self.get_data(url)
                self.row_data_transform_extend()
            except Exception:
                pass

        return self.data_df
    
    def fund_info(self):
        # create datafram by using first fund in fund list 
        self.ticker = str(self.tickers[0])
        self.ticker = self.ticker.zfill(6)
        url = '/api/fund/getFund.json?field=&secID=&ticker=' + self.ticker + '&etfLof=&listStatusCd=&category=&operationMode=&idxID=&idxTicker='
        self.get_data(url)
        self.row_data_transform_init()
        # append rest fund in fund list
        tickers = self.tickers
        for ticker in tickers[1:]:
            try:
                self.ticker = str(ticker).zfill(6)
                url = '/api/fund/getFundPerfIndic.json?field=&beginDate=20180327&endDate=20180327&secID=&ticker=' + self.ticker + '&dataDate=&window=8'
                self.get_data(url)
                self.row_data_transform_extend()
            except Exception:
                pass

        return self.data_df
        
        
        
if __name__ == "__main__":
    fund_tickers = pd.read_csv('/Users/Roy/Documents/Investment/Investment/FoF/data/allfundcode.csv')
    ticker = fund_tickers['基金代码']
    result = fund_data(ticker)
    # #fund perf
    # r = result.fund_perf()
    #fund info
    r = result.fund_info()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    