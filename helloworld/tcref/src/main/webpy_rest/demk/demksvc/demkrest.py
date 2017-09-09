#!/usr/bin/env python
import web
import json

import demkfunc
import os,sys,logging
#import demksvc

urls = (
    '/records/zcm', 'list_zcm',
    '/records/zcm/(.*)', 'get_zcm',
    '/records/mkcode', 'list_mkcode',
    '/records/mkcode/(.*)', 'get_mkcode',
    '/demk/(.*)', 'call_demk',
    '/','index',
    '/favicon.ico', 'Icon'
     
)
 
app = web.application(urls, globals())
logger = logging.getLogger( 'demk' )

class index:
    def GET(self):
        return 'Hello World'
        
class Icon:
    def GET(self):
        raise web.seeother('/static/pencil.png')

class list_zcm:        
    def GET(self):
        
        rows = demkfunc.query_db(demkfunc.list_zcm_sql)
        #print 'rows=',type (rows), rows
        
        output = [{'zcm': row['zcm'],'mkcode':row['mkcode']} for row in rows]
        #print 'output=',output
        return json.dumps(output)

class get_zcm:
    def GET(self, zcm):
        #print 'zcm=',type(zcm),zcm
        rows = demkfunc.query_db(demkfunc.get_by_zcm, [zcm]) #(demkfunc.get_by_zcm, (zcm,))
        output = [{'zcm': row['zcm'],'mkcode':row['mkcode']} for row in rows]
        return json.dumps(output)
        pass
        
class list_mkcode:
    def GET(self):
        
        rows = demkfunc.query_db(demkfunc.list_mkcode_sql)
        #print 'rows=',type (rows), rows
        
        output = [{'zcm': row['zcm'],'mkcode':row['mkcode']} for row in rows]
        #print 'output=',output
        return json.dumps(output)

class get_mkcode:
    def GET(self, mkcode):
        #print 'zcm=',type(mkcode),mkcode
        rows = demkfunc.query_db(demkfunc.get_by_mkcode, (mkcode,))
        output = [{'zcm': row['zcm'],'mkcode':row['mkcode']} for row in rows]
        return json.dumps(output)
        pass

class call_demk:
    def GET(self, mkcode):
        #print mkcode
        cip = web.ctx.ip
        print cip
        logger.info( 'cip='+ cip )
        m = demkfunc.invoke_demk(mkcode, cip)
        print 'call_demk return m=', m
        logger.info( 'call_demk_return m='+ str( m ))
        return json.dumps(m)