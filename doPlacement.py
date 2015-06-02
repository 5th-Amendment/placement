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

def sf1Header(ofile, placement):
    ofile.write("############\n")
    ofile.write("#\n")
    ofile.write("# Parallel Job\n")
    ofile.write("#\n")
    ofile.write("############\n")
    ofile.write("\n")
    ofile.write("universe = parallel\n")
    ofile.write("executable = %s.py\n" % placement)
    ofile.write("\n")

def sf2Hosts(ofile, exper, srcHost, dstHost):
    ofile.write("EXPERIMENT=%s\n" % exper)
    ofile.write("SRC_HOST=%s\n" % srcHost)
    ofile.write("SRC_PATH=/home/idpl/100M\n")
    ofile.write("DST_HOST=%s\n" % dstHost)
    ofile.write("DST_PATH=100M\n")
    ofile.write("\n")

def cronOpt(ofile, cronWindow, cronHr, cronMin):
    ofile.write("### Crondor Settings\n")
    ofile.write("# A promise that jobs will not run more often than this (in seconds)\n")
    ofile.write("# Required for the the job to run multiple times successfully.\n")
    ofile.write("#LEASE=1500\n")
    ofile.write("\n")
    ofile.write("# A run is allowed to take this long (in seconds) to set up; otherwise\n")
    ofile.write("# that run is skipped\n")
    ofile.write("cron_window=%s\n" % cronWindow)
    ofile.write("\n")
    ofile.write("# Try to run jobs on this schedule\n")
    if cronHr != 0:
        ofile.write("cron_hour=%s\n" % cronHr)
    if cronMin != 0:
        ofile.write("cron_minute=%s\n" % cronMin)
    ofile.write("#\n")

def sf3Args(ofile):
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

def sf4IO(ofile, placement):
    ofile.write("input   = /dev/null\n")
    ofile.write("output = $(EXPERIMENT)/%s.out.$(Node)\n" % placement)
    ofile.write("error  = $(EXPERIMENT)/%s.err.$(Node)\n" % placement)
    ofile.write("log    = $(EXPERIMENT)/%s.log\n" % placement)
    ofile.write("getenv = true\n")
    ofile.write("\n")
    ofile.write('+SrcHost = "$(SRC_HOST)"\n')
    ofile.write('+SrcPath = "$(SRC_PATH)"\n')
    ofile.write('+DstHost = "$(DST_HOST)"\n')
    ofile.write('+DstPath = "$(DST_PATH)"\n')
    ofile.write('+ExperimentName = "$(EXPERIMENT):$(executable)"\n')
    ofile.write('+ExperimentDescription = "$(SRC_HOST) to $(DST_HOST) file $(SRC_PATH)"\n')
    ofile.write("\n")

def sf5Policy(ofile):
    ofile.write('+ParallelShutdownPolicy = "WAIT_FOR_ALL"\n')
    ofile.write("\n")
    ofile.write("transfer_input_files = DataMover.py,TimedExec.py,IDPLException.py,CondorTools.py,SCPMover.py,empty\n")
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
    ofile.close()

## *****************************
## main routine
## *****************************

def main(argv):
    srcFile = ''
    dstFile = ''
    srcHost = ''
    dstHost = ''
    moverAlg = ''
    placement = ''
    exper = ''
    cronWindow = 0
    cronHr = 0
    cronMin = 0
    try:
        opts, args = getopt.gnu_getopt(argv, 'h', [ 'srcfile=', 'dstfile=', 'srchost=', 'dsthost=', 'moveralg=', 'expr=', 'cw=', 'ch=', 'cm='])
    except getopt.GetoptError as err:
        print str(err) # 'Usage: --srcfile <sourcefile> --dstfile <destfile> 
        usage()        #         --srchost <sourcehost> --dsthost <desthost>'
        sys.exit(2)    # --moverAlg [netcat, scp] --cw <cronWindow> --ch <cronHour> --cm <cronMinute>
    #TODO: Optimize using dictionaries
    for opt, arg in opts:
        if opt == '-h':
            print 'doPlacement.py --srcfile <sourcefile> --dstfile <destfile> --srchost <sourcehost> --dsthost <desthost> --moveralg [netcat, scp] --expr <experiment> --cw <cronWindow> --ch <cronHour> --cm <cronMinute>'
            sys.exit()
        elif opt == '--srcfile':
            srcFile = arg
        elif opt == '--dstfile':
            dstFile = arg
        elif opt == '--srchost':
            srcHost = arg
        elif opt == '--dsthost':
            dstHost = arg
        elif opt == '--moveralg':
            moverAlg = arg
        elif opt == '--expr':
            exper = arg
        elif opt == '--cw':
            cronWindow = arg
        elif opt == '--ch':
            cronHr = arg
        elif opt == '--cm':
            cronMin = arg

    submit = dstFile + "-submit-" + exper

    if moverAlg == 'netcat':
        placement = 'placement2'
    elif moverAlg == 'scp':
        placement = 'placement3'
    else:
        print "Unrecognized DataMover algorithm: %s" % moverAlg
        sys.exit(1)

    try:
        ifile = open(srcFile)
        catfile = ifile.read()
        ofile = open(submit, "w+")
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)

    sf1Header(ofile, placement)
    sf2Hosts(ofile, exper, srcHost, dstHost)
    if cronWindow != 0 and (cronHr != 0 or cronMin !=0):
        cronOpt(ofile, cronWindow, cronHr, cronMin)
    sf3Args(ofile)
    sf4IO(ofile, placement)
    sf5Policy(ofile)

if __name__ == "__main__":
    main(sys.argv[1:])

# vim: ts=4:sw=4:tw=78
