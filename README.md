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
        user表 id，name，pwd（注册，登录）
        create table user (id int primary key auto_increment,name varchar(30) not null,passwd char(64) not null);
    字典表（查词典）
        从dict.txt文本中导入数据，创建字典表dict，id，word，mean 创建索引word     
    用户查询历史记录表（查历史记录）u_id,u_name，word,time  
        create table hist1(u_id int primary key auto_increment,
        u_name varchar(30) not null,
        word varchar(30),
        `time` datetime default now());
    一级界面怎么到二级界面
        一级界面：登录，注册，退出   二级界面：查单词，历史记录，注销
        用户注册
            成功：print 1）回到一级界面继续登录 2）直接进入二级界面，调用二级界面展示函数
            失败：继续注册
        用户登录
           成功：调用二级界面展示函数
           失败：回到一级界面，继续登录
        用户注销：回到一级界面
                    
4.结构设计：使用什么封装，分成几个模块
