import datetime
import logging
import os
import socket
import sys
import time
import traceback
import xml.etree.ElementTree

import mbu.const
import mbu.processor
import mbu

VERSION = "2.1"


def cmdline():
    hostname = socket.gethostname()
    process_name = 'BUFR_ProcMain'

    file_input = dict()
    env_var = "ECCODES_DEFINITION_PATH"
    if env_var not in os.environ:
        os.environ[env_var] = ":".join([os.path.join(mbu.__file__, "conf"),
                                        f"/usr/local/components/MBU-{VERSION}/share/eccodes/definitions"])
        #                               f"/usr/local/components/MBU-{VERSION}/share/eccodes_MBU1.2/definitions"])

    file_input['inputFilenameJO'] = sys.argv[1]
    tree_job_order = xml.etree.ElementTree.parse(file_input['inputFilenameJO'])
    path_output_jo = os.path.dirname(tree_job_order.find(".//List_of_Outputs/Output/File_Name").text)

    file_input['filenameLog'] = path_output_jo + '/' + os.path.basename(path_output_jo) + '.INTERNALLOG'
    file_input['filenameList'] = path_output_jo + '/' + os.path.basename(path_output_jo) + '.LIST'

    class LogFormatter(logging.Formatter):
        prefix = f'%(asctime)s {hostname} MBU_PROC {VERSION}-0 [%(process)010d]'
        suffix = f'({process_name}:%(processName)s) %(message)s'
        FORMATS = {
            logging.DEBUG: f'{prefix}: [D] {suffix}',
            logging.INFO: f'{prefix}: [I] {suffix}',
            logging.WARNING: f'{prefix}: [W] {suffix}',
            logging.ERROR: f'{prefix}: [E] {suffix}',
            'PROGRESS': f'{prefix}: [P] {suffix}'}

        def format(self, record):
            self._fmt = self.FORMATS.get(record.levelno, self.FORMATS['PROGRESS'])
            self.datefmt = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
            return logging.Formatter.format(self, record)

    log_handler = logging.FileHandler(file_input['filenameLog'])

    # LogHandler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(LogFormatter())
    logging.root.addHandler(log_handler)
    logging.root.setLevel(logging.INFO)

    logging.info("Processing %s" % file_input['inputFilenameJO'])
    excst = time.time()
    x = mbu.processor.Processor(file_input)
    try:
        x.parse_job_order()
        x.start_core()
        x.prepare_outputs()
        exit_code = mbu.const.EXIT_OK
        processed_product_count = len(x.output_bufr['burfProducts']) + len(x.output_bufr['skippedProducts'])
        if len(x.manifest['ntcdfFilename']) != processed_product_count:
            exit_code = mbu.const.EXIT_INCOMPLETE
        if len(x.output_bufr['burfProducts']) == 0:
            exit_code = mbu.const.EXIT_PB
    except mbu.const.BufrConversionError:
        exit_code = mbu.const.EXIT_PB
    except:
        logging.error("General exception")
        logging.error(traceback.format_exc())
        exit_code = mbu.const.EXIT_PB
    excen = time.time()
    logging.info("Run completed in %s seconds:", excen - excst)
    logging.info(mbu.const.EXIT_LOG[exit_code])
    sys.exit(exit_code)
