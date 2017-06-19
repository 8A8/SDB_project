# -*- coding: utf8 -*-
import psycopg2

class DateBase:
    def __init__(self,dbname='test', user='postgres', password='9764',host='localhost'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.conn = psycopg2.connect("host='" + host + "' dbname='" + dbname + "' user='" + user + "' password='" + password + "'")
        self.cur = self.conn.cursor()
        self.table = []

    def GetTable(self):
        self.cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
        temp = self.cur.fetchall()
        for a in temp:
            if a[0] != 'spatial_ref_sys' and a[0] != 'osm_line' and a[0] != 'osm_polygon' and a[0] != 'osm_point' :
                self.table.append(a[0])
        return self.table

    def SendQuery(self, query):
        self.cur.execute(query)

    def GetFetch(self):
        result = self.cur.fetchall()
        return result

    def GetAttr(self, TableName):
        self.cur.execute('SELECT * FROM "'+TableName+'";')
        colnames = [desc[0] for desc in self.cur.description]
        return colnames

    def Commit(self):
        self.conn.commit()

    def Disconnect(self):
        self.cur.close()
        self.conn.close()