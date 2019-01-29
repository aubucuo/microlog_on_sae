#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps import code, admin ,spiderman ,pages

urls = [(r"/", pages.homepage),
        (r"/msg/(\d+)", code.EntryHandler),
        (r"/newmsg", code.ComposeHandler),
        (r"/page/(\d+)", code.PageHandler),
        (r"/auth/login", admin.LoginHandler),
        (r"/auth/logout", admin.LogoutHandler),
        (r"/admin/start", admin.SiteStartHandler),
        (r"/dashboard",code.dashboard),

        (r"/spider",spiderman.spiderpanelHandler),
        (r"/spideredit",spiderman.spidereditHandler),
        (r"/runspider",spiderman.runspiderhandler),

        (r'/debug',code.debug),]
