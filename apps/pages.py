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
        key_prefix=str(self.get_argument("prefix"))
        checked = self.get_argument('check',None)
        if  checked:
            keys_delete = self.kv.getkeys_by_prefix(key_prefix)
            count = 0
            for key in keys_delete:
                self.kv.delete(key)
                count+=1

            if 'msg_' in key_prefix:
                current_msg_count=self.kv.get('count_for_msg')
                current_msg_count[0]-=count
                self.kv.replace('count_for_msg', current_msg_count)
            
            self.render("dashboard.html",tip='Delete %d kv'%count)
        else:
            #select
            if key_prefix[-1] is '_':
                g = self.kv.get_by_prefix(key_prefix)
                postlist = []
                for i in g:
                    postlist.append(i[0])
                tip = 'These keys start with the prefix: %s'% str(postlist)
            else:
                tip='Query result：%s'%str(self.kv.get(key_prefix))
            self.render('dashboard.html',tip=tip)

