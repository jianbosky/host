#!/usr/bin/env python3.5
# -*- coding:utf8 -*-
import os,sys,pickle,logging
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from conf import setting
from core import file_handler
from core import db_handler
from core import host_handler
"""
************************************
此为主机宝主运行程序
************************************
"""
logging.basicConfig(level=logging.INFO, filename=os.path.join(BASEDIR,'log/ssh.log'), filemode='a',
                    format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
log = logging.getLogger(__name__)
def login():
    count = 0
    flage = False
    while count < 3:
        count += 1
        user_input = input("请输入用户名：").strip()
        pass_input = input("请输入密码：").strip()
        db = db_handler.handler(setting.DATABASE,user_input)
        if os.path.isfile(db):
            f = open(db,"rb")
            data = pickle.loads(f.read())
            f.close()
            if user_input == data["name"] and data["lock"] !=1:
                if pass_input == data["password"]:
                    flage = True
                    log.info("用户[%s]登陆成功！"%user_input)
                    break
                else:
                    print("用户名或密码错误！")
                    if count > 2:
                        with open(db,"wb") as f:
                            data["lock"] = 1
                            pickle.dump(data,f)
                            log.info("用户[%s]被锁定！"%user_input)
                            print("用户[%s]已被锁定！"%user_input)
            else:
                print("用户[%s]已被锁定！"%user_input)
                exit()
    if flage == True:
        print("用户[%s]登陆成功！"%user_input)
        men()
    else:
        exit()
def men():
    print("欢迎进入主机宝管理系统!")
    host_men = """
                  1、显示主机与所属组
                  2、增加组
                  3、增加主机
                  4、修改主机
                  5、删除主机
                  6、执行命令
                  7、退出管理系统
   """
    host_dic ={
        "1":{"option":"显示主机与所属组","action":file_handler.show},
        "2":{"option":"增加组","action":file_handler.add_group},
        "3":{"option":"增加主机","action":file_handler.add_host},
        "4":{"option":"修改主机","action":file_handler.mod_host},
        "5":{"option":"删除主机","action":file_handler.host_delete},
        "6":{"option":"执行命令","action":host_handler.exciton},
        "7":{"option":"退出管理系统","action":exit}
    }
    exit_flag =False
    while not exit_flag:
        print(host_men)
        option = input("请按键选择：").strip()
        if option in host_dic:
            func = host_dic[option].get("action")
            func()


def run():
    login()