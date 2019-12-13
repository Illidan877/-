1. 安装定时任务包：

```
pip install django-crontab
```

2. 设置settings.py

```
INSTALLED_APPS = (
    'django_crontab',
    ...
)
```

3.  创建应用下的 cron.py	(任务)
4. 在django项目的**settings.py**中添加以下命令

```python
CRONJOBS = (
    ('*/2* * * *', '你的app名.定时函数所在的py文件名.定时函数名'),
    ('*/2* * * *', '你的app名.定时函数所在的py文件名.定时函数名', '>>/路径/log.log'),
)
```

5. 启动/停止
   1. python3 manage.py crontab add
   2. python3 manage.py crontab show
   3. python3 manage.py crontab remove(删除所有)



django-crontab 封装的crontab

| f1   | f2   | f3   | f4   | f5   |
| ---- | ---- | ---- | ---- | ---- |
| 分   | 时   | 日   | 月   | 周   |
| 1~59 | 0~23 | 1~31 | 1~12 | 0~6  |

用法:

1. *表示每分钟都要执行；
2. */n表示每n分钟执行一次；
3. [a-b]表示从第a分钟到第b分钟这段时间要执行；
4. a,b,c,...表示第a,b,c分钟要执行

















