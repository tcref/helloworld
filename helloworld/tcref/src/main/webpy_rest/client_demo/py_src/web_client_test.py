import urllib2

#url = 'http://localhost:7856/demk'   
url = 'http://106.14.57.192:7856/demk'

def get_zcm(param):
    f = urllib2.urlopen(url+'/'+param)
    ret = f.read()
    return ret
    


def get_zcm_requests(mkcode):    
    import requests 
    response = requests.get(url+'/'+mkcode)
    ret = response.text
    return ret
    
def parse_csv(filename):
    import pandas as pd
    df_data = pd.read_csv(filename)
    #for i, row in df_data[200:300].iterrows() :  
    
    for i, row in df_data.iterrows() : 
        print 'row =', row [0]
        mm =get_zcm_requests(row[0])
        print mm
        
    print 'df_data size = ', df_data.__len__()
    
    
    
    
if __name__ == '__main__':
#     input = '5D166BA3C4A11409B44F132B1D5D7B5F'
#     print get_zcm_requests(input)
    import time , timeit
    st = time.time()
    
    mkcode_file = 'markcode_001.csv'
    parse_csv(mkcode_file)
    elapsed = time.time() - st
    print 'total elapsed =', elapsed
#     import datetime
#     print datetime.datetime.utcfromtimestamp(time.time()).isoformat()