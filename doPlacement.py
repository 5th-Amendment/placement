#! /usr/bin/env python
import DataMover
import CondorTools
from IDPLException import *
import os
import sys
import signal
import socket
import time
import getopt
import subprocess

def main(argv):
    srcFile = ''
    dstFile = ''

    SRC_HOST=''
    DST_HOST=''
    try:
        opts, args = getopt.gnu_getopt(argv, 'h', [ 'srcfile=', 'dstfile=', 'srchost=', 'dsthost='])
    except getopt.GetoptError as err:
        print str(err) # 'Usage: --srcfile <sourcefile> --dstfile <destfile> 
        usage()        #         --srchost <sourcehost> --dsthost <desthost>'
        sys.exit(4)
    for opt, arg in options:
        if opt == '-h':
            print 'doPlacement.py -srcfile <sourcefile> --dstfile <destfile> --srchost <sourcehost> --dsthost <desthost>'
        elif opt == '--srcfile':
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

if __name__ == "__main__":
	main(sys.argv[1:])

# vim: ts=4:sw=4:tw=78
