# -*- coding: utf-8 -*-
"""
Created on Fri May 25 09:20:25 2018
微博评论
@author: hndx
"""
from requests import session 
import random
from kvdb import kv,bkt
#from bs4 import  BeautifulSoup

'''
def _getnewduan():
    u = 'http://jandan.net/top-duan'
    c1 = s.get(u)
    soup = BeautifulSoup(c1.text,'html.parser') 
    p = soup.select('p')
    ls = []
    for i in range(3):
        ls.append(str(p[i]))
    kv.set('jiandantopduan',''.join(i+',' for i in ls))
    kv.set('jiandancount',3)
    return 'done'
'''
def _comment(wbid):
    s=session()
    u3 = 'https://api.weibo.com/2/comments/create.json'
    with open("static/tt.py", "r") as fo:
    	lis = fo.readlines() #土味情话
    kv.set('00jlwb_comments',kv.get('00jlwb_comments')+1)
    d3 = {"access_token":"2.00RebVPCdLgyYBbd316348cc8P6azD",  
      "comment":lis[random.randint(0,113)],
      'id':wbid  }
    rs = s.post(u3,data=d3)
    '''
    kv.set('jlwb_comments',kv.get('jlwb_comments')+1) #评论计数
    c = kv.get('jiandancount') #未使用的内容数
    if c == 0:
        _getnewduan()
        c = 3
    d3 = {"access_token":"2.00RebVPCdLgyYBbd316348cc8P6azD",  
      "comment":kv.get('jiandantopduan').split(',')[3-c], 
      'id':int(wbid) }
    rs = s.post(u3,data=d3)
    kv.set('jiandancount',c-1)
    '''
    return '%d\n=====\n%s'%(wbid,rs.text)

def _check(): #检查是否有新微博
    s=session()
    u7 = 'https://api.weibo.com/2/users/domain_show.json'
    d7 ={"access_token":"2.00RebVPCdLgyYBbd316348cc8P6azD",  
         'domain':'yjlyaoyao'   }
    r7 = s.get(u7,params=d7)
    j7 = r7.json()
    if kv.get('jlweibo') < j7["statuses_count"]: #如果有新微博
        kv.set('jlweibo',j7["statuses_count"])
        return _comment(j7['status']['id'])
    else:
        return str(j7)

def _jay(): #instagram搬运
    s=session()
    u2 = 'http://aubucuo.pythonanywhere.com/jay'
    s.get(u2)
    pic_url = 'http://aubucuo.pythonanywhere.com/static/jay.jpg'
    ask_url = 'http://aubucuo.pythonanywhere.com/ask'
    r = s.get(ask_url)   
    j = r.json()
    if not int(j['instagram'][0]): #是否有新内容
        return 'no new insta-Jay'
    else:
        kv.set('00jay_insta',kv.get('00jay_insta')+1)
        jay_text= j['instagram'][2]
        jay_link= j['instagram'][3]
        if j['instagram'][4] == '1':
            wb_content="[video]"+jay_text+" http://instagram.com/p/"+jay_link
        else:
            wb_content="[img]"+jay_text+" http://instagram.com/p/"+jay_link
            
        wb_url = 'https://api.weibo.com/2/statuses/share.json'
        d2 = {"access_token":"2.00RebVPCdLgyYBbd316348cc8P6azD",  
        "status": wb_content }
        
        jay_pic = s.get(pic_url)
        open('/s/jay/jay.jpg', 'wb').write(jay_pic.content)
        files={"pic":open("/s/jay/jay.jpg","rb") }  
        rs = s.post(wb_url,data=d2,files=files)
        
        return rs.content

