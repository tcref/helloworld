import os
from subprocess import Popen, PIPE
import subprocess
import json
import logging, logging.handlers
from __builtin__ import str
import time
import cgi, cgitb
from sqlite_tool import connect_sqlite, close_sqlite
import datetime
import sqlite_tool


logger = logging.getLogger( 'demk' )
#----------- work new_new_cmd -----------
# new_cmd = dir+os.sep+fn+' '+param
# print new_cmd
# p = Popen(new_cmd)
#----------- work new_new_cmd -----------

db_path = './db'
db_file = 'demklog'
db_filepath = os.path.join(db_path, db_file)

create_log_table =  'CREATE TABLE IF NOT EXISTS \
        demklog(_id integer primary key  AUTOINCREMENT, \
        zcm varchar(20), mkcode varchar(80), client varchar(100), \
        verified varchar(5), [timestamp] timestamp )'
        

insert_log_sql =  'INSERT INTO demklog (zcm,mkcode,client,verified,timestamp) \
        values (?,?,?,?,?)'
        
list_zcm_sql = 'SELECT _id, zcm, mkcode from demklog group by zcm order by _id desc limit 1000'

list_mkcode_sql = 'SELECT _id, zcm, mkcode from demklog group by mkcode order by _id desc limit 1000'   

get_by_zcm = 'SELECT _id, zcm, mkcode from demklog where zcm=?'

get_by_mkcode  = 'SELECT _id, zcm, mkcode from demklog where mkcode=?'    
        
class TimeoutError(Exception): 
    pass


def popen_demk(exefile, mkcode, timeout=10):
    ret = {}
    out = ''
    #print mkcode
    param = mkcode.strip()
    p = None
    try:
        _st = time.time()
        elapsed = 0
        #logger.info(exefile)
        p = Popen([exefile, param],stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False )
        (data, stderr) = p.communicate()
        while True:
            if p.poll() is not None:
                break
            elapsed = time.time() - _st
            if timeout and elapsed > timeout :
                p.kill()
                p.terminate()
                raise TimeoutError('timeout')
        p.poll()

        ret['mkcode'] = param
        ret['zcm'] =  data.decode('ascii')#_ret[0]
        print 'zcm data=', data
        #err =  _ret[1]
        if len(stderr) > 0 :
            print  'size=',  len(stderr)
            print 'err=',stderr
            ret['cmd_err'] = stderr #_ret[1]

    except Exception as e:
        print 'exception=',e
        if len(str(e)) >0 :
            print e
            ret['exception'] = str(e)
        logger.error('['+mkcode+'] error on transforming ', e )

    if not p==None:
        p.terminate()
    
    
    logger.info( 'ret='+ str (ret) )
    return ret #out





def _set_logger(logDir=None):
    # TODO mutex locker
    logDir = './logs/'
    try:
        os.mkdir(logDir, 0o777)
    except:
        pass    
    if not os.path.exists(logDir):
        dataDir ='/temp/demklogs/'
    try:
        os.mkdir(logDir, 0o777)
    except:
        pass         
    console = logging.StreamHandler()
    logging.handlers
    fh = logging.handlers.RotatingFileHandler( logDir + 'demk.log', maxBytes=1024*1024*10, backupCount=3 ) 

    formatter = logging.Formatter( '%(asctime)s - %(filename)s line: %(lineno)d - [%(levelname)s] : %(message)s' )
    fh.setFormatter( formatter )
    logger.addHandler( fh )
    logger.setLevel( logging.DEBUG )


def invoke_demk(param, cip=None):
    #_set_logger()
    #print 'content-type:application/json \n\n'#'content-type:text/html \n\n'    
    try:
        f = check_db()
        #print 'db check=', f
        dir = os.getcwd() #os.path.abspath(os.curdir)  #os.getcwd()   #"C:\\eclipse_wk_space\\neon-test\\cgi\\cgi-bin\\"
        fn = "deMK-006"
        #param = " 00059B1C93C53400 " # 
        #param = "6CABD9B4C237EB13B44F132B1D5D7B5F " 
        #param =" 009763F220C61E7C "   # " 009763F2 20C61E7C "  # find ERROR input that cause previous exe popup msg box, there is a space in between.
        exefile = dir + os.sep + fn
        m = popen_demk(exefile, param, 10)  
        #m['client'] = cip      
    except Exception as e:
        logger.error('['+param+'] error on invoke', e )

    #print 'content-type:text/html \n\n'
    #print  json.dumps(m) 
    try:
        insert_a_record(m, cip)
    except Exception as e :
        logger.error('['+param+'] error on insert ', e )
    #del m['client']
    return m

def insert_a_record(json, client_ip):
    row = (json['zcm'],
           json['mkcode'],
           client_ip,
           '',
           datetime.datetime.utcfromtimestamp(time.time()).isoformat())
    write_db(row)
    return row

def check_db(): 
    _hasdb = False
    if not os.path.exists(db_path) :
        os.mkdir(db_path)
        logger.warn('db directory does not exist, create new')
    
    if os.path.isfile(db_filepath) :
        if os.path.getsize(db_filepath) > 100 :
            with open(db_filepath) as fd:
                db_header = fd.read(100)
                if db_header[:16] == 'SQLite format 3\x00' :
                    qdata = query_db('select count(*) from demklog')                    
                    if qdata and qdata[0] >0:    
                        return True
    else :
        try:
            
            conn , cur = connect_sqlite(db_filepath)
            cur.execute(create_log_table)
            close_sqlite(conn)
            _hasdb = True
        except:
            logger.error('Error on create table demklog. ')
            return False
    
    return _hasdb
        
        
        
def query_db(sql, value=[]):
    conn , cur = connect_sqlite(db_filepath)
    #print value, sql
    cur.execute(sql, value)
    data = cur.fetchall()#cur.fetchone()
    print 'row data=', data
    close_sqlite(conn) 
    return data
             
  
    
def write_db(myrow):
    conn = None  
    try:  
        conn , cur = connect_sqlite(db_filepath)
    
        cur.execute(insert_log_sql, myrow)
        conn.commit()
    except Exception as e:
        logger.error( e )
        logger.error( myrow )
    finally:
        close_sqlite(conn)
    #return True

if __name__ == '__main__':
    param = "6CABD9B4C237EB13B44F132B1D5D7B5F "
    mm = invoke_demk(param)
    print mm
            
            
