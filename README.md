This project is fork from [SerhoLiu/CodeShare](https://github.com/SerhoLiu/CodeShare).The database is [sae-kvdb](https://www.sinacloud.com/doc/sae/php/kvdb.html) (A simple nosql database)  You can deploy it on `GoogleAppEngine` `BaiduAppEngine` `Pythonanywhere.com`。


### 说明
- Why use nosql `sae-kvdb`?   
Because it's FREE on sae-platform ;)

### 数据结构
- user数据：  
```py
'user_%s' % email_adr, {
                    'email': email_adr, 'passwd': password, }
```
- 博文的数据结构：  
key: `msg_%d` value: [count,title,content,time] 
- （每日签到）爬虫的数据结构  
key: `spider_%d` value: [index, url, header, cookie, runningtime_count, response]
（爬虫默认一天执行一次）有需要可去[这里](https://www.sinacloud.com/doc/sae/services/cron.html)自行定制。


## 使用方法
1. 在 SAE 上新建 Python 应用，在`setting.py`中设置站点名，修改后上传
2. ~~开启MySQL服务，进入数据库，导入db.sql~~
3. 打开 http://youapp.sinaapp.com/admin/start 输入你的管理员帐号（为了安全，建议初始化后删除urls.py文件中的对应网址）


### License

See MIT-LICENSE.txt