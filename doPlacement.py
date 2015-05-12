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
    srcHost = ''
    dstHost = ''
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
            srcHost = arg
        elif opt == '--dsthost':
            dstHost = arg
    
    output = dstFile + ".out"
    error  = dstFile + ".err"
    log    = dstFile + ".log"
    submit = dstFile + "-submit"
    
    ifile = open(srcFile)
    catfile = ifile.read()
    ofile = open(submit, "w+")
    ofile.write("############\n")
    ofile.write("#\n")
    ofile.write("# Parallel Job\n")
    ofile.write("#\n")
    ofile.write("############\n")
    ofile.write("\n")
    ofile.write("universe = parallel\n")
    ofile.write("executable = %s.py\n" % srcFile)
    ofile.write("\n")
    
    ofile.write("SRC_HOST=%s\n" % srcHost)
    SRC_PATH=/home/idpl/100M
    ofile.write("DST_HOST=%s\n" % dstHost)
    DST_PATH=100M
    ofile.write("\n")

    ofile.write("# Keep running the job\n")
    ofile.write("on_exit_remove=false\n")
    ofile.write("\n")
    ofile.write("# Arguments are:\n")
    ofile.write("# 1. File to send (on the sending host)\n")
    ofile.write("# 2. Location to write file (on the receiving host)\n")
    ofile.write("\n")
    ofile.write("arguments = -i $(SRC_PATH) -o $(DST_PATH)\n")
    ofile.write("\n")
    ofile.write("## Enable Chirp\n")
    ofile.write("+WantIOProxy = true\n")
    ofile.write("\n")
    
    ofile.write("input   = /dev/null\n")
    ofile.write("output = %s.$(Node)\n" % out)
    ofile.write("error  = %s.$(Node)\n" % error)
    ofile.write("log    = %s\n" % log)
    ofile.write("getenv = true\n")
    ofile.write("\n")
    ofile.write('+SrcPath = "$(SRC_PATH)"\n')
    ofile.write('+DstHost = "$(DST_HOST)"\n')
    ofile.write('+DstPath = "$(DST_PATH)"\n')
    ofile.write("\n")
    
    ofile.write('+ParallelShutdownPolicy = "WAIT_FOR_ALL"\n')
    ofile.write("\n")
    ofile.write("transfer_input_files = DataMover.py,TimedExec.py,IDPLException.py,CondorTools.py,empty\n")
    ofile.write("\n")
    ofile.write("should_transfer_files = YES\n")
    ofile.write("when_to_transfer_output = ON_EXIT\n")
    ofile.write("\n")
    ofile.write("machine_count = 1\n")
    ofile.write('requirements = (Machine == "$(SRC_HOST)")\n')
    ofile.write("transfer_output_files = empty\n")
    ofile.write("queue\n")
    ofile.write("\n")
    
    ofile.write("machine_count = 1\n")
    ofile.write('requirements = (Machine == "$(DST_HOST)")\n')
    ofile.write("transfer_output_files = empty\n")
    ofile.write("queue\n")

if __name__ == "__main__":
	main(sys.argv[1:])

# vim: ts=4:sw=4:tw=78