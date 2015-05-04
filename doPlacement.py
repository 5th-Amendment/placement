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

def main(argv) {
    srcFile = argv[1]
    ifile = open(srcFile)
    dstFile = srcFile + "-submit"
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
