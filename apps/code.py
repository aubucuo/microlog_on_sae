#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    msg 发布和管理模块
"""

from datetime import datetime
import tornado.web
from settings import NAVNUM
from libs import markdown
from tornado.escape import xhtml_escape
import sae.kvdb

md = markdown.Markdown(safe_mode=True)

sae.kvdb.Client().add('count_for_msg', [0,0])  # current count and index
sae.kvdb.Client().add('count_for_spider', [0,0])  # count,index

class BaseHandler(tornado.web.RequestHandler):

    @property
    def kv(self):
        return sae.kvdb.Client()

    def get_current_user(self):
        user_email = self.get_secure_cookie("user")
        return user_email


class HomeHandler(BaseHandler):

    def get(self):
        count_for_msg = self.kv.get('count_for_msg')
        if count_for_msg[0]==0:
            self.redirect('/newcode')
            return
        entries = self.kv.get_by_prefix('msg_', limit=8, marker='msg_%s'%str(count_for_msg[0]-8 if count_for_msg[0] > 8 else 0))
        #entries= generate ('msg_1', [1, u'1', u'1\n', datetime.datetime(2019, 1, 7, 15, 57, 35, 880823)])
        postlist = []
        for i in entries:
            postlist.append(i[1])
        self.render("home.html", entries=postlist[::-1],msg_counts=count_for_msg[0], tip=0)


class PageHandler(BaseHandler):
    pass

    def get(self, id):
        results = self.db.query("SELECT COUNT(*) As code FROM entries")
        count = results[0].code
        pages = (count - 1) / NAVNUM + 1
        offset = (int(id) - 1) * NAVNUM
        entries = self.db.query("""
            SELECT * FROM entries ORDER BY published DESC LIMIT 8 OFFSET %s
            """, offset)
        self.render("page.html", entries=entries, pages=pages, this=int(id),
                    counts=count)


class EntryHandler(BaseHandler):

    def get(self, codeid):
        entry = self.kv.get('msg_%s' % str(codeid))
        if not entry:
            raise tornado.web.HTTPError(404)
        self.render("entry.html", entry=entry, tip=0)


class ComposeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("compose.html",tip=0)
    # id title content time

    def post(self):
        title = xhtml_escape(self.get_argument("title"))
        content = md.convert(self.get_argument("content"))

        msg_id = map(lambda x :x+1,self.kv.get('count_for_msg'))
        self.kv.replace('count_for_msg', msg_id)
        self.kv.add('msg_%d'%msg_id[1], [msg_id[1], title, content, datetime.now().strftime( "%Y-%m-%d %H:%M:%S")])

        self.redirect("/msg/%d"%msg_id[1])
     

class debug(BaseHandler):
    def get(self):
        ls=[]
        self.kv.set('study/point',0)
        self.write('done')
