#!/usr/bin/python
########################################################################
# Copyright (C) 2016 SERCO SpA                                         #
# Gianluca Sabella gianluca.sabella@gmail.com                          #
# Giovanna Palumbo giovanna.palumbo@serco.com                          #
#                                                                      #
# This file is part of OCN to BURF Processor Project                   #
#                                                                      #
# OCN to BURF Processor project can not be copied and/or distributed   #
# without the express permission of the authors.                       #
########################################################################

import datetime
import logging
import os
import socket
import sys
import time
import traceback
import xml.etree.ElementTree

import mbu.processor


def cmdline():
    hostname = socket.gethostname()
    processName = 'BUFR_ProcMain'

    fileInput = dict()

    fileInput['inputFilenameJO'] = sys.argv[1]
    treeJobOrder = xml.etree.ElementTree.parse(fileInput['inputFilenameJO'])
    pathOutputJO = os.path.dirname(treeJobOrder.find(".//List_of_Outputs/Output/File_Name").text)

    fileInput['filenameLog'] = pathOutputJO + '/' + os.path.basename(pathOutputJO) + '.INTERNALLOG'
    fileInput['filenameList'] = pathOutputJO + '/' + os.path.basename(pathOutputJO) + '.LIST'

    class LogFormatter(logging.Formatter):
        FORMATS = {
            logging.DEBUG: '%(asctime)s ' + hostname + ' MBU_PROC 0.1-0 [%(process)010d]: [D] (' + processName + ':%(processName)s) %(message)s',
            logging.INFO: '%(asctime)s ' + hostname + ' MBU_PROC 0.1-0 [%(process)010d]: [I] (' + processName + ':%(processName)s) %(message)s',
            logging.WARNING: '%(asctime)s ' + hostname + ' MBU_PROC 0.1-0 [%(process)010d]: [W] (' + processName + ':%(processName)s) %(message)s',
            logging.ERROR: '%(asctime)s ' + hostname + ' MBU_PROC 0.1-0 [%(process)010d]: [E] (' + processName + ':%(processName)s) %(message)s',
            'PROGRESS': '%(asctime)s ' + hostname + ' MBU_PROC 0.1-0 [%(process)010d]: [P] (' + processName + ':%(processName)s) %(message)s'}

        def format(self, record):
            self._fmt = self.FORMATS.get(record.levelno, self.FORMATS['PROGRESS'])
            self.datefmt = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
            return logging.Formatter.format(self, record)

    LogHandler = logging.FileHandler(fileInput['filenameLog'])

    # LogHandler = logging.StreamHandler(sys.stdout)
    LogHandler.setFormatter(LogFormatter())
    logging.root.addHandler(LogHandler)
    logging.root.setLevel(logging.INFO)

    logging.info("Processing %s" % fileInput['inputFilenameJO'])
    excst = time.time()
    x = mbu.processor.Processor(fileInput)
    try:
        x.parseJO()
        x.startCore()
        x.prepareOutputs()
        exitCode = 0
    except:
        logging.error("General exception")
        logging.error(traceback.format_exc())
        exitCode = 1
    excen = time.time()
    logging.info("Run completed in %s seconds:", excen - excst)
    sys.exit(exitCode)
