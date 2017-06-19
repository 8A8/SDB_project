# -*- coding: utf8 -*-
from Viewer import *
from DB_connector import *
from shapely import wkb


DB = DateBase(host='164.125.70.136', dbname='test2', user='postgres', password='as589578')
DB.GetTable()

viewer = Viewer(DB.table)

DB.SendQuery('SELECT * FROM "' + "parking" + '";')
data = DB.GetFetch()

T_list={}
colors = [(1.0, 0.8, 0.74, 1),  (0.88, 0.75, 0.91, 1),  (0.77, 0.79, 0.91, 1),  (0.7, 0.9, 0.99, 1),  (0.7, 0.92, 0.95, 1),  (0.78, 0.9, 0.79, 1) ,  (0.94, 0.96, 0.76, 1) ,  (1.0, 0.98, 0.77, 1) ,  (1.0, 0.93, 0.7, 1) ,  (1.0, 0.8, 0.74, 1) ,  (1.0, 0.88, 0.7, 1) ,  (0.84, 0.8, 0.78, 1) ,  (0.81, 0.85, 0.86, 1) ,  (0.97, 0.73, 0.82, 1) ,  (1.0, 0.8, 0.74, 1)]
idx = 0
for t in DB.table:
    items = []

    T_list[t] = DB.GetAttr(t)
    if 'line_way' in T_list[t]:
        DB.SendQuery('SELECT z_order,  (ST_Transform(line_way, 4326)) FROM "' + t + '"where line_way is not null;')
        data = DB.GetFetch()
        for d in data:
            item = {}
            item['zorder'] = d[0]
            item['object'] = wkb.loads(d[1], hex=True)
            items.append(item)
    if 'point_way' in T_list[t]:
        DB.SendQuery('SELECT z_order, (ST_Transform(point_way, 4326)) FROM "' + t + '" where point_way is not null;')
        data = DB.GetFetch()
        for d in data:
            item = {}
            item['zorder'] = d[0]
            item['object'] = wkb.loads(d[1], hex=True)
            items.append(item)
    if 'geom_way' in T_list[t]:
        DB.SendQuery('SELECT z_order, (ST_Transform(geom_way, 4326)) FROM "' + t + '"where geom_way is not null;')
        data = DB.GetFetch()
        for d in data:
            item = {}
            item['zorder'] = d[0]
            item['object'] = wkb.loads(d[1], hex=True)
            items.append(item)
    viewer.insert_object(t, items, colors[idx])

    idx+=1
    #for key, val in T_list[t]:


viewer.run()

DB.Disconnect()
