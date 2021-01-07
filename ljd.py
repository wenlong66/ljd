#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os, os.path
import shutil
import main
           
           
           
def luactolua(src):
    for item in os.listdir(src):
        path = os.path.join(src, item)
        if not item.startswith('.') and os.path.isfile(path):
            if item.endswith('.luac'):
                print(path)
                outpath = path.replace(luacdir,luaout)
                # main._main("%s > %s" % (path,path[:-1]))
                os.system("python3 main.py %s > %s" % (path,path[:-1])) 
        if os.path.isdir(path):
            luactolua(path)        
           
           
def build():

    luactolua(luacdir)        
            
            
# -------------- main --------------
if __name__ == '__main__':

    current_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_dir)

    # s = u"输入32 64,默认64\n"
    # bitnum = raw_input(s.encode('gbk')) #raw_input 只支持GBK
    bitnum = "32"
    if bitnum == "32":
        luacdir = os.path.join(current_dir,"script32")
        luaout = os.path.join(current_dir,"lua32")
    else:
        luacdir = os.path.join(current_dir,"luac64")
        luaout = os.path.join(current_dir,"lua64")
    try:
        build()
        # raw_input("success")
    except Exception as e:
        print (e)
        sys.exit(1)
