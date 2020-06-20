import requests
import re
import json
import pandas as pd 

url = "http://fund.eastmoney.com/js/fundcode_search.js"
#发送get请求
r = requests.get(url)

cont = re.findall('var r = (.*])', r.text)[0]  # 提取list
ls = json.loads(cont)  # 将字符串个事的list转化为list格式
all_fund_code = pd.DataFrame(ls, 
                             columns=['基金代码', '基金名称缩写', '基金名称', '基金类型', '基金名称拼音'],
                             dtype = 'str')
all_fund_code.to_csv('/Users/Roy/Documents/Investment/Investment/FoF/data/allfundcode.csv',
                     index = False,
                     encoding="utf_8")
