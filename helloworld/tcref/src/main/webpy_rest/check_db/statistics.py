import pandas as pd
import sqlite3


def connect_sqlite(db_file):
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur
        
        
def get_dataframe(db_file, sql):
    conn, cur = connect_sqlite(db_file)
    df = pd.read_sql(sql,conn)
    if conn:
        conn.close()
        
    return df

def req_count(df):
    '''
        df : pandas dataframe
    '''
    df['datatime']


if __name__ == '__main__' : 
    db_file = 'demklog_2017-01-21'
    sql = 'select * from demklog '  
    df = get_dataframe(db_file, sql)
    #print df.head()

    df.plot()
#     df_tm = pd.TimeSeries( pd. to_datetime( df['timestamp'] ) )
#     print 'type df_tm=', type(df_tm),df_tm.head()
    
#     ddtest =  df['timestamp']
# 
# #    dd1.resample('M')
#     print type(ddtest), ddtest [800:810]
#     print ddtest.resample('H')