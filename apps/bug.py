#!/usr/bin/env python
# -*- coding: utf-8 -*-

from code import BaseHandler

class bugtool(BaseHandler):
    def get(self):
        headers1 = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Connection':'keep-alive',
'Host':'www.xiami.com',
'Origin':'http://www.xiami.com',
'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
'Referer':'http://www.xiami.com/',
'X-Requested-With':'XMLHttpRequest'
}
        cookies1 = {
'gid':'152040660952503'
, '_unsign_token':'46b721f2f8d65b0f742c45e6bdd977f3'
, 'UM_distinctid':'161ff4c3c13b43-07c010e1217f36-35465d60-c0000-161ff4c3c142880'
, 'cna':'uqJtEm3qbgYCATyrLR/sRi9d'
, 'bdshare_firstime':'1520406703723'
, 'XMPLAYER_volumeValue':'0.75'
, 'member_auth':'0zGfH95D6Gkxi6OQG98xe3BO5bGGHjbUkogBieR%2Bt1QqIIsONoGskquQQwxM2yiSr2FOUe%2FZjn4RJu8'
, 'user':'11743817%22aubucuo%22images%2Favatar_new%2F234%2F59fed76df1ff8_11743817_b_w162h162.png%220%2218479%22%3Ca+href%3D%27http%3A%2F%2Fwww.xiami.com%2Fwebsitehelp%23help9_3%27+%3ELv8%3C%2Fa%3E%2219%2228%225468%22c1411475fd%221522657888'
, '_xiamitoken':'1f7f1bdb2f8e8f106b6f9c1c7e9a67d9'
, 'CNZZDATA921634':'cnzz_eid%3D1298708-1520402537-null%26ntime%3D1523226749'
, 'CNZZDATA2629111':'cnzz_eid%3D42738943-1520406270-null%26ntime%3D1523230481'
, 't_sign_auth':'1'
,'isg':'BO_vs4YM6axine3FYd9u9o5cfgNVhEKzQfC5ygF8Yt5nUA5SCmdoBltG1kLuKBsu'
}
        self.kv.get('spider_xiami')