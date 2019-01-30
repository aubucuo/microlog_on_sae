#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from code import BaseHandler
from libs.utils import hexpassword, checkpassword
import requests

#spider_title :[index,url,header,cookies,running_time,response]

class spiderpanelHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        count_for_spider=kv.get('count_for_spider') #[count,index]
        spiderlist = self.kv.get_by_prefix(
            'spider_', limit=8, marker=str(count_for_spider[0]-8 if count_for_spider[0] > 8 else 0))
        entries = []
        for i in spiderlist:
            entries.append(i)

        self.render('spiderman.html', spider_counts=count_for_spider[0],entries=entries, tip=0)


class spidereditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('spideredit.html',tip=0)
    def post(self):
        title = str(self.get_argument("title"))
        url = str(self.get_argument("url"))
        header = str(self.get_argument("header",None))
        cookie = str(self.get_argument("cookie",None))
        for i in [header,cookie]:
            if 
        if url != '':
            #add new spider
            self.kv.add('spider_%s' % title, [title, url, header, cookie, 0, 0])
            self.render("spideredit.html", tip='Add spider success!')

        else:
            #update cookie
            spiderinfo=self.kv.get('spider_%s'%title)
            spiderinfo[3]=cookie
            self.kv.replace('spider_%s'%title,spiderinfo)
            self.render("spideredit.html", tip='Update cookie')


class spider_daily(BaseHandler):
    def get(self):

        spider_list = self.kv.get_by_prefix('spider_')
        #spider_list=generate(key:[value])
        
        '''
        ls = []
        for spider in spider_list:
            ls.append(spider[1][1])
        self.write(str(ls))
        return 
        '''

        resp = {}
        for spider in spider_list:
            with requests.Session() as s:
                spider[1][5]=s.get(spider[1][1],headers=spider[1][2],cookies=spider[1][3]).json()
                spider[1][4]+=1
                self.kv.replace(spider[0],spider[1])
                resp[spider[1][0]] = spider[1][5]

        self.write(resp)

