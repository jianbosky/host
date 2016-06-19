#!/usr/bin/env python3.5
# -*- coding:utf8 -*-
import os,sys,re
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
import logging,importlib
# 初始化日志格式及对象
logging.basicConfig(level=logging.INFO, filename=os.path.join(BASEDIR,'log/ssh.log'), filemode='a',
                    format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
log = logging.getLogger(__name__)
# 调用执行模块
def module_excute(moudle_name,func_name,arg):
    try:
        # 导入要执行的模块
        module = importlib.import_module("salt.salt_{}".format(moudle_name))
        # 判断函数名是否包含在模块里
        if hasattr(module,func_name):
            func = getattr(module,func_name)
            func(arg)
            print("***" * 20)
        else:
            print("不存在")
    except Exception as e :
        log.info("input:{},error:{}".format(moudle_name,e))
def exciton():
    usage = """
    salt "*" cmd.run "excute_cmd1,excute_cmd2..."          :"所有主机执行命令"
    salt -g "group" cmd.run "excute_cmd1,excute_cmd2..."   :"指定组执行命令"
    salt -h "ip_host" cmd.run "excute_cmd1,excute_cmd2..." :"指定主机IP执行命令"
    salt "*" file.put "filename"                           :"所有主机上传文件"
    salt "*" file.get "filename"                           :"所有主机下载文件"
    exit                                                   :"退出"
     """
    print("欢迎进入主机命令执行系统!")
    user_cmd = input("请输入要执行的命令>>>:").strip()
    if user_cmd.startswith("salt"):  # 判断是否以salt开始
        user_cmd_list = user_cmd.split()  #以空格分割成列表
        # 过滤掉特殊字符
        user_arg_list = list(map(lambda x:re.sub(r'[\"\']',"",x),user_cmd_list))
        # 匹配含点的模块名字
        p = re.compile(r'[a-zA-Z_]+\.[a-zA-Z_]+')
        flag =False
        count = 0
        for i in user_arg_list:
            if p.match(i):
                flag = True
                count +=1
                moudle_func = i  # 获取模块名
                break   # 只匹配第一个含点的模块名
        # 只有命令里含*。*格式时，继续
        if flag and count == 1:
            cmd_list = user_arg_list[user_arg_list.index(moudle_func)+1:]  # 获取原列表在此命令（*.*）之后的所有命令变成命令列表
            obj_list = user_arg_list[user_arg_list.index("salt")+1:user_arg_list.index(moudle_func)]  # 获取以salt开头模块函数结尾之前的所有内空转到列表
            arg = (obj_list,cmd_list) # 将操作对象列表和指令列表放到元组中
            moudle_name = moudle_func.split(".")[0]  # 获取模块名
            func_name = moudle_func.split(".")[1]  # 获取函数名
            module_excute(moudle_name,func_name,arg)
            exciton()
        else:
            print("命令输入错误！请按以下格式输入：")
            print(usage)
            exciton()
    elif user_cmd =="exit":
        exit()
    else:
        print("命令输入错误！请按以下格式输入：")
        print(usage)
        exciton()