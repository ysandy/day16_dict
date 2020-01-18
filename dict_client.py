import sys
from socket import *
from getpass import getpass
#服务器地址
ADDR = ('127.0.0.1',8000)

#套接字作为全局变量
s = socket()
s.connect(ADDR)

#注册功能
def do_register():
    while True:
        name = input("user:")
        passwd = getpass("passwd:")
        passwd1 = getpass("Again:")
        if passwd1 != passwd:
            print("两次密码不一致")
        if (" " in name) or (' ' in passwd):
            print("用户名密码不能有空格")
            continue

        msg = "R %s %s" %(name,passwd)
        s.send(msg.encode()) #发送请求
        data = s.recv(128).decode()
        if data == 'OK':
            print("注册成功")
            login()
        else:
            print('注册失败')
        return

def do_login():
    name = input("user:")
    passwd = getpass("passwd:")

    msg = "L %s %s"%(name,passwd)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        print("登录成功")
        login(name)
    else:
        print('登录失败')


def do_query(name):
    while True:
        word = input("输入单词：")
        if word == '##':
            break
        msg = "Q %s %s"%(name,word)
        s.send(msg.encode())
        # 直接打印所得到的结果
        data = s.recv(2048).decode()
        print(data)

# 历史记录
def do_history(name):
    msg = 'H '+name
    s.send(msg.encode())#　发起请求
    data = s.recv(1024).decode() #　是否有历史记录
    if data == 'OK':
        while True:
            msg = s.recv(1024).decode()
            if msg == '##':
                break
            print(msg)
    else:
        print("没有历史记录")


#登录后的界面
def login(name):
    while True:
        print("""
                ========welcome===========
                1.查单词  2.历史记录  3.注销
                ==========================
                """)
        cmd = input("输入选项：")
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_history(name)
        elif cmd == '3':
            s.send(b'E')
            sys.exit("谢谢使用")
            return
        else:
            print("请输入正确命令")



def main():
    while True:
        print("""
        ========welcome======
        1.注册  2.登录  3.退出
        =====================
        """)
        cmd = input("输入选项：")
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            s.send(b'E')
            sys.exit("谢谢使用")
        else:
            print("请输入正确命令")



if __name__ == '__main__':
    main()