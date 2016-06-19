#!/usr/bin/env python3.5
# -*- coding:utf8 -*-
import os,sys,pickle,re,logging
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
# 初始化日志格式及对象
logging.basicConfig(level=logging.INFO, filename=os.path.join(BASEDIR,'log/ssh.log'), filemode='a',
                    format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
log = logging.getLogger(__name__)
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
            log.info("增加组%s成功！"%add_input)
            print("增加组%s成功！"%add_input)
    else:
        log.error("增加组%s失败！已存在该组!"%add_input)
        print("增加组%s失败！已存在该组!"%add_input)
def show():
    for y_data in data:
        for k in y_data:
            for i in y_data[k]:
                print("主机IP：[%s],所属组为：[%s]"%(i["ip"],k))
def add_host():
    """
    增加主机
    :return:
    """
    try:
        host_add = input("请输入主机IP：").strip()
        host_port = int(input("请输入端口号："))
        host_user = input("请输入登陆主机用户名：").strip()
        host_pwd = input("请输入登陆主机密码：").strip()
        #  判断是否为IP
        if re.match(r"((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$",host_add):
            if  host_port != "" and len(host_user) != 0 and len(host_pwd)!= 0:
                host_group = input("请输入主机所属组:").strip()
                for g in data:
                    if host_group  in g.keys():
                        for g_data in data:
                            if host_group in g_data.keys():
                                g_data[host_group].append({"ip":"%s"%host_add,"port":"%s"%host_port,"username":"%s"%host_user,"password":"%s"%host_pwd})
                        with open(db_path,"wb") as fw:
                            pickle.dump(data,fw)
                            log.info("增加主机[%s]成功！"%host_add)
                            print("增加主机[%s]成功！"%host_add)
                            break
                else:
                    log.error("增加主机[%s]失败,组[%]不存在！"%(host_add,host_group))
                    print("增加主机[%s]失败，组[%]不存在！！"%(host_add,host_group))
                    return add_host()
            else:
                return add_host()
        else:
            log.error("你输入的不是IP地址：%s" %host_add)
            print("你输入的不是IP地址：%s" %host_add)
    except Exception as ex:
        log.error("增加主机异常%s"%ex)
        print("增加主机异常")
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
                log.info("该IP主机：{}，原已属于该组：{}".format(IP_modi,gg))
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
                    log.info("修改主机[%s]成功,新组名称为%s！"%(IP_modi,gg))
                    print("修改主机[%s]成功,新组名称为%s！"%(IP_modi,gg))
    else:
        log.error("不存在此IP主机{}".format(IP_modi))
        print("不存在此IP主机{}".format(IP_modi))
def cmd_handle(arg):
    """
    解析命令，并返回主机IP列表
    :param arg:
    :return:
    """
    if arg[0] == "*":
        ip_list = []
        for g in data:
            for gg in g:
                for ip in g[gg]:
                    ip_list.append(ip["ip"])
        ip_list = list(set(ip_list)) # 去除重复IP
        return ip_list
    elif arg[0] == "-h":
        ip_list=[]
        ip_group = arg[1:]
        for data_ip in data:
            for ip in ip_group:
                for ip_data in data_ip:
                    for iptest in data_ip[ip_data]:
                        if ip in iptest["ip"]:
                            ip_list.append(ip)
        ip_list =list(set(ip_list))
        return ip_list
    elif arg[0] == "-g":
        ip_list = []
        group_list =arg[1:]
        for group in group_list:
            for g in data:
                if group in g.keys():
                    for ip in g[group]:
                        ip_list.append(ip["ip"])
        ip_list = list(set(ip_list)) # 去除重复的IP
        return ip_list

    else:
        ip_list =[]
        return ""
def ip_user(ip):
    """
    获取主机连接账号信息
    :param ip:
    :return:
    """
    ip_info = []
    for data_ip in data:
        for ip_data in data_ip:
            for iptest in data_ip[ip_data]:
                if ip in iptest["ip"]:
                    ip_info = [iptest["ip"],iptest["port"],iptest["username"],iptest["password"]]
    return ip_info
def host_delete():
    try:
        host_add = input("请要删除主机IP：").strip()
        #  判断是否为IP
        if re.match(r"((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$",host_add):
            flag = check_ip(host_add)
            if flag:
                for g in data:
                    for g_data in g:
                        for index,host in enumerate(g[g_data]):
                            if host_add in host["ip"]:
                                print(g[g_data][index])
                                del g[g_data][index]
                with open(db_path,"wb") as fw:
                    pickle.dump(data,fw)
                    log.info("删除主机[%s]成功！"%host_add)
                    print("删除主机[%s]成功！"%host_add)

            else:
                log.error("删除主机[%s]失败！"%host_add)
                print("删除主机[%s]失败！"%host_add)
                return add_host()
        else:
            log.error("你输入的不是IP地址：%s" %host_add)
            print("你输入的不是IP地址：%s" %host_add)
    except Exception as ex:
        log.error("删除主机异常%s"%ex)
        print("删除主机异常")