1.需求分析 --> 客户端该怎么用
    服务端：处理请求，处理逻辑
    客户端：发送请求，得到结果
    
    
2.确定并发方案，确定套接字使用，确定细节
    并发方案：多进程网络并发模型
    套接字：tcp套接字
    使用数据库处理数据，注册成功进入二级界面
    历史记录只看前10条，注册信息 用户名 密码
    
    
3.技术点
    用户信息表
        user表 id，name，passwd（注册，登录）
        create table user (id int primary key auto_increment,name varchar(30) not null,passwd char(64) not null);
    字典表（查词典）
        从dict.txt文本中导入数据，创建字典表dict，id，word，mean 创建索引word     
    用户查询历史记录表（查历史记录）id,u_name，word,time  
        create table hist1(id int primary key auto_increment,
        u_name varchar(30) not null,
        wd varchar(30),
        `time` datetime default now());
    一级界面怎么到二级界面
        一级界面：登录，注册，退出   二级界面：查单词，历史记录，注销
        用户注册
            成功：1）回到一级界面继续登录 2）直接进入二级界面，调用二级界面展示函数
            失败：继续注册
        用户登录
           成功：调用二级界面展示函数
           失败：回到一级界面，继续登录
        用户注销：回到一级界面
                    
4.结构设计：使用什么封装，分成几个模块
    客户端模块  函数
    服务端逻辑  函数
    服务端数据处理 类
5.功能划分和通信协议设计
    网络通信
    注册
    登录
    查单词
    历史记录
6.具体每个功能干什么
    网络通信
    注册
        客户端：请求 R name passwd 
                等请求，展示结果
        服务端：验证能否注册
               插入数据库
    登录
    查单词
    历史记录
    
cookie:import getpass
       getpass.getpass()
       功能:同input，但是隐藏输入内容
       
       加密方法
       import hashlib
       
       # 传入一个密码返回加密后的密码
        def change_passwd(passwd):
            hash = hashlib.md5()  # md5对象
            hash.update(passwd.encode())  # 加密
            return hash.hexdigest()