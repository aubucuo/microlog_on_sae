#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from code import BaseHandler

class homepage(BaseHandler):
    def get(self):
        self.render('home.html')

