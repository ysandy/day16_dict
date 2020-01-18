import hashlib

import pymysql

# 传入一个密码返回加密后的密码
def change_passwd(passwd):
    hash = hashlib.md5()  # md5对象
    hash.update(passwd.encode())  # 加密
    return hash.hexdigest()

class Database:
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='123456',
                             database='dict',
                             charset='utf8')

        # 生成游标对象 (操作数据库,执行sql语句,获取结果)
        self.cur = self.db.cursor()

    def close(self):
        # 关闭游标和数据库连接
        self.cur.close()
        self.db.close()

    def register(self,name,passwd):
        sql = "select name from user where name='%s';"%name
        self.cur.execute(sql)
        #如果查到内容返回False
        if self.cur.fetchone():
            return False
        #插入数据库
        sql = 'insert into user (name,passwd) values (%s,%s);'
        passwd = change_passwd(passwd)  # 密码加密
        try:
            self.cur.execute(sql,[name,passwd])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def login(self,name,passwd):
        sql = "select name from user where name=%s and passwd=%s;"
        passwd = change_passwd(passwd)  # 密码加密
        self.cur.execute(sql,[name,passwd])
        #如果用户存在则返回True
        if self.cur.fetchone():
            return True
        else:
            return False

    def insert_history(self,name,word):
        # 插入查询记录到数据库
        sql = 'insert into hist1 (u_name,wd) values (%s,%s);'
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def query(self,word):
        sql = "select mean from word where wd=%s;"
        self.cur.execute(sql,[word])
        # 如果查到内容则插入查询记录
        r = self.cur.fetchone()
        if r:
            return r[0]
        else:
            return False

    def history(self,name):
        sql = "select u_name,wd,time from hist1 where u_name=%s order by time desc limit 10;"
        self.cur.execute(sql,[name])
        return self.cur.fetchall()   #fetchall() 有值，则是两层元组，没值，则是空元组



if __name__ == '__main__':
    db = Database()
    db.register('Tom','123')
    db.login('Tom','123')
    db.close()