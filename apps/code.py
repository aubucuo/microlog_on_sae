#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    code 发布和管理模块
"""

from datetime import datetime
import tornado.web
import tornado.database
from settings import db, NAVNUM
from libs import markdown
from tornado.escape import xhtml_escape
import sae.kvdb

md = markdown.Markdown(safe_mode=True)

sae.kvdb.Client().add('count_post_total', 0)  # post计数


class BaseHandler(tornado.web.RequestHandler):

    @property
    def kv(self):
        return sae.kvdb.Client()

    @property
    def login_stas(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return False
        return True

    def get_current_user(self):
        user_email = self.get_secure_cookie("user")
        return user_email


class HomeHandler(BaseHandler):

    def get(self):
        count_post_total = self.kv.get('count_post_total')
        entries = self.kv.get_by_prefix('msg_', limit=8, marker=count_post_total-8 if count_post_total > 8 else 0)
        #entries= generate ('post_1', [1, u'1', u'1\n', datetime.datetime(2019, 1, 7, 15, 57, 35, 880823)])
        postlist = []
        while 1:
            try:
                postlist.append(next(entries)[1])
            except:
                break
        self.render("home.html", entries=postlist[::-1],msg_counts=count_post_total, tip=0)


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


class FeedHandler(BaseHandler):
    pass

    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published "
                                "DESC LIMIT 10")
        self.set_header("Content-Type", "application/atom+xml")
        self.render("feed.xml", entries=entries)


class ComposeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("compose.html",tip=0)
    # id title content time

    def post(self):
        msg_id = self.kv.get('count_post_total')+1
        self.kv.replace('count_post_total', msg_id)
        title = xhtml_escape(self.get_argument("title"))
        content = md.convert(self.get_argument("content"))
        self.kv.add('msg_%d'%msg_id, [msg_id, title, content, datetime.now().strftime( "%Y-%m-%d %H:%M:%S")])

        self.redirect("/msg/%d"%msg_id)

class DeleteHandler(BaseHandler):

    def post(self):
        if self.login_stas:
            #password = self.get_argument("password")
            num = self.get_argument("id")
            self.kv.delete('post_%s' % num)
            self.redirect("/")
        else:
            self.redirect("/%s" % num)


class UpdateHandler(BaseHandler):

    def get(self, codeid):
        cookie_codeid = self.get_secure_cookie("codeid")
        # 逻辑有点问题
        if str(codeid) == cookie_codeid:
            code = self.kv.get('post_%s' % cookie_codeid)
            self.render("update.html", code=code)
        else:
            self.redirect("/%s" % cookie_codeid)

    def post(self, codeid):
        title = xhtml_escape(self.get_argument("title"))
        #code = xhtml_escape(self.get_argument("code"))
        info = md.convert(self.get_argument("info"))
        # 鉴权太弱
        check = self.get_argument("check", None)
        if check != "1984":
            self.redirect("/newcode")
            return

        self.kv.replace('post_%d' %
                        codeid, [codeid, title, info, datetime.datetime.now()])

        self.redirect("/%d" % codeid)


class dashboard(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("dashboard.html",tip=0)

    def post(self):
        keys_delete = self.kv.getkeys_by_prefix(str(self.get_argument("prefix")))
        count = 0
        for key in keys_delete:
            self.kv.delete(key)
            count+=1
        # 添加“已删除”信息
        self.kv.replace('count_post_total',
                            self.kv.get('count_post_total')-count)
        self.render("dashboard.html",tip='已删除%d条数据'%count)


class debug(BaseHandler):
    def get(self,):
        num=self.kv.replace('count_post_total',
                            self.kv.get('count_post_total')-9)
        self.write(str(num))
