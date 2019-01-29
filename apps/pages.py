#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from code import BaseHandler

class homepage(BaseHandler):
    def get(self):
        self.render('home.html')

class dashboard(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("dashboard.html",tip=0)

    def post(self):
        key_prefix=str(self.get_argument("prefix")
        action = str(self.get_argument('checkbox'))
        if  action:
        
            keys_delete = self.kv.getkeys_by_prefix(key_prefix)
            count = 0
            for key in keys_delete:
                self.kv.delete(key)
                count+=1

            if 'msg' in key_prefix:
                current_msg_count=self.kv.get('count_for_msg')
                current_msg_count[0]-=count
                self.kv.replace('count_for_msg', current_msg_count)
            self.render("dashboard.html",tip='已删除%d条数据'%count)
        else:
            #select
            tip='查询：%s'%str(self.kv.get(key_prefix))
            self.render('dashboard.html',tip=tip)

