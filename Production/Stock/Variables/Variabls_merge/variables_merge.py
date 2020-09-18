# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 15:32:07 2020

@author: Lenovo
"""

import pandas as pd
import logging
from sqlalchemy import create_engine
import traceback

class VariableMerge():
    """
    Class for merge stocks variable to one table for quantile calculation
    
    Parameters
    --------
        data_base_address : str
            Database address for data storage

        
    Attributes
    --------
    
    error_columns : list
        Error occured during columns calculation
        

    Notes
    --------
    """
    
    def __init__(self, data_base_address, data_base_name, filename = 'stock_daily_capital_flow.log'):
        
        self.data_base_address = data_base_address
        self.data_base_name = data_base_name
        # build up database connection
        self.conn = create_engine(self.data_base_address, encoding ='utf8')

        logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=filename,
                filemode='a')


    def variable_data_merge(self):
        """
        Downloadind data from Tushare database and save them to the database
        
        Parameters
        --------
            adj : str
            None, qfq or hfq.
                
        Returns
        --------
            error_ticks: list
                Ticks that can't get responded from the Tushare server. 
    
        Notes
        --------
        """
        
        # get all tables name        
        conn = create_engine(self.data_base_address, encoding ='utf8')
        cur = conn.execute('''SHOW TABLES''')
        tables_name = cur.fetchall()
            
        # get table column names 
        sql_cmd = "SELECT * FROM `" + tables_name[0][0] + '`;'
        daily_price = pd.read_sql(sql = sql_cmd, con = conn)
        temp_data = pd.read_sql(sql = sql_cmd, con = conn)
        columns = temp_data.columns[2:]

        # build column dataframe
        for column in columns:
            script = column + '=pd.DataFrame()' 
            exec(script)
        
        # merge all data with the same column
        i = 0
        for name in tables_name:
            i += 1
            print(i)
            name = name[0]
            sql_cmd = "SELECT * FROM `" + name + '`;'
            daily_price = pd.read_sql(sql = sql_cmd, con = conn)
            
            for column in columns:
                target_data = daily_price[['trade_date',column]]
                column_name = column + '_' + name
                target_data = target_data.rename(columns = {column : column_name})
                merge_script = """
if len( """+ column + """) == 0:
    """+ column + """ = target_data.copy()
else:
    """+ column + """ = pd.merge("""+ column + """,target_data,on = 'trade_date', how = 'outer')
"""
                exec(merge_script)

        # saving 
        error_columns = []
        for column in columns:
            try:
                sec_half_script = "'" + column + "'" + ", conn,index = None,if_exists = 'replace')"
                saving_script = "pd.io.sql.to_sql(" + column + ", "  + sec_half_script
                exec(saving_script)
            except ValueError:
                error_columns.append(column)
        
    
        if not error_columns:
            log_info = self.data_base_name + ' variable merge ssuccessfully!'
            logging.info(log_info)

        else:
            logging.warning('Some volumns merged failed, check error ticks----' + self.data_base_name)
            logging.warning(str(error_columns))
        return error_columns
        
    def run(self):
        '''
        
        running

        '''
        
        try:
            self.variable_data_merge()

        except Exception:
            logging.error("错误日志：\n" + traceback.format_exc())


        

if __name__ == '__main__':
    
    '''-----------set up-----------'''    # set data_base_address
    data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stock_daily_capital_flow'
    
    '''-----------merge stocks variables-----------'''
    vm = VariableMerge(data_base_address,data_base_name = 'Stock_daily_capital_flow')
    vm.run()
    

        

