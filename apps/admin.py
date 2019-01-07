#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from code import BaseHandler
from libs.utils import hexpassword, checkpassword


class SiteStartHandler(BaseHandler):
    #self.kv.add('current_amount_of_users',0)
    def get(self):
        admin = self.kv.get('user_1')
        if not admin:
            self.render("start.html")
        else:
            self.redirect("/")
    
    def post(self):
        email_adr = str(self.get_argument("email"))
        pswd1 = self.get_argument("password1")
        pswd2 = self.get_argument("password2")
    	
        if pswd1 != pswd2:
            self.redirect("/admin/start")
            return
        password = hexpassword(pswd1)
        self.kv.add('user_%s'%email_adr,{'email':email_adr,'passwd':password,})
        self.redirect("/auth/login")


class LoginHandler(BaseHandler):

    def get(self):
        if self.current_user:
            self.redirect("/")
            return
        self.render("login.html", msg=0)
    
    def post(self):
        email_adr = str(self.get_argument("email", None))
        password = self.get_argument("password")
        
        user = self.kv.get('user_%s'%email_adr)
        if user and checkpassword(password, user["passwd"]):
            self.set_secure_cookie("user", user["email"])
            self.redirect("/")
        else:
            msg = "Error"
            self.render("login.html", msg=msg)


class LogoutHandler(BaseHandler):
    
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


class DeleteHandler(BaseHandler):
    
    @tornado.web.authenticated
    def get(self, slug):
        code = self.kv.get('post_%s'%str(slug))
        if not code:
            raise tornado.web.HTTPError(404)
        else:
            self.kv.delete("post_%s"%str(slug))
            self.redirect("/")
