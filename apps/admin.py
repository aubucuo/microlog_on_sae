#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from code import BaseHandler
from libs.utils import hexpassword, checkpassword


class SiteStartHandler(BaseHandler):
    # self.kv.add('current_amount_of_users',0)
    def get(self):
        admin = self.kv.get('user_1')
        if not admin:
            self.render("start.html",tip='创建管理员')
        else:
            self.redirect("/")

    def post(self):
        email_adr = str(self.get_argument("email"))
        pswd1 = self.get_argument("password")

        password = hexpassword(pswd1)
        self.kv.add('user_%s' % email_adr, {
                    'email': email_adr, 'passwd': password, })
        self.redirect("/auth/login")


class LoginHandler(BaseHandler):

    def get(self):
        tip=0
        if self.current_user:
            self.redirect("/")
        elif self.get_argument("next", "/")!='/':
            tip='需要登录以继续'
        self.render("login.html", tip=tip)

    def post(self):
        email_adr = str(self.get_argument("email", None))
        password = self.get_argument("password")

        user = self.kv.get('user_%s' % email_adr)
        if user and checkpassword(password, user["passwd"]):
            self.set_secure_cookie("user", user["email"])
            self.redirect("/")
        else:
            self.render("login.html", tip='出错了')


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


