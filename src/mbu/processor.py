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
import logging
import os
import pprint
import xml.etree.ElementTree

import mbu.bufr_encode_sentinel1


class JobOrder(object):
    def __init__(self, filenameJO='#'):
        self.filenameJO = filenameJO
        self.treeJobOrder = xml.etree.ElementTree.parse(self.filenameJO)
        self.Inputs = dict()
        self.Outputs = dict()
        self.LogLevel = dict()
        self.timeSensing = dict()
        pass

    def readInputs(self):
        self.Inputs['count_ListOfInputs'] = str(
            self.treeJobOrder.find(".//List_of_Inputs/Input/List_of_File_Names").get('count'))
        # if the input OCN is one
        self.Inputs['fileType'] = self.treeJobOrder.find(".//List_of_Inputs/Input/File_Type").text
        self.Inputs['filename'] = self.treeJobOrder.find(".//List_of_Inputs/Input/List_of_File_Names/File_Name").text
        return self.Inputs

    def readOutput(self):
        self.Outputs['count_ListOfOutputs'] = str(self.treeJobOrder.find(".//List_of_Outputs").get('count'))
        self.Outputs['fileType'] = self.treeJobOrder.find(".//List_of_Outputs/Output/File_Type").text
        self.Outputs['filename'] = os.path.dirname(self.treeJobOrder.find(".//List_of_Outputs/Output/File_Name").text)
        return self.Outputs

    def readLogLevel(self):
        self.LogLevel['Stdout_Log_Level'] = self.treeJobOrder.find(".//Stdout_Log_Level").text
        self.LogLevel['Stderr_Log_Level'] = self.treeJobOrder.find(".//Stderr_Log_Level").text
        return self.LogLevel

    def readTimeSensing(self):
        self.timeSensing['Start'] = self.treeJobOrder.find(".//Sensing_Time/Start").text
        self.timeSensing['Stop'] = self.treeJobOrder.find(".//Sensing_Time/Stop").text
        return self.timeSensing


class OCNProduct(object):
    def __init__(self, filename='#'):
        self.ocnProduct = filename
        self.treeManifestOcnProduct = xml.etree.ElementTree.parse(self.ocnProduct + '/manifest.safe')

        self.listManifest = dict()
        self.namespace = {'s1sarl2': "http://www.esa.int/safe/sentinel-1.0/sentinel-1/sar/level-2",
                          'safe': "http://www.esa.int/safe/sentinel-1.0",
                          's1': "http://www.esa.int/safe/sentinel-1.0/sentinel-1",
                          's1sar': "http://www.esa.int/safe/sentinel-1.0/sentinel-1/sar",
                          's1sarl1': "http://www.esa.int/safe/sentinel-1.0/sentinel-1/sar/level-1"
                          }

    def parseManifest(self):
        # filename netcdf
        self.listManifest['ntcdfFilename'] = list()

        fileLocation = self.treeManifestOcnProduct.findall('.//dataObjectSection/dataObject/byteStream/fileLocation')
        root = self.treeManifestOcnProduct.getroot()
        for iNC in fileLocation:
            if os.path.splitext(iNC.get('href'))[1] == '.nc':
                self.listManifest['ntcdfFilename'].append(self.ocnProduct + iNC.get('href')[1:])

        logging.info('listManifest: ')
        logging.info(pprint.pformat(self.listManifest))
        return self.listManifest


class Processor(object):
    def __init__(self, fileInput='#'):
        logging.info("libProcessor ")
        self.jo = JobOrder(fileInput['inputFilenameJO'])
        self.listJobOrder = dict()
        self.listOutputBUFR = dict()
        self.listManifest = dict()
        self.errorProductConvert = list()
        # get .LIST in the working dir
        self.listfile = open(fileInput['filenameList'], "a")

    def parseJO(self):
        logging.info("parseJO ")
        self.listJobOrder['input'] = self.jo.readInputs()
        self.listJobOrder['output'] = self.jo.readOutput()
        # logger
        logging.info('listJobOrder: ')
        logging.info(pprint.pformat(self.listJobOrder))

    def startCore(self):
        logging.info("startCore ")
        # extract the path Output from JobOrder
        self.pathOutputJO = self.listJobOrder['output']['filename']

        ocnSAFEproduct = self.listJobOrder['input']['filename']

        self.listOutputBUFR['burfProducts'] = list()
        self.ocnProduct = OCNProduct(ocnSAFEproduct)
        self.listManifest = self.ocnProduct.parseManifest()
        crcOCNproduct = os.path.basename(ocnSAFEproduct)[63:67]
        # for each nc input   save the bufr in self.listOutputBUFR
        for iinputNETCDF in self.listManifest['ntcdfFilename']:

            # print iinputNETCDF
            logging.info(iinputNETCDF)
            try:

                nc_filename = iinputNETCDF

                pathOutput = self.pathOutputJO
                crc = crcOCNproduct
                obj_nc2bufr = mbu.bufr_encode_sentinel1.netcdfToBufr(iinputNETCDF, pathOutput, crc)
                encodeOCNtoBUFR = obj_nc2bufr.oswNetcdf2bufr()
                # print encodeOCNtoBUFR
                self.listOutputBUFR['burfProducts'].append(encodeOCNtoBUFR)
            except Exception:

                logging.error('error with product= ' + iinputNETCDF)
                logging.error('exception', exc_info=True)
                self.errorProductConvert.append(iinputNETCDF)

    def prepareOutputs(self):
        logging.info("prepareOutputs ")
        # create .LIST
        filenameLIST = self.pathOutputJO + '/' + os.path.basename(os.path.normpath(self.pathOutputJO)) + '.LIST'
        listfile = open(filenameLIST, "a")
        count = 0
        for ibufr in self.listOutputBUFR['burfProducts']:
            listfile.write(os.path.basename(ibufr) + "\n")
            count = count + 1

        logging.info('listOutputBUFR: ')
        logging.info(pprint.pformat(self.listOutputBUFR))


if __name__ == "__main__":
    logging.info("libProcessor library")
