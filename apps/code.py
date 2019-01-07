#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    code 发布和管理模块
"""

import datetime
import tornado.web
import tornado.database
from settings import db, NAVNUM
from libs import markdown
from tornado.escape import xhtml_escape
import sae.kvdb

md = markdown.Markdown(safe_mode=True)

sae.kvdb.Client().add('count_post_total',0)#post计数
class BaseHandler(tornado.web.RequestHandler):

    @property
    def kv(self):
        return sae.kvdb.Client()

    @property
    def login_stas(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None
        return True


class HomeHandler(BaseHandler):
    
    def get(self):
        #查询最新8个
        marker=self.kv.get('count_post_total')
        entries = self.kv.get_by_prefix('post_',limit=8, marker=marker-8 if marker>8 else 0)
        if not entries:
            self.redirect("/newcode")
            return
            '''
        results = self.db.query("SELECT COUNT(*) As code FROM entries") #results = {'code': 1L}
        count = results[0].code
        pages = (count - 1) / NAVNUM + 1
        '''
        pages=marker/8
        self.render("home.html", entries=entries, pages=pages, counts=marker)


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
        self.render("page.html", entries=entries, pages = pages, this=int(id),
            counts=count)


class EntryHandler(BaseHandler):
    
    def get(self, codeid):
        entry = self.kv.get('post_%s'%str(codeid))
        if not entry:
            raise tornado.web.HTTPError(404)
        self.render("entry.html", entry=entry)


class FeedHandler(BaseHandler):
    pass
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published "
                                "DESC LIMIT 10")
        self.set_header("Content-Type", "application/atom+xml")
        self.render("feed.xml", entries=entries)

#/newcode
class ComposeHandler(BaseHandler):
    
    def get(self):
        self.render("compose.html")
    # id title content time 
    def post(self):
        count=self.kv.get('count_post_total')+1
        self.kv.replace('count_post_total',count)
        title = xhtml_escape(self.get_argument("title"))
        #code = xhtml_escape(self.get_argument("code"))
        info = md.convert(self.get_argument("info"))

        check = self.get_argument("check", None)
        if check != "1984":
            self.redirect("/newcode")
            return
            
        self.kv.add('post_%d'%count,[count,title,info,datetime.datetime.now()])

        self.redirect("/%d"%count)


class DeleteHandler(BaseHandler):

    def post(self):
        if self.login_stas:
            #password = self.get_argument("password")
            num = self.get_argument("id")
            self.kv.delete('post_%s'%num)
            self.redirect("/")
        else:
            self.redirect("/%s"%num)
            

class UserLoginHandler(BaseHandler):
    #缺少get
    def post(self):
        password = self.get_argument("password")
        id = self.get_argument("id")
        e = self.db.get("SELECT * FROM entries WHERE id = %s", int(id))
        if checkuserpass(password, e["password"]):
            self.set_secure_cookie("codeid", str(id))
            self.redirect("/update/" + str(id))
        else:
            self.redirect("/" + str(id))
    
#未保存markdown之前的内容，只提供除info之外   
class UpdateHandler(BaseHandler):
    
    def get(self, codeid):
        cookie_codeid = self.get_secure_cookie("codeid")
        #逻辑有点问题
        if str(codeid) == cookie_codeid:
            code = self.kv.get('post_%s'%cookie_codeid)
            self.render("update.html", code=code)
        else:
            self.redirect("/%s"%cookie_codeid)
            
    def post(self, codeid):
        title = xhtml_escape(self.get_argument("title"))
        #code = xhtml_escape(self.get_argument("code"))
        info = md.convert(self.get_argument("info"))
        #鉴权太弱
        check = self.get_argument("check", None)
        if check != "1984":
            self.redirect("/newcode")
            return
            
        self.kv.replace('post_%d'%codeid,[codeid,title,info,datetime.datetime.now()])

        self.redirect("/%d"%codeid)

class debug(BaseHandler):
    pass
    def get(self,):
        results = self.db.query("SELECT COUNT(*) As code FROM entries")
        count = results[0].code
        self.write(str([results,count]))

        