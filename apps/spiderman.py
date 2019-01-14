#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from code import BaseHandler
from libs.utils import hexpassword, checkpassword
import requests

class spiderpanelHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        spiderlist = self.kv.get_by_prefix(
            'spider_', limit=8, marker=count_for_msg[0]-8 if count_for_msg[0] > 8 else 0)
        entries = []
        for i in spiderlist:
            entries.append(i)

        self.render('spiderman.html', spider_counts=kv.get('count_for_spider')[0],entries=entries, tip=0)


class spidereditHandler(BaseHandler):
    def get(self):

    def post(self):
        title = str(self.get_argument("title"))
        url = str(self.get_argument("url"))
        header = str(self.get_argument("header"))
        cookie = str(self.get_argument("cookie"))
        if url != '':
            #add new spider
            c_f_s = self.kv.get('count_for_spider')
            self.kv.add('spider_%s' % title, [c_f_s[1], url, header, cookie, 0, 0])
            c_f_s[0] += 1
            self.kv.replace('count_for_spider', c_f_s)
            self.render("spiderman.html", tip='添加成功')
        else:
            #update cookie
            spiderinfo=self.kv.get('spider_%s'%title)
            spiderinfo[3]=cookie
            self.kv.replace('spider_%s'%title,spiderinfo)
            self.render("spiderman.html", tip='成功更新cookie')


class runspiderhandler(BaseHandler):
    def get(self):
        spider_list = self.kv.get_by_prefix('spider_')
        for spider in spider_list:
            if 'xiami' in spider[0]:
                spider[1][3]['t_sign_auth']+=1
            with requests.Session() as s:
                spider[1][5]=s.get(spider[1][1],headers=spider[1][2],cookies=spider[1][3])
                spider[1][4]+=1
                self.kv.replace(spider[0],spider[1])

        self.write('All done')