#! /usr/bin/env python3.5
# -*- coding:utf-8 -*-
import os,sys,logging,pickle,paramiko
from multiprocessing import Pool
from core import file_handler
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
# 初始化日志格式及对象
logging.basicConfig(level=logging.INFO, filename=os.path.join(BASEDIR,'log/ssh.log'), filemode='a',
                    format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
log = logging.getLogger(__name__)
def cmd_func(i,cmd):
    ip_info = file_handler.ip_user(i)
    if len(ip_info) != 0:
        ip = ip_info[0]
        port = int(ip_info[1])
        username = ip_info[2]
        passowrd = ip_info[3]
        try:
            # 创建SSH对象
            ssh = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机进行连接
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            ssh.connect(hostname=ip,port=port,username=username,password=passowrd)
            # 执行命令
            resu = []
            for excute_cmd in cmd:
                stdin, stdout, stderr = ssh.exec_command(excute_cmd)
                # 获取结果
                result= list(filter(lambda x:x is not None,[stdout.read(),stderr.read()]))[0]
                resu.append(result)
            # 关闭连接
            ssh.close()
            log.info("主机：{}，执行命令{}成功！".format(ip,cmd))
            for x,result in enumerate(resu):                print("主机：{},执行命令：{}，结果如下：\n\n{}".format(ip,cmd[x],result.decode()))
        except Exception as e:
            print("连接主机{}出错".format(ip))
            log.error("连接主机{}出错：{}".format(ip,e))
    else:
        log.error("没有可用主机可以进行连接")
        print("没有可用主机可以进行连接")
def run(arg):
    "命令执行方法"
    if len(arg) != 2:  # 如果arg 没有两个参数
        log.info("参数出错，此处需要两个参数{}".format(arg))
        print("参数出错，此处需要两个参数{}".format(arg))
    else:
        #  从元组里拆分出对象列表与指令列表
        obj_list ,cmd_list =  arg
        cmd = " ".join(cmd_list)  # 组合命令
        cmd = cmd.split(",") # 以逗号分割重组命令
        ip_list = file_handler.cmd_handle(obj_list)  # 获取所有的IP列表
        if len(ip_list) >= 1:
            pool = Pool(5)
            for i in ip_list:
                # cmd_func(i,cmd)
                pool.apply_async(cmd_func,args=(i,cmd))
            pool.close()
            pool.join()
        else:
            log.info("你当前输入的IP地址不存在，请先增加！")
            print("你当前输入的IP地址不存在，请先增加！")
            file_handler.add_host()
