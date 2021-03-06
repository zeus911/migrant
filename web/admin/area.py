#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
    server area  action
    author comger@gmail.com
"""

from kpages import url,mongo_conv
from kpages.model import ModelMaster
from utility import ActionHandler
from logic.pinying import get_pinyin


MArea = ModelMaster()('AreaModel')


@url(r"/admin/area")
class ServiceArea(ActionHandler):
    def get(self):
        pass


@url(r'/admin/area/list')
class ServerAreaList(ActionHandler):
    def get(self):
        page = int(self.get_argument('page',1))
        lst = MArea.page(page=page-1)
        npage = (MArea.count()+1)/10+1
        self.render('admin/arealist.html',data=lst, page=page,npage=npage)

@url(r"/admin/area/save")
class ServerAreaSave(ActionHandler):
    def post(self):
        try:
            obj = MArea.fetch_data(self)
            if not obj.get('listname',None):
                obj['listname'] = get_pinyin(obj['name'])
            
            obj['_id'] = self.get_argument('_id',None)
            if not obj['_id'] and MArea.exists(listname = obj['listname']):
                raise Exception('已存在域名:'+obj['listname'])

            r = MArea.save(obj) 
            self.write(dict(status=True, data = r))
        except Exception as e:
            self.write(dict(status=False, errmsg = e.message))

    def get(self):
        _id = self.get_argument("id", None)
        info = {}
        if _id:info = MArea.info(_id)
        self.render('admin/areainfo.html', info=info)

@url(r"/admin/area/delete")
class ServerAreaDelete(ActionHandler):
    def post(self):
        _id = self.get_argument("id", None)
        try:
            MArea.remove(_id)
            self.write(dict(status=True))
        except Exception as e:
            self.write(dict(status=False, msg= e.message))






