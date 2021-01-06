#!/usr/bin/python
# Copyright 2005-2016 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

# Description: How to encode Sentinel 1 netCDF dataset into BUFR

import argparse
import logging
import os
import sys
import traceback
from dateutil.parser import parse as parse_date

import numpy as np
from netCDF4 import Dataset

import mbu.config
import eccodes as ecc

alongTrackResolution = mbu.config.ini.get('ocnVariable', 'alongTrackResolution')

unexpandedDescriptors = [1007, 2019, 1096, 25061, 5071, 5072, 5073, 5074, 5075, 5040, 8075, 301011, 301013, 301021,
                         1012, 7002, 22063, 8012, 2104, 21105, 42008, 25103, 25104, 25105, 25106, 25107, 25108, 11001,
                         11002, 42006, 21030, 201130, 202129, 22022, 202000, 201000, 2026, 2027, 3025, 3026, 40039,
                         40040, 40041, 40042, 2111, 25014, 25189, 106000, 31001, 42010, 42001, 42002, 42003, 42004,
                         42005, 113000, 31001, 5030, 201130, 6030, 201000, 201131, 21135, 201000, 21136, 201130, 22161,
                         201000, 42009, 42007]


class netcdfToBufr(object):
    def __init__(self, nc_filename='#', pathOutput='#', crc='#'):
        self.nc_filename = nc_filename

        if self.nc_filename != '#' and pathOutput != '#' and crc != '#':
            logging.info("processing %s" % self.nc_filename)
            self.output_filename = pathOutput + '/' + (
                os.path.basename(self.nc_filename).replace('.nc', '_' + crc + '.bufr')).replace('ocn', 'mbu')

        self.fileBasename = os.path.basename(nc_filename)

        # read swath from the filename
        self.swathId = int(self.fileBasename[6:7])

        # reading S-1 WV file and importing into a dict
        self.sentinel1 = Dataset(self.nc_filename, 'r')
        logging.info('read all variables in the nc file and store it in dictionary')
        self.dic_var_value = {}
        for v in self.sentinel1.variables:
            if v == 'rvlZeroDopplerTime':  # and np.ma.is_masked(self.sentinel1.variables['rvlZeroDopplerTime'][:]) :
                self.dic_var_value[v] = self.sentinel1.variables[v]
            elif v != 'oswPartitions' and np.ma.is_masked(self.sentinel1.variables[v][:]):
                self.dic_var_value[v] = self.sentinel1.variables[v][:].data
            else:
                self.dic_var_value[v] = self.sentinel1.variables[v][:]

        logging.info('read all dimensions in the nc file and store it in dictionary')
        self.dic_dim_value = {}
        for d in self.sentinel1.dimensions:
            self.dic_dim_value[d] = self.sentinel1.dimensions[d]

        logging.info('read all attributes in the nc file and store it in dictionary')
        self.dic_attr_value = {}
        for a in self.sentinel1.ncattrs():
            self.dic_attr_value[a] = self.sentinel1.getncattr(a)

        logging.info('set up missionIdentifier')
        if 'S1A' in self.dic_attr_value['missionName']:
            self.missionCode = 62
        elif 'S1B' in self.dic_attr_value['missionName']:
            self.missionCode = 63

        logging.info('set up polarization')
        if self.dic_attr_value['polarisation'] == 'HH':
            self.polarization = 0
        elif self.dic_attr_value['polarisation'] == 'VV':
            self.polarization = 1

        logging.info('set up land or water flag')
        if int(self.dic_var_value['oswLandFlag'][0][0]) == 1:
            self.landWaterFlag = 0
        elif int(self.dic_var_value['oswLandFlag'][0][0]) == 0:
            self.landWaterFlag = 1

        logging.info('Ascending/descending orbit qualifier')
        self.stateVectorVel = self.dic_attr_value['statevectorVel']
        if self.stateVectorVel[2] > 0:
            self.orbitQualifier = 0
        elif self.stateVectorVel[2] < 0:
            self.orbitQualifier = 1

        logging.info('set crossTrackResolution')
        if 'wv1' in os.path.basename(self.nc_filename):
            self.crossTrackResolution = 2.0
        elif 'wv2' in os.path.basename(self.nc_filename):
            self.crossTrackResolution = 3.1

        # alongTrackResolution : set it to 4.8m instead of 5m
        logging.info('set alongTrackResolution')
        self.alongTrackResolution = alongTrackResolution

        # TODO: define an env variable to be the seed file . E.g. S1_OCN2BUFR_SEED and read the env variable
        prjFolder = os.path.dirname(os.path.abspath(__file__))
        seed_filename = os.path.join(prjFolder, 'conf', 'seed.bufr')

        self.fbufrin = open(seed_filename, 'rb')
        self.fbufrout = open(self.output_filename, 'wb')

        self.bufr = ecc.codes_bufr_new_from_file(self.fbufrin)
        if self.bufr is None:
            logging.error('Not able to codes_bufr_new_from_file')
            sys.exit()

    def oswNetcdf2bufr(self):
        self.delayedDescriptorReplication = [len(self.dic_dim_value['oswPartitions']),
                                             len(self.dic_dim_value['oswAngularBinSize'])]
        ecc.codes_set_array(self.bufr, 'inputDelayedDescriptorReplicationFactor', self.delayedDescriptorReplication)
        ecc.codes_set(self.bufr, 'compressedData', 1)
        ecc.codes_set(self.bufr, 'numberOfSubsets', len(self.dic_dim_value['oswWavenumberBinSize']))
        firstMeasurementTime = parse_date(self.dic_attr_value['firstMeasurementTime'], ignoretz=True)
        ecc.codes_set(self.bufr, 'typicalYear', firstMeasurementTime.year)
        ecc.codes_set(self.bufr, 'typicalMonth', firstMeasurementTime.month)
        ecc.codes_set(self.bufr, 'typicalDay', firstMeasurementTime.day)
        ecc.codes_set(self.bufr, 'typicalHour', firstMeasurementTime.hour)
        ecc.codes_set(self.bufr, 'typicalMinute', firstMeasurementTime.minute)
        ecc.codes_set(self.bufr, 'typicalSecond', firstMeasurementTime.second)

        logging.info('unexpandedDescriptors and BufrTemplate can be set alternatively')
        logging.info('to choose the template for the BUFR message')

        ecc.codes_set(self.bufr, 'masterTablesVersionNumber', 27)
        ecc.codes_set(self.bufr, 'localTablesVersionNumber', 4)
        ecc.codes_set_array(self.bufr, 'unexpandedDescriptors', unexpandedDescriptors)
        ecc.codes_set(self.bufr, 'satelliteIdentifier', self.missionCode)
        ecc.codes_set(self.bufr, 'satelliteInstruments', 151)
        ecc.codes_set(self.bufr, 'stationAcquisition', self.dic_attr_value['processingCenter'][:3])
        ecc.codes_set(self.bufr, 'softwareVersionNumber', self.dic_attr_value['oswAlgorithmVersion'])
        ecc.codes_set_long(self.bufr, 'stripmapIdentifier', self.swathId)  # ecc.CODES_MISSING_LONG)
        ecc.codes_set_long(self.bufr, 'numberOfSpectraInRangeDirection', 1)
        ecc.codes_set_long(self.bufr, 'numberOfSpectraInAzimuthalDirection', 1)
        ecc.codes_set_long(self.bufr, 'indexInRangeDirection', 1)
        ecc.codes_set_long(self.bufr, 'indexInAzimuthalDirection', 1)
        ecc.codes_set(self.bufr, 'orbitNumber', int(self.dic_attr_value['sourceProduct'].split('_')[8]))
        ecc.codes_set(self.bufr, 'orbitQualifier', self.orbitQualifier)
        ecc.codes_set(self.bufr, 'year', firstMeasurementTime.year)
        ecc.codes_set(self.bufr, 'month', firstMeasurementTime.month)
        ecc.codes_set(self.bufr, 'day', firstMeasurementTime.day)
        ecc.codes_set(self.bufr, 'hour', firstMeasurementTime.hour)
        ecc.codes_set(self.bufr, 'minute', firstMeasurementTime.minute)
        ecc.codes_set(self.bufr, 'second', firstMeasurementTime.second)
        ecc.codes_set_double_array(self.bufr, 'latitude', self.dic_var_value['oswLat'][0])
        ecc.codes_set_double_array(self.bufr, 'longitude', self.dic_var_value['oswLon'][0])
        ecc.codes_set_double_array(self.bufr, 'directionOfMotionOfMovingObservingPlatform',
                                   self.dic_var_value['oswHeading'][0])
        ecc.codes_set(self.bufr, 'height', 0)
        ecc.codes_set_double_array(self.bufr, 'totalWaterDepth', self.dic_var_value['oswDepth'][0])
        ecc.codes_set(self.bufr, 'landOrSeaQualifier', self.landWaterFlag)
        ecc.codes_set(self.bufr, 'antennaPolarization', self.polarization)
        ecc.codes_set_double_array(self.bufr, 'normalizedRadarCrossSection', self.dic_var_value['oswNrcs'][0])
        ecc.codes_set_double_array(self.bufr, 'nonlinearInverseSpectralWidth', self.dic_var_value['oswNlWidth'][0])

        ecc.codes_set(self.bufr, 'numberOfDirectionalBins', len(self.dic_dim_value['oswAngularBinSize']))
        ecc.codes_set(self.bufr, 'numberOfWavelengthBins', len(self.dic_dim_value['oswWavenumberBinSize']))
        ecc.codes_set(self.bufr, 'firstDirectionalBin', 0)
        ecc.codes_set(self.bufr, 'directionalBinStep', 5)
        ecc.codes_set(self.bufr, 'firstWavelengthBin', 1000)
        ecc.codes_set(self.bufr, 'lastWavelengthBin', 30)
        ecc.codes_set_double_array(self.bufr, 'windDirection', self.dic_var_value['oswWindDirection'][0])
        ecc.codes_set_double_array(self.bufr, 'windSpeed', self.dic_var_value['oswWindSpeed'][0])
        ecc.codes_set_double_array(self.bufr, 'waveAge', self.dic_var_value['oswWaveAge'][0])
        ecc.codes_set_double_array(self.bufr, 'signalToNoiseRatio', self.dic_var_value['oswSnr'][0])
        ecc.codes_set_double_array(self.bufr, 'heightOfWindWaves', self.dic_var_value['oswWindSeaHs'][0])

        ecc.codes_set(self.bufr, 'crossTrackResolution', self.crossTrackResolution)
        ecc.codes_set(self.bufr, 'alongTrackResolution', float(self.alongTrackResolution))

        ecc.codes_set_double_array(self.bufr, 'crossTrackEstimationAreaSize', self.dic_var_value['oswGroundRngSize'][0])
        ecc.codes_set_double_array(self.bufr, 'alongTrackEstimationAreaSize', self.dic_var_value['oswAziSize'][0])
        ecc.codes_set_double_array(self.bufr, 'singleLookComplexImageIntensity', self.dic_var_value['oswInten'][0])
        ecc.codes_set_double_array(self.bufr, 'singleLookComplexImageSkewness', self.dic_var_value['oswSkew'][0])
        ecc.codes_set_double_array(self.bufr, 'singleLookComplexImageKurtosis', self.dic_var_value['oswKurt'][0])
        ecc.codes_set_double_array(self.bufr, 'singleLookComplexImageVariance', self.dic_var_value['oswNv'][0])
        ecc.codes_set_double_array(self.bufr, 'radarIncidenceAngle', self.dic_var_value['oswIncidenceAngle'][0])
        ecc.codes_set_double_array(self.bufr, 'azimuthClutterCutOff', self.dic_var_value['oswAzCutoff'][0])
        ecc.codes_set_double_array(self.bufr, 'rangeCutOffWavelength', self.dic_var_value['oswRaCutoff'][0])

        for p in range(len(self.dic_dim_value['oswPartitions'])):
            ecc.codes_set(self.bufr, "#%d#partitionNumber" % (p + 1), int(p + 1))

            value = float(self.dic_var_value['oswDirmet'][0][0][p])
            if value == -999: value = 511
            ecc.codes_set(self.bufr, '#%d#dominantSwellWaveDirectionOfSpectralPartition' % (p + 1),  value)

            value = float(self.dic_var_value['oswHs'][0][0][p])
            if value == -999: value = 51.1
            ecc.codes_set(self.bufr, '#%d#significantSwellWaveHeightOfSpectralPartition' % (p + 1), value)

            value = float(self.dic_var_value['oswWl'][0][0][p])
            if value == -999: value = 1311.71
            ecc.codes_set(self.bufr, '#%d#dominantSwellWavelengthOfSpectralPartition' % (p + 1), value)

            value = float(self.dic_var_value['oswIconf'][0][0][p])
            if value == -999: value = 15
            ecc.codes_set(self.bufr, '#%d#confidenceOfInversionForEachPartitionOfSwellWaveSpectra' % (p + 1), value)

            value = float(self.dic_var_value['oswAmbiFac'][0][0][p])
            if value == -999: value = 1.62143
            ecc.codes_set(self.bufr, '#%d#ambiguityRemovalFactorForSwellWavePartition' % (p + 1), value)

        if np.ma.is_masked(self.dic_var_value['oswPartitions']):
            dum = self.dic_var_value['oswPartitions'].astype(np.float32)
            dataOswPartitions = dum.data
            dataOswPartitions[dataOswPartitions == -128] = 255
            dataOswPartitions[dataOswPartitions == -1] = 255
            self.dic_var_value['oswPartitions'] = dataOswPartitions

        for a in range(len(self.dic_dim_value['oswAngularBinSize'])):
            ecc.codes_set(self.bufr, "#%d#directionSpectral" % (a + 1), int(self.dic_var_value['oswPhi'][a]))
            ecc.codes_set_double_array(self.bufr, "#%d#waveNumberSpectral" % (a + 1), self.dic_var_value['oswK'])
            ecc.codes_set_double_array(self.bufr, "#%d#realPartOfCrossSpectraPolarGridNumberOfBins" % (a + 1),
                                       self.dic_var_value['oswQualityCrossSpectraRe'][0][0][a][:60])
            ecc.codes_set_double_array(self.bufr, "#%d#imaginaryPartOfCrossSpectraPolarGridNumberOfBins" % (a + 1),
                                       self.dic_var_value['oswQualityCrossSpectraIm'][0][0][a][:60])
            ecc.codes_set_double_array(self.bufr, "#%d#waveSpectra" % (a + 1),
                                       self.dic_var_value['oswPolSpec'][0][0][a][:60])
            ecc.codes_set_double_array(self.bufr, "#%d#binPartitionReference" % (a + 1),
                                       self.dic_var_value['oswPartitions'][0][0][a][:60])
            ecc.codes_set(self.bufr, "#%d#shortestOceanWavelengthOnSpectralResolution" % (a + 1),
                          float(self.dic_var_value['oswSpecRes'][0][0][a]))

        logging.info(self.bufr)
        ecc.codes_set(self.bufr, 'pack', 1)
        ecc.codes_write(self.bufr, self.fbufrout)
        self.fbufrout.close()
        self.fbufrin.close()
        logging.info("Created output BUFR file %s" % self.output_filename)

        return self.output_filename


