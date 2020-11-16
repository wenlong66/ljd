#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os, os.path
import shutil
import main
           
def build():
    for item in os.listdir(luaout):
        if item.endswith('.luac'):
            path = os.path.join(luaout, item)
            # main._main("%s > %s" % (path,path[:-1]))
            os.system("python3 main.py %s > %s" % (path,path[:-1])) 

# -------------- main --------------
if __name__ == '__main__':

    current_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_dir)

    # s = u"输入32 64,默认64\n"
    # bitnum = raw_input(s.encode('gbk')) #raw_input 只支持GBK
    bitnum = "64"
    if bitnum == "32":
        luaout = os.path.join(current_dir,"luac32")
    else:
        luaout = os.path.join(current_dir,"luac64")
    try:
        build()
        # raw_input("success")
    except Exception as e:
        print (e)
        sys.exit(1)
