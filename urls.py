#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps import code, admin

urls = [(r"/", code.HomeHandler),
        (r"/msg/(\d+)", code.EntryHandler),
        (r"/newcode", code.ComposeHandler),
        (r"/update/(\d+)", code.UpdateHandler),
        (r"/delete", code.DeleteHandler),
        (r"/page/(\d+)", code.PageHandler),
        (r"/auth/login", admin.LoginHandler),
        (r"/auth/logout", admin.LogoutHandler),
        (r"/admin/start", admin.SiteStartHandler),
        (r"/admin/delete/(\d+)", admin.DeleteHandler),
        (r"/feed", code.FeedHandler),
        (r"/dashboard",code.dashboard),
        (r'/debug',code.debug),]
