import logging
import os
import pprint
import xml.etree.ElementTree

import mbu.bufr_encode_sentinel1


class JobOrder(object):
    def __init__(self, filename_jo='#'):
        self.filenameJO = filename_jo
        self.treeJobOrder = xml.etree.ElementTree.parse(self.filenameJO)
        self.Inputs = dict()
        self.Outputs = dict()
        self.LogLevel = dict()
        self.timeSensing = dict()
        pass

    def read_inputs(self):
        self.Inputs['count_ListOfInputs'] = str(
            self.treeJobOrder.find(".//List_of_Inputs/Input/List_of_File_Names").get('count'))
        # if the input OCN is one
        self.Inputs['fileType'] = self.treeJobOrder.find(".//List_of_Inputs/Input/File_Type").text
        self.Inputs['filename'] = self.treeJobOrder.find(".//List_of_Inputs/Input/List_of_File_Names/File_Name").text
        return self.Inputs

    def read_output(self):
        self.Outputs['count_ListOfOutputs'] = str(self.treeJobOrder.find(".//List_of_Outputs").get('count'))
        self.Outputs['fileType'] = self.treeJobOrder.find(".//List_of_Outputs/Output/File_Type").text
        self.Outputs['filename'] = os.path.dirname(self.treeJobOrder.find(".//List_of_Outputs/Output/File_Name").text)
        return self.Outputs

    def read_log_level(self):
        self.LogLevel['Stdout_Log_Level'] = self.treeJobOrder.find(".//Stdout_Log_Level").text
        self.LogLevel['Stderr_Log_Level'] = self.treeJobOrder.find(".//Stderr_Log_Level").text
        return self.LogLevel

    def read_time_sensing(self):
        self.timeSensing['Start'] = self.treeJobOrder.find(".//Sensing_Time/Start").text
        self.timeSensing['Stop'] = self.treeJobOrder.find(".//Sensing_Time/Stop").text
        return self.timeSensing


class OCNProduct(object):
    def __init__(self, filename='#'):
        self.ocn_product = filename
        self.manifest_tree = xml.etree.ElementTree.parse(self.ocn_product + '/manifest.safe')

        self.list_manifest = dict()
        self.namespace = {'s1sarl2': "http://www.esa.int/safe/sentinel-1.0/sentinel-1/sar/level-2",
                          'safe': "http://www.esa.int/safe/sentinel-1.0",
                          's1': "http://www.esa.int/safe/sentinel-1.0/sentinel-1",
                          's1sar': "http://www.esa.int/safe/sentinel-1.0/sentinel-1/sar",
                          's1sarl1': "http://www.esa.int/safe/sentinel-1.0/sentinel-1/sar/level-1"
                          }

    def parse_manifest(self):
        # filename netcdf
        self.list_manifest['ntcdfFilename'] = list()

        file_location = self.manifest_tree.findall('.//dataObjectSection/dataObject/byteStream/fileLocation')
        for i_nc in file_location:
            if os.path.splitext(i_nc.get('href'))[1] == '.nc':
                self.list_manifest['ntcdfFilename'].append(self.ocn_product + i_nc.get('href')[1:])

        logging.info('listManifest: ')
        logging.info(pprint.pformat(self.list_manifest))
        return self.list_manifest


class Processor(object):
    def __init__(self, file_input):
        logging.info("Processor ")
        self.jo = JobOrder(file_input['inputFilenameJO'])
        self.job_order = dict()
        self.output_bufr = dict()
        self.manifest = dict()
        self.error_product_convert = list()
        # get .LIST in the working dir
        self.listfile = open(file_input['filenameList'], "a")
        self.path_output_from_job_order = None
        self.ocn_product = None

    def parse_job_order(self):
        logging.info("parseJO ")
        self.job_order['input'] = self.jo.read_inputs()
        self.job_order['output'] = self.jo.read_output()
        # logger
        logging.info('listJobOrder: ')
        logging.info(pprint.pformat(self.job_order))

    def start_core(self):
        logging.info("startCore ")
        # extract the path Output from JobOrder
        self.path_output_from_job_order = self.job_order['output']['filename']

        ocn_saf_eproduct = self.job_order['input']['filename']

        self.output_bufr['burfProducts'] = list()
        self.ocn_product = OCNProduct(ocn_saf_eproduct)
        self.manifest = self.ocn_product.parse_manifest()
        crc_oc_nproduct = os.path.basename(ocn_saf_eproduct)[63:67]
        # for each nc input   save the bufr in self.listOutputBUFR
        for filename in self.manifest['ntcdfFilename']:
            logging.info(filename)
            try:
                path_output = self.path_output_from_job_order
                crc = crc_oc_nproduct
                obj_nc2bufr = mbu.bufr_encode_sentinel1.NetcdfToBufr(filename, path_output, crc)
                encode_ocn_to_bufr = obj_nc2bufr.osw_netcdf2bufr()
                # print encodeOCNtoBUFR
                self.output_bufr['burfProducts'].append(encode_ocn_to_bufr)
            except Exception:
                logging.error('error with product= ' + filename)
                logging.error('exception', exc_info=True)
                self.error_product_convert.append(filename)

    def prepare_outputs(self):
        logging.info("prepareOutputs ")
        # create .LIST
        filename_list = os.path.join(self.path_output_from_job_order,
                                     os.path.basename(os.path.normpath(self.path_output_from_job_order)) + '.LIST')
        listfile = open(filename_list, "a")
        count = 0
        for ibufr in self.output_bufr['burfProducts']:
            listfile.write(os.path.basename(ibufr) + "\n")
            count = count + 1

        logging.info('listOutputBUFR: ')
        logging.info(pprint.pformat(self.output_bufr))


if __name__ == "__main__":
    logging.info("libProcessor library")
