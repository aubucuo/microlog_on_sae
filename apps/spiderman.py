#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from code import BaseHandler
from libs.utils import hexpassword, checkpassword
import requests

#spider_title :[index,url,header,cookies,running_time,response]

class spiderpanelHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        count_for_spider=kv.get('count_for_spider') #[count,index]
        spiderlist = self.kv.get_by_prefix(
            'spider_', limit=8, marker=str(count_for_spider[0]-8 if count_for_spider[0] > 8 else 0))
        entries = []
        for i in spiderlist:
            entries.append(i)

        self.render('spiderman.html', spider_counts=count_for_spider[0],entries=entries, tip=0)


class spidereditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('spideredit.html',tip=0)
    def post(self):
        title = str(self.get_argument("title"))
        url = str(self.get_argument("url"))
        header = str(self.get_argument("header",None))
        cookie = str(self.get_argument("cookie",None))

        info = {"header":header,"cookie":cookie}
        for i in info:
            #{"key":"value","k":"v"}
            if ":" in info[i]:
                info[i] = map(lambda x : x.split(":") , info[i].strip('{},').split(","))
                d = {}
                for element in info[i]:
                    d[element[0].strip('" ')]=element[1].strip('" ')
                info[i] = d
            # k=v;k=v;
            elif "=" in info[i]:
                info[i] = map(lambda x : x.split("="), info[i].split(";").strip())
                d = {}
                for element in info[i]:
                    d[element[0].strip('" ')]=element[1].strip('" ')
                info[i] = d

            else:
                continue
        header = info['header']
        cookie = info['cookie']

        if url != '':
            #add new spider
            self.kv.add('spider_%s' % title, {"title":title, "url":url, "header":header, "cookie":cookie, "count":0, "response":0})
            self.render("spideredit.html", tip='Add spider success!')

        else:
            #update cookie
            spiderinfo=self.kv.get('spider_%s'%title)
            spiderinfo["cookie"]=cookie
            self.kv.replace('spider_%s'%title,spiderinfo)
            self.render("spideredit.html", tip='Update cookie')


class spider_daily(BaseHandler):
    def get(self):
        #spider_list=generate(key:[value])
        spider_list = self.kv.get_by_prefix('spider_')

        resp = {}
        for spider in spider_list:

            with requests.Session() as s:
                spider[1]["response"]=s.get(spider[1]["url"],headers=spider[1]["header"],cookies=spider[1]["cookie"] if len(spider[1]["cookie"]) > 10 else None).json()
                spider[1]["count"]+=1
                if "xiami" in spider[0]:
                    spider[1]["cookie"]["t_sign_auth"] = str(spider[1]["response"])

                self.kv.replace(spider[0],spider[1])
                resp[spider[1]["title"]] = spider[1]["response"]

        self.write(resp)

class yuque_webhook(BaseHandler):
    def get(self):
        with requests.Session() as s:
            url = "https://www.yuque.com/api/v2/repos/209206/toc"

            headers = {
        "Content-Type":"application/x-www-form-urlencoded",
        "User-Agent":"sae_plat",
        "X-Auth-Token": "Ozm3E1GEZetQISn2bmaBs1WlgWiDBryOPX2zpDaV",
        }
            docs = s.get(url,headers=headers).json()
            ls = []
            docs_count = len(docs['data']) if len(docs['data']) < 5 else 5
            for i in range(docs_count):
                ls.append({"slug":docs['data'][i]["slug"], "title":docs['data'][i]["title"].encode("u8") })

            self.kv.set("yuque_note_toc",ls)
            self.write(str(ls))

            
'''
class xiami_debug(BaseHandler):
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
, 't_sign_auth':'300'
,'isg':'BO_vs4YM6axine3FYd9u9o5cfgNVhEKzQfC5ygF8Yt5nUA5SCmdoBltG1kLuKBsu'
}
        xiami = self.kv.get('spider_xiami')
        xiami["cookie"] = cookies1
        xiami['header'] = headers1
        self.kv.replace('spider_xiami', xiami) 
        self.write(str(xiami))
'''
