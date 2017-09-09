from sqlite_tool import connect_sqlite, close_sqlite
import json
import pandas as pd
import datetime
import dateutil.tz
from pandas.io.tests.parser import quoting
import csv

#db_file = 'C:\\eclipse_wk_space\\neon-test\\webpy_rest\\demk\\demksvc\\db\\demklog'
db_file = 'demklog_2017-01-21'

def read_db(num = 1000):
    conn, cur = connect_sqlite(db_file)
    
    sql = 'select * from demklog order by _id desc limit ' +str(num)
    
    cur.execute(sql)
    data = cur.fetchall()
    
    close_sqlite(conn)
    return data

def write_to_csv(filename, rows):
    with open(filename, 'w') as f :
    #with open('./fetched.csv', 'w') as f :
        output = [f.write (json.dumps({'_id':r['_id'],'zcm': r['zcm'],'mkcode':r['mkcode'], 'from_ip': r['client'], 'timestamp': r['timestamp']})+', \n') for r in rows]
        #f.write (json.dumps(output))
    print 'write to csv finished.'
    
# def _to_local_zone(datetime_in_utc): #utcfromtimestamp
#     
#     local = datetime_in_utc.astimezone(dateutil.tz.tzlocal())
#     import pytz
#     tz_cn = pytz.timezone("Asia/Shanghai")
#     return 
    
# using PANDAS to dealwith sqlite db
def  read_db_2_dataframe(sql, limit_num=1000): 
    '''
        , pickup db data and then write to a csv file. 
        default sql = 'select * from demklog  order by zcm '
        default limit rows =1000
    '''  
    if (not sql == None) and sql.strip().lower().endswith('limit %d'):
        sql += ' limit ' +str(limit_num)
    conn , cur = connect_sqlite(db_file)    
    df = pd.read_sql(sql, conn)
    close_sqlite(conn)
    #----------write to csv file------------
    #df.to_csv(output, index=None)
    print 'get df=', df.head(100)
    return df


        
if __name__ == '__main__' :
#     data = read_db(10000)
#     filename = 'output/fetched.csv'
#     write_to_csv(filename, data)
#     print 'done!'

    #----------ok ---------
    sql = 'select _id, zcm, mkcode, client, Datetime(timestamp,\'localtime\') timestamp from demklog  order by zcm ' 
    outputcsv = 'output/zcm_ordered_0121a.csv'
    df = read_db_2_dataframe(sql,1500000)
    df.to_csv(outputcsv, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, quotechar='\'', index=False)
    print type(df['timestamp'][5]), df['timestamp'][5:12]
#    print df.head(5),'\n=====\n',df.tail(5),'\n\nDone!'
#-----------------------
 
    #-----------ok------------
    client_ip = '182.150.59.216'
    sql2 = 'select _id, zcm, mkcode, client, Datetime(timestamp,\'localtime\') timestamp  from demklog where client=\''+client_ip+'\' order by _id desc  '
    output2 = 'output\\fetched_0121a.csv'
    df2 = read_db_2_dataframe(sql2, 1500000)
    df2.to_csv(output2, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, quotechar='\'', index=None)

    #--------ok--------
    sql3 = 'select count(*) cnt, client from demklog group by client '
    output3 = 'output\\ip_lists_0121a.csv'
    df3 = read_db_2_dataframe(sql3, 1500000)
    df3.to_csv(output3, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC, quotechar='\'', index=None)    
    
    