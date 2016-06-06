#!/usr/bin/env python3.5
# -*- coding:utf8 -*-
import os,sys,pickle
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from conf import setting
from core import db_handler
from core import host_handler
db_path = db_handler.handler(setting.DATABASE,"host")
if os.path.exists(db_path):
    with open(db_path, "rb") as f:
        data = pickle.loads(f.read())
else:
    data =[]

def check_ip(ip):
    for data_ip in data:
        for ip_data in data_ip:
            for iptest in data_ip[ip_data]:
                if ip in iptest["ip"]:
                    return True
    else:
        return False
def check_group(group):
    for gc in data:
        if group in gc.keys():
            return True
    else:
        return False
def add_group():
    add_input = input("请输入要增加的组：").strip()
    list_data = []
    for y_data in data:
        for k in y_data:
            list_data.append(k)
    if add_input not in list_data:
        new_group = {"%s"%add_input:[]}
        data.append(new_group)
        with open(db_path,"wb") as fw:
            pickle.dump(data,fw)
            print("增加组%s成功！"%add_input)
    else:
        print("增加组%s失败！已存在该组!"%add_input)
def show():
    for y_data in data:
        for k in y_data:
            for i in y_data[k]:
                print("主机IP：[%s],所属组为：[%s]"%(i["ip"],k))
def add_host():
    try:
        host_add = input("请输入主机IP：").strip()
        host_port = int(input("请输入端口号："))
        host_user = input("请输入登陆主机用户名：").strip()
        host_pwd = input("请输入登陆主机密码：").strip()
        if len(host_add) != 0 and host_port != "" and len(host_user) != 0 and len(host_pwd)!= 0:
            host_group = input("请输入主机所属组:").strip()
            for g in data:
                if host_group  in g.keys():
                    for g_data in data:
                        if host_group in g_data.keys():
                            g_data[host_group].append({"ip":"%s"%host_add,"port":"%s"%host_port,"username":"%s"%host_user,"password":"%s"%host_pwd})
                    with open(db_path,"wb") as fw:
                        pickle.dump(data,fw)
                        print("增加主机[%s]成功！"%host_port)
                        break
            else:
                print("增加主机[%s]失败！"%host_port)
                return add_host()
        else:
            return add_host()
    except Exception as ex:
        print("增加主机异常%s"%ex)

def mod_host():
    """
    修改主机所属组
    :return:
    """
    IP_modi = input("请输入要变更的IP：").strip()
    ip_check = check_ip(IP_modi)
    if ip_check:
        gg = input("请输入转入的组名称：").strip()
        gg_check = check_group(gg)
        if gg_check:
            # 获取该IP 原所属组名称
            for data_gg in data:
                for i_gg in data_gg:
                    for i,ip_data in enumerate(data_gg[i_gg]):
                        if IP_modi == ip_data["ip"]:
                            g = i_gg
                            count = i
                            ip = ip_data
            if gg == g:
                print("该IP主机：{}，原已属于该组：{}".format(IP_modi,gg))
            else:
                for x_data in data:
                    for xi_gg in x_data:
                        # 确定转入组相符
                        if xi_gg == gg:
                            x_data[xi_gg].append(ip)
                        # 删除原来所属组IP主机
                        elif xi_gg == g:
                            x_data[xi_gg].remove(ip)
                with open(db_path,"wb") as fw:
                    pickle.dump(data,fw)
                    print("修改主机[%s]成功,新组名称为%s！"%(IP_modi,gg)
    else:
        print("不存在此IP主机{}".format(IP_modi))