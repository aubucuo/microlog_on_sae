#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from code import BaseHandler
from libs.utils import hexpassword, checkpassword


class spiderpanelHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        spiderlist=self.kv.get_by_prefix('spider_', limit=8, marker=count_for_msg[0]-8 if count_for_msg[0] > 8 else 0)
        self.render('spiderman.html',tip=0)

class spidereditHandler(BaseHandler):
    def get(self):
        