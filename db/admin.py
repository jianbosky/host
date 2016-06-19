#! /usr/bin/env python3.5
# -*- coding:utf-8 -*-
import pickle
# 增加用户
testDict ={"name":"jjb","password":"123456","lock":0}
file = 'jjb' # 以用户名命名文件
fp = open(file,'wb')
pickle.dump(testDict,fp)
fp.close()