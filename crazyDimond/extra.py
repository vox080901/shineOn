import redis
import re
import time
from hashlib import md5
from .models import User
from rest_framework.views import Response

class Reserializer(object):

    def __init__(self, lis):
        self.lis = lis

    def fileReserializer(self, years_list, *args, **kwargs):
        """
        重新序列化api--->files的数据, 返回新的数据结构

        [OrderedDict([('pk', 2), ('create_date', '2018-12-13'),
        ('title', 'orm')]),
        OrderedDict([('pk', 3),
        ('create_date', '2018-12-14'), ('title', '中间件')]),
        OrderedDict([('pk', 4),
        ('create_date', '2018-12-14'), ('title', 'RESTful01')])]

        :param lis:
        :param args:
        :param kwargs:
        :return:
        """
        year_set = set()
        res = []
        for i in range(len(self.lis)):
            """
            记录res的长度, 如果长度变化说明增加了新年份, 
            因为已经在视图中进行过排序, 所以不会出现年份混杂在一起的情况
            每增加一个新年份, 则else中的res[index_res-1]向后移动一次
            """
            index_res = len(res)
            year = self.lis[i].get("create_date").split("-")[0]
            # print("="*40,year)
            # print("="*40,res)
            if year not in year_set:  # 如果是一个res中没有的年份, 就添加
                res.append({
                    "years": years_list,
                    "year": year,
                    "article": [
                        {"pk": self.lis[i].get("pk"),
                         "title": self.lis[i].get("title"),
                         "create_date": self.lis[i].get("create_date").split(year + "-")[-1],
                         },
                    ],
                })
            else:  # res中已经添加过该年份,说明当前循环对象与上一次循环的对象年份相同, 直接修改article即可
                res[index_res-1]["article"].append({"pk": self.lis[i].get("pk"),
                                                    "title": self.lis[i].get("title"),
                                                    "create_date": self.lis[i].get("create_date").split(year + "-")[-1],
                                                    })
            year_set.add(year)
        return res

    def cat4ArtReserializer(self, item_name, flag=False, *args, **kwargs):
        if flag:
            for i in self.lis:
                i["category"] = item_name.get("title")
        else:
            for i in self.lis:
                i["tag_name"] = item_name.get("tag_name")
        return self.lis

    @classmethod
    def tagAndCatReserializer(self, catnum, tagnum, *args, **kwargs):
        res = []
        res.append({"catnum": catnum, "tagnum": tagnum})
        return res

class Authentication(object):
    def __init__(self, account):
        self.account = account

    def tokenMaker(self):
        m = md5()
        m.update((str(time.time())+self.account).encode("utf-8"))
        token = m.hexdigest()
        return token

class UserInfoVerification(object):

    def __init__(self, user_name, account, password, confirm_pass, authcode, ip_addr):
        self.user_name = user_name
        self.account = account
        self.password = password
        self.confirm_pass = confirm_pass
        self.authcode = authcode
        self.ip_addr = ip_addr

    def verify(self):
        r = redis.Redis(host="127.0.0.1", password="123456")
        msg = {}
        try:
            mail_auth_code = r.get(self.account).decode()
        except AttributeError as e:
            msg["mail"] = "1"
        else:
            if self.authcode != mail_auth_code:
                msg["authcode"] = "1"
            if len(User.objects.filter(account=self.account)):
                msg["account"] = "1"
            if len(self.user_name)==0 or len(User.objects.filter(user_name=self.user_name)):
                msg["user_name"] = "1"
            if not re.match(r"[^\u4e00-\u9fa5]{3,10}", self.user_name):
                msg["user_name_code"] = "1"
            if self.password != self.confirm_pass:
                msg["confirm"] = "1"
            if not re.match(r"([a-zA-Z\d.\-+*/!@#$%^&()]){6,20}", self.password):
                msg["password"] = "1"
            if not re.match(r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}', self.account):
                msg["email"] = "1"
            if not self.ip_addr:
                msg["ip_addr"] = self.ip_addr
        finally:
            if not len(msg):
                self.user_name = self.user_name.strip()
                user = User.objects.create(user_name=self.user_name, account=self.account,
                                           ip_addr=self.ip_addr, password=self.password,
                                           )
                return user
            else:
                return msg

class UporDownVerification(object):
    pass
