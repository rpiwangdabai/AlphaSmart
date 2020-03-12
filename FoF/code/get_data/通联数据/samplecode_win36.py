# -*- coding: utf-8 -*-
from dataapi_win36 import Client
if __name__ == "__main__":
    try:
        client = Client()
        client.init('1baefd826e7832aa413a1ee278342380fcbc6302fc5ae371d56d0573fd228cfa')
        url1='/api/fund/getFund.json?field=&secID=&ticker=000001&etfLof=&listStatusCd=&category=&operationMode=&idxID=&idxTicker='
        code, result = client.getData(url1)
        if code==200:
            a = result.decode('utf-8')
        else:
            print (code)
            print (result)
#        url2='/api/equity/getSecST.csv?field=&secID=&ticker=000521&beginDate=20020101&endDate=20150828'
#        code, result = client.getData(url2)
#        if(code==200):
#            file_object = open('thefile.csv', 'w')
#            file_object.write(result.decode('GB18030'))
#            file_object.close( )
#        else:
#            print (code)
#            print (result) 
    except Exception as e:
        #traceback.print_exc()
        raise e