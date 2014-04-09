#!/usr/bin/python

import sqlalchemy.orm
import sqlalchemy.exc
from sqlalchemy.event import listen
try:
    import MySQLdb
except ImportError:
    pass
import os

if MySQLdb:
    def _ping_on_checkout(dbapi_con, con_record, con_proxy):
        cursor = dbapi_con.cursor()
        try:
            cursor.execute("SELECT 1")
        except MySQLdb.OperationalError, e:
            raise sqlalchemy.exc.DisconnectionError()
        else:
            cursor.close()

    def _setup_on_connect(dbapi_con, con_record):
        cursor = dbapi_con.cursor()
        cursor.execute("SET TIME_ZONE=%s", "+00:00")
        cursor.close()

def make_sessionmaker(dburi=None, echo=False):
    if dburi is None:
        with open(os.path.expanduser("~/.genav_connector.dburi"), "r") as f:
            dburi = f.read().strip()
    engine = sqlalchemy.create_engine(dburi, echo=echo, pool_recycle=3600)
    if MySQLdb and 'mysql' in engine.dialect.name:
        listen(engine, 'checkout', _ping_on_checkout)
        listen(engine, 'connect', _setup_on_connect)
    return sqlalchemy.orm.sessionmaker(bind=engine)
