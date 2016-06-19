#!/usr/bin/env python3.5
# -*- coding:utf8 -*-
import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from core import main

"""
******************************************
此为启动程序
******************************************
主机宝登陆用户名 jjb   密码 123456
主机宝登陆用户名 alex  密码 123456
******************************************
"""
if __name__ == "__main__":
    main.run()
