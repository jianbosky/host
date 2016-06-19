#! /usr/bin/env python3.5
# -*- coding:utf-8 -*-
import os,sys,logging,pickle,paramiko
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from multiprocessing import Pool
from core import file_handler
from conf import setting
# 初始化日志格式及对象
logging.basicConfig(level=logging.INFO, filename=os.path.join(BASEDIR,'log/ssh.log'), filemode='a',
                    format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
log = logging.getLogger(__name__)
def file(i,path_x,path_y,obj):
    ip_info = file_handler.ip_user(i)
    if len(ip_info) != 0:
        ip = ip_info[0]
        port = int(ip_info[1])
        username = ip_info[2]
        passowrd = ip_info[3]
        try:
            transport = paramiko.Transport((ip, port))
            transport.connect(username=username, password=passowrd)
        except paramiko.ssh_exception.AuthenticationException as e:
            # 接收认证错误并返回给结果
            log.error("主机:%s,用户名或密码错误,%s"%(ip,e))
            print("主机:%s,用户名或密码错误"%ip)
        except paramiko.ssh_exception.SSHException as e:
            # 接收连接错误并返回给结果
            log.error("主机:%s,连接失败:%s"%(ip,e))
            print("主机:%s,连接失败"%ip)
        else:
            sftp = paramiko.SFTPClient.from_transport(transport)
            try:
                if obj == "get":
                    if os.path.isdir(os.path.dirname(path_y)):
                        sftp.get(path_x,path_y)
                    else:
                        os.makedirs(os.path.dirname(path_y))
                        sftp.get(path_x,path_y)
                elif obj == "put":
                    sftp.put(path_x,path_y)
            except Exception as e:
                log.error("主机:%s,操作失败:%s"%(ip,e))
                print("主机:%s,操作失败"%ip)
            else:
                log.info("主机:%s,文件操作成功！"%ip)
                print("主机:%s,文件操作成功！"%ip)
            transport.close()
    else:
        log.error("没有可用主机可以进行连接")
def get(arg):
    "命令执行方法"
    if len(arg) != 2:  # 如果arg 没有两个参数
        log.info("参数出错，此处需要两个参数{}".format(arg))
    else:
        #  从元组里拆分出对象列表与指令列表
        obj_list ,file_name =  arg
        cmd = " ".join(file_name)
        remote_path =os.path.join(setting.FILEPATH["remote_path"],cmd) # 组合远程主机目录
        ip_list = file_handler.cmd_handle(obj_list)  # 获取所有的IP列表
        if len(ip_list) >= 1:
            pool = Pool(5)
            for i in ip_list:
                local_path =os.path.join(setting.FILEPATH["loca_path"],i) #组合以IP命令的本地目录
                local_path = os.path.join(local_path,cmd)
                pool.apply_async(file,args=(i,remote_path,local_path,"get"))
            pool.close()
            pool.join()
        else:
            log.info("IP地址为空！可能是输入的IP不合法或没有增加进去")

def put(arg):
    "命令执行方法"
    if len(arg) != 2:  # 如果arg 没有两个参数
        log.info("参数出错，此处需要两个参数{}".format(arg))
    else:
        #  从元组里拆分出对象列表与指令列表
        obj_list ,file_name =  arg
        cmd = " ".join(file_name)
        local_path =os.path.join(setting.FILEPATH["loca_path"],cmd) # 组合本地目录
        if os.path.isfile(local_path):
            remote_path =os.path.join(setting.FILEPATH["remote_path"],cmd) # 组合远程主机目录
            ip_list = file_handler.cmd_handle(obj_list)  # 获取所有的IP列表
            if len(ip_list) >= 1:
                pool = Pool(5)
                for i in ip_list:
                    pool.apply_async(file,args=(i,local_path,remote_path,"put"))
                pool.close()
                pool.join()
            else:
                log.error("IP地址为空！可能是输入的IP不合法或没有增加进去")
        else:
            log.error("文件%s不存在"%local_path)