def cmdline():
    parser = argparse.ArgumentParser(description="This script process convert a WV OCN .nc in bufr file.")

    parser.add_argument("--nc2bufr", dest="nc2bufr", nargs='+',
                        help="convert a WV OCN .nc in bufr file. "
                             "Please insert in input: filename_nc_input, "
                             "folder_bufr_out, crc_nc_input")
    parser.add_argument("--verbose", dest="verbose", default=False, action='store_true',
                        help="add verbosity")
    args = parser.parse_args()

    if args.nc2bufr:
        logging.info('convert nc2bufr')
        logging.info(args.nc2bufr)
        if len(args.nc2bufr) < 3:
            print('Usage: {0} nc_input  bufr_out crc'.format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)
        nc_filename = args.nc2bufr[0]
        outputDir = args.nc2bufr[1]
        crc = args.nc2bufr[2]
        try:
            obj = netcdfToBufr(nc_filename, outputDir, crc)
            output_filename = obj.oswNetcdf2bufr()

        except ecc.CodesInternalError as err:
            if args.verbose:
                traceback.print_exc(file=sys.stderr)
            else:
                print(err.msg, file=sys.stderr)
    else:
        logging.error("No valid argument found; try -h.")


if __name__ == "__main__":
    sys.exit(cmdline())
