#!/usr/bin/env python
import web
import json

#import demkfunc
import os,sys,logging
import demkrest


logger = logging.getLogger( 'demk' )



def _set_logger(logDir=None):
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
    fh = logging.handlers.RotatingFileHandler( logDir + 'demk.log', maxBytes=1024*1024*10, backupCount=3 ) 
    logger.addHandler( fh )
    formatter = logging.Formatter( '%(asctime)s - %(filename)s line: %(lineno)d - [%(levelname)s] : %(message)s' )
    fh.setFormatter( formatter )
    logger.setLevel( logging.DEBUG )
    
    
    
PORT = '7856' #  default port     
def _get_port():
    with open('./demk.conf') as conf:
        for item in conf.readlines():
            #print item
            if item.strip().startswith('#') :
                continue
            prop = item.split('=')
            #print item, prop, '|',prop[0],prop[1]
            if prop[1] and prop[0].strip().lower() == 'PORT'.lower():
                PORT = prop[1]
    return PORT


if __name__ == "__main__":
    _set_logger()
    PORT = _get_port() #check for configuration

    curpath = os.getcwd()
    print curpath
    sys.path.append(curpath)
    sys.path.append( os.path.join(curpath,'demksvc'))

    try :        
        if sys.argv[1] and int(sys.argv[1].strip()) :
            PORT= str(sys.argv[1])
            pass
    except :
        pass
        
        
    msg = "Start serving at port %s" % PORT
    logger.info(msg)
    logger.info('os.environ='+str(os.environ))
    print msg        
    os.environ['PORT'] = PORT 
    '''
    #web.py specified in wsgi.py
    server_addr = validip(listget(sys.argv, 1, ''))
    if os.environ.has_key('PORT'): # e.g. Heroku
        server_addr = ('0.0.0.0', intget(os.environ['PORT']))
    '''
    demkrest.app.run()