#!/usr/bin/env python
#coding:utf-8
from sqlalchemy import *
from toughlib.dbengine import get_engine
import json,os,gzip

class DBBackup:

    def __init__(self, sqla_metadata, excludes=[]):
        self.metadata = sqla_metadata
        self.excludes = excludes
        self.dbengine = self.metadata.bind

    def dumpdb(self, dumpfile):
        _dir = os.path.split(dumpfile)[0]
        if not os.path.exists(_dir):
            os.makedirs(_dir)

        with self.dbengine.begin() as db:
            with gzip.open(dumpfile, 'wb') as dumpfs:
                tables = {_name:_table for _name, _table in self.metadata.tables.items() if _name not in self.excludes}
                table_headers = ('table_names', tables.keys())
                dumpfs.write(json.dumps(table_headers, ensure_ascii=False).encode('utf-8'))
                dumpfs.write('\n')
                for _name,_table in tables.iteritems():
                    rows = db.execute(select([_table]))
                    for row in rows:
                        obj = (_name, dict(row.items()))
                        dumpfs.write(json.dumps(obj,ensure_ascii=False).encode('utf-8'))
                        dumpfs.write('\n')



    def restoredb(self,restorefs):
        if not os.path.exists(restorefs):
            print 'backup file not exists'
            return
        
        with self.dbengine.begin() as db:
            with gzip.open(restorefs,'rb') as rfs:
                cache_datas = {}
                for line in rfs:
                    try:
                        tabname, rdata = json.loads(line)
                        if tabname == 'table_names' and rdata:
                            for table_name in rdata:
                                print "clean table %s" % table_name
                                db.execute("delete from %s;" % table_name)
                            continue

                        if tabname not in cache_datas:
                            cache_datas[tabname] = [rdata]
                        else:
                            cache_datas[tabname].append(rdata)

                        if tabname in cache_datas and len(cache_datas[tabname]) >= 500:
                            print 'insert datas<%s> into %s' % (len(cache_datas[tabname]), tabname)
                            db.execute(self.metadata.tables[tabname].insert().values(cache_datas[tabname]))
                            del cache_datas[tabname]

                    except:
                        print 'error data %s ...'% line
                        raise

                print "insert last data"
                for tname, tdata in cache_datas.iteritems():
                    try:
                        print 'insert datas<%s> into %s' % (len(tdata), tname)
                        db.execute(self.metadata.tables[tname].insert().values(tdata))
                    except:
                        print 'error data %s ...' % tdata
                        raise

                cache_datas.clear()

    def restoredbv1(self,restorefs):
        if not os.path.exists(restorefs):
            print 'backup file not exists'
            return

        table_defines = {
            'slc_node' : 'tr_node',
            'slc_operator' : 'tr_operator',
            'slc_operator_nodes' : 'tr_operator_nodes',
            'slc_operator_rule' : 'tr_operator_rule',
            'slc_param' : 'tr_param',
            'slc_rad_bas' : 'tr_bas',
            'slc_member' : 'tr_customer',
            'slc_member_order' : 'tr_customer_order',
            'slc_rad_account' : 'tr_account',
            'slc_rad_product' : 'slc_product',
            'slc_rad_product_attr' : 'slc_product_attr',
        }

        with self.dbengine.begin() as db:
            with gzip.open(restorefs,'rb') as rfs:
                for line in rfs:
                    try:
                        obj = json.loads(line)
                        if obj['table'] not in table_defines:
                            continue
                        ctable = table_defines[obj['table']]
                        print "delete from %s"%ctable
                        db.execute("delete from %s"%ctable
                        print 'insert datas into %s'%ctable
                        objs =  obj['data']
                        if len(objs) < 500:
                            for o in objs:
                                if 'member_id' in o:
                                    o['customer_id'] = o['member_id']
                                    del o['member_id']
                            if objs:db.execute(metadata.tables[ctable].insert().values(objs))
                        else:
                            while len(objs) > 0:
                                _tmp_pbjs = objs[:500]
                                objs = objs[500:]
                                for o in objs:
                                    if 'member_id' in o:
                                        o['customer_id'] = o['member_id']
                                        del o['member_id']
                                db.execute(metadata.tables[ctable].insert().values(_tmp_pbjs))
                            
                        # db.execute("commit;")
                    except:
                        print 'error data %s ...'%line[:128] 
                        import traceback
                        traceback.print_exc()


if __name__ == '__main__':
    pass







