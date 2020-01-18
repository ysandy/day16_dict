"""
dict 服务端
功能：请求逻辑处理
并发模型：tcp，多进程并发
"""
import sys
from multiprocessing import Process
from socket import *
import signal
from time import sleep

from dict_db import Database

#全局变量
HOST ='0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

# 创建数据库连接
db = Database()

#处理注册
def do_register(connfd,name,passwd):
    if db.register(name,passwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'Fail')

#处理登录
def do_login(connfd,name,passwd):
    if db.login(name,passwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'Fail')


def do_query(connfd,name,word):
    db.insert_history(name, word)
    data = db.query(word)
    if data:
        msg = "%s : %s"%(word,data)
        connfd.send(msg.encode())
    else:
        connfd.send("单词不存在".encode())

#　历史记录
def do_history(connfd,name):
    #re  --> ((...),(...))  / ()
    re = db.history(name)# 获取历史记录
    if not re:
        connfd.send(b'Fail')
        return
    else:
        connfd.send(b'OK')
        for r in re:
            sleep(0.01)
            msg = "%s  %2s   %s" %r
            connfd.send(msg.encode())
        sleep(0.01)
        connfd.send(b'##')



def handle(connfd):
    while True:
        request = connfd.recv(1024).decode()
        tmp = request.split(' ')
        if not request or tmp[0] == 'E':  #客户端异常退出或者用户退出
            return
        elif tmp[0] == 'R':
            # R name passwd
            do_register(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'L':
            # L name passwd
            do_login(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'Q':
            # Q name word
            do_query(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'H':
            # H name
            do_history(connfd,tmp[1])



def main():
    #创建监听套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)
    #循环等待处理客户端连接
    print("listen the port 8000")
    while True:
        try:
            c,addr = s.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit("退出服务端")
        except Exception as e:
            print(e)
            continue

        #处理僵尸进程
        signal.signal(signal.SIGCHLD,signal.SIG_IGN)

        #为客户端创建进程
        p = Process(target=handle,args=(c,))
        p.start()

if __name__ == '__main__':
    main()


