#!/usr/bin/python

import CondorTools
import TimedExec
from IDPLException import *
import getopt
import os
import sys
import signal
import socket
import time

def main() {
    srcFile = ''
    dstFile = ''

    SRC_HOST=''
    DST_HOST=''
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], '', [ 'srcfile=', 'dstfile=', 'srchost=', 'dsthost='])
    except getopt.GetoptError as err:
        print str(err) # 'Usage: --srcfile <sourcefile> --dstfile <destfile> 
        usage()        #         --srchost <sourcehost> --dsthost <desthost>'
        sys.exit(4)

    for opt, arg in options:
        if opt == '--srcfile':
            srcFile = arg
        elif opt == '--dstfile':
            dstFile = arg
        elif opt == '--srchost':
            SRC_HOST = arg
        elif opt == '--dsthost':
            DST_HOST = arg
        
    ifile = open(srcFile)
    catfile = ifile.read()
    ofile = open(dstFile, "w+")
    
    output = srcFile + ".out"
    error  = srcFile + ".err"
    log    = srcFile + ".log"
    
    SRC_HOST=komatsu.chtc.wisc.edu
    SRC_PATH=/home/idpl/100M
    DST_HOST=murpa.rocksclusters.org
    DST_PATH=100M
}

#def sourceFile(fname) {
#    file = open(fname)
#    destFile(file)
    #TODO
#}

#def destFile(fname) {
#    fileName = fname + "-submit"
#    file = open(fileName, 'w+')
    #TODO
#}

#def srcHost(fname) {
#    fileName = fname + ".log"
#    file = open(fileName, 'w+')
    #TODO
#}

#def dstHost(fname) {

    #TODO
#}
# vim: ts=4:sw=4:tw=78
