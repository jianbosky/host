#!/usr/bin/env python3.5
# -*- coding:utf8 -*-
import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from conf import setting
from core import file_handler
from core import db_handler
from core import host_handler

def men():
    print("欢迎进入主机宝管理系统!")
    host_men = """
                  1、显示主机与所属组
                  2、增加组
                  3、增加主机
                  4、修改主机
                  5、执行命令
                  6、退出管理系统
   """
    host_dic ={
        "1":{"option":"显示主机与所属组","action":file_handler.show},
        "2":{"option":"增加组","action":file_handler.add_group},
        "3":{"option":"增加主机","action":file_handler.add_host},
        "4":{"option":"修改主机","action":file_handler.mod_host},
        "5":{"option":"执行命令","action":host_handler.exciton},
        "6":{"option":"退出管理系统","action":exit}
    }
    exit_flag =False
    while not exit_flag:
        print(host_men)
        option = input("请按键选择：").strip()
        if option in host_dic:
            func = host_dic[option].get("action")
            func()
def run():
    men()