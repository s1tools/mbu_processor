import argparse
import logging
import os
import re
import sys
import traceback
from dateutil.parser import parse as parse_date

import numpy as np
from netCDF4 import Dataset

import mbu.config
import mbu.const
import eccodes as ecc

along_track_resolution = mbu.config.ini.get('ocnVariable', 'alongTrackResolution')

# extract:
#
# |  F  |  X  |  Y  |
# |2bits|6bits|8bits|
#
# noted as number in form FXXYYY in next list: starting 0 are not present du to python syntax
# for instance 1007 -> 001007 -> F=0 X=01 Y=007

# If F = 0, the descriptor is an element descriptor.
# The values of X and Y refer directly to a single entry in Table B, X indicating
# the class and Y the entry within that class.
#
# If F = 1, the descriptor is a replication descriptor defining the replication data description operator according to
# Regulations 94.5.4.1 and 94.5.4.2. The values of X and Y define the scope of the operator and the number of
# replications, respectively. If Y = 0, delayed replication is defined; the next element descriptor will define a
# data item giving the number of replications; this descriptor may also indicate (by its value of Y) that the following
# datum is to be replicated together with the following descriptor.
#
# If F = 2, the descriptor is an operator descriptor. The value of X indicates an operation in Table C. The meaning
# of Y depends on the operation.
#
# If F = 3, the descriptor is a sequence descriptor. The values of X and Y refer directly to a single entry in
# Table D. Each entry in Table D contains a list of element descriptors, data description operators, and/or sequence
# descriptors. A sequence descriptor is defined to be equivalent to the corresponding list of descriptors at the
# Table D entry.
# numerical model.
unexpanded_descriptors = [
    (1007, 'satelliteIdentifier'),
    (2019, 'satelliteInstruments'),
    (1096, 'stationAcquisition'),
    (25061, 'softwareVersionNumber'),
    (5071, 'stripmapIdentifier'),
    (5072, 'numberOfSpectraInRangeDirection'),
    (5073, 'numberOfSpectraInAzimuthalDirection'),
    (5074, 'indexInRangeDirection'),
    (5075, 'indexInAzimuthalDirection'),
    (5040, 'orbitNumber'),
    (8075, 'orbitQualifier'),
    (301011, 'seq: year month day'),
    (301013, 'seq: hour minute second'),
    (301021, 'seq: latitude longitude'),
    (1012, 'directionOfMotionOfMovingObservingPlatform'),
    (7002, 'height'),
    (22063, 'totalWaterDepth'),
    (8012, 'landOrSeaQualifier'),
    (2104, 'antennaPolarization'),
    (21105, 'normalizedRadarCrossSection'),
    (42008, 'nonlinearInverseSpectralWidth'),
    (25103, 'numberOfDirectionalBins'),
    (25104, 'numberOfWavelengthBins'),
    (25105, 'firstDirectionalBin'),
    (25106, 'directionalBinStep'),
    (25107, 'firstWavelengthBin'),
    (25108, 'lastWavelengthBin'),
    (11001, 'windDirection'),
    (11002, 'windSpeed'),
    (42006, 'waveAge'),
    (21030, 'signalToNoiseRatio'),
    (201130, 'add 2 bits'),
    (202129, 'add 1 to the scale'),
    (22022, 'heightOfWindWaves'),
    (202000, 'end of change the scale'),
    (201000, 'end of bit add'),
    (2026, 'crossTrackResolution'),
    (2027, 'alongTrackResolution'),
    (3025, 'crossTrackEstimationAreaSize'),
    (3026, 'alongTrackEstimationAreaSize'),
    (40039, 'singleLookComplexImageIntensity'),
    (40040, 'singleLookComplexImageSkewness'),
    (40041, 'singleLookComplexImageKurtosis'),
    (40042, 'singleLookComplexImageVariance'),
    (2111, 'radarIncidenceAngle'),
    (25014, 'azimuthClutterCutOff'),
    (25189, 'rangeCutOffWavelength'),
    (42017, 'qualityFlagOfSwellWaveSpectra'),
    (107000, 'Delayed replication of 7 descriptors'),
    (31001, 'delayedDescriptorReplicationFactor'),
    (42010, 'partitionNumber'),
    (42001, 'dominantSwellWaveDirectionOfSpectralPartition'),
    (42002, 'significantSwellWaveHeightOfSpectralPartition'),
    (42003, 'dominantSwellWavelengthOfSpectralPartition'),
    (42004, 'confidenceOfInversionForEachPartitionOfSwellWaveSpectra'),
    (42005, 'ambiguityRemovalFactorForSwellWavePartition'),
    (42018, 'qualityFlagForEachPartitionOfSwellWaveSpectra'),
    (113000, 'Delayed replication of 13 descriptors'),
    (31001, 'delayedDescriptorReplicationFactor'),
    (5030, 'directionSpectral'),
    (201130, 'add 2 bits'),
    (6030, 'waveNumberSpectral'),
    (201000, 'end of change'),
    (201131, 'add 3 bits'),
    (21135, 'realPartOfCrossSpectraPolarGridNumberOfBins'),
    (201000, 'end of change'),
    (21136, 'imaginaryPartOfCrossSpectraPolarGridNumberOfBins'),
    (201130, 'add 2 bits'),
    (22161, 'waveSpectra'),
    (201000, 'end of change'),
    (42009, 'binPartitionReference'),
    (42007, 'shortestOceanWavelengthOnSpectralResolution'),
]


class NetcdfToBufr(object):
    def __init__(self, nc_filename='#', path_output='#', crc='#'):
        self.delayed_descriptor_replication = None
        self.nc_filename = nc_filename

        if self.nc_filename != '#' and path_output != '#' and crc != '#':
            logging.info("processing %s" % self.nc_filename)
            self.output_filename = path_output + '/' + (
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
        # under progress see https://github.com/wmo-im/CCT/pull/148
        elif 'S1C' in self.dic_attr_value['missionName']:
            self.missionCode = 68
        elif 'S1D' in self.dic_attr_value['missionName']:
            self.missionCode = 69

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
        self.alongTrackResolution = along_track_resolution

        # TODO: define an env variable to be the seed file . E.g. S1_OCN2BUFR_SEED and read the env variable
        prj_folder = os.path.dirname(os.path.abspath(__file__))
        seed_filename = os.path.join(prj_folder, 'conf', 'seed.bufr')

        self.fbufrin = open(seed_filename, 'rb')
        self.fbufrout = open(self.output_filename, 'wb')

        self.bufr = ecc.codes_bufr_new_from_file(self.fbufrin)
        if self.bufr is None:
            logging.error('Not able to codes_bufr_new_from_file')
            sys.exit()

    def osw_netcdf2bufr(self):
        self.delayed_descriptor_replication = [len(self.dic_dim_value['oswPartitions']),
                                               len(self.dic_dim_value['oswAngularBinSize'])]
        ecc.codes_set_array(self.bufr, 'inputDelayedDescriptorReplicationFactor', self.delayed_descriptor_replication)
        ecc.codes_set(self.bufr, 'compressedData', 1)
        ecc.codes_set(self.bufr, 'numberOfSubsets', len(self.dic_dim_value['oswWavenumberBinSize']))
        first_measurement_time = parse_date(self.dic_attr_value['firstMeasurementTime'], ignoretz=True)
        ecc.codes_set(self.bufr, 'typicalYear', first_measurement_time.year)
        ecc.codes_set(self.bufr, 'typicalMonth', first_measurement_time.month)
        ecc.codes_set(self.bufr, 'typicalDay', first_measurement_time.day)
        ecc.codes_set(self.bufr, 'typicalHour', first_measurement_time.hour)
        ecc.codes_set(self.bufr, 'typicalMinute', first_measurement_time.minute)
        ecc.codes_set(self.bufr, 'typicalSecond', first_measurement_time.second)

        logging.info('unexpandedDescriptors and BufrTemplate can be set alternatively')
        logging.info('to choose the template for the BUFR message')

        ecc.codes_set(self.bufr, 'masterTablesVersionNumber', 27)
        ecc.codes_set(self.bufr, 'localTablesVersionNumber', 4)
        ecc.codes_set_array(self.bufr, 'unexpandedDescriptors', [e[0] for e in unexpanded_descriptors])

        ecc.codes_set(self.bufr, 'satelliteIdentifier', self.missionCode)
        ecc.codes_set(self.bufr, 'satelliteInstruments', 151)
        ecc.codes_set(self.bufr, 'stationAcquisition', self.dic_attr_value['processingCenter'][:3])
        ecc.codes_set(self.bufr, 'softwareVersionNumber', self.dic_attr_value['oswAlgorithmVersion'])
        ecc.codes_set_long(self.bufr, 'stripmapIdentifier', self.swathId)  # ecc.CODES_MISSING_LONG)
        ecc.codes_set_long(self.bufr, 'numberOfSpectraInRangeDirection', 1)
        ecc.codes_set_long(self.bufr, 'numberOfSpectraInAzimuthalDirection', 1)
        ecc.codes_set_long(self.bufr, 'indexInRangeDirection', 1)
        ecc.codes_set_long(self.bufr, 'indexInAzimuthalDirection', 1)

        info = re.match(mbu.const.SAFE_PRODOUCTS_RE, self.dic_attr_value['sourceProduct'])
        if info is None:
            logging.error("Source product do not math the SAFE name nomenclature: "
                          "{0}".format(self.dic_attr_value['sourceProduct']))
            sys.exit(mbu.const.EXIT_PB)

        ecc.codes_set(self.bufr, 'orbitNumber', int(info.groupdict()["orbit"]))
        ecc.codes_set(self.bufr, 'orbitQualifier', self.orbitQualifier)
        ecc.codes_set(self.bufr, 'year', first_measurement_time.year)
        ecc.codes_set(self.bufr, 'month', first_measurement_time.month)
        ecc.codes_set(self.bufr, 'day', first_measurement_time.day)
        ecc.codes_set(self.bufr, 'hour', first_measurement_time.hour)
        ecc.codes_set(self.bufr, 'minute', first_measurement_time.minute)
        ecc.codes_set(self.bufr, 'second', first_measurement_time.second)
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

        try:
            value = float(self.dic_var_value['oswQualityFlag'][0])
            if value < 0: value = 15
        except KeyError:
            value = 15
        ecc.codes_set_long(self.bufr, 'qualityFlagOfSwellWaveSpectra', value)

        for p in range(len(self.dic_dim_value['oswPartitions'])):
            ecc.codes_set(self.bufr, "#%d#partitionNumber" % (p + 1), int(p + 1))

            value = float(self.dic_var_value['oswDirmet'][0][0][p])
            if value < 1: value = 511
            ecc.codes_set(self.bufr, '#%d#dominantSwellWaveDirectionOfSpectralPartition' % (p + 1), value)

            value = float(self.dic_var_value['oswHs'][0][0][p])
            if value == -999: value = 51.1
            ecc.codes_set(self.bufr, '#%d#significantSwellWaveHeightOfSpectralPartition' % (p + 1), value)

            value = float(self.dic_var_value['oswWl'][0][0][p])
            if value < 1: value = 1311.71
            ecc.codes_set(self.bufr, '#%d#dominantSwellWavelengthOfSpectralPartition' % (p + 1), value)

            value = int(self.dic_var_value['oswIconf'][0][0][p])
            if value < 0: value = 15
            ecc.codes_set(self.bufr, '#%d#confidenceOfInversionForEachPartitionOfSwellWaveSpectra' % (p + 1), value)

            value = float(self.dic_var_value['oswAmbiFac'][0][0][p])
            if value < -1 or value > 1.62143: value = 1.62143
            ecc.codes_set(self.bufr, '#%d#ambiguityRemovalFactorForSwellWavePartition' % (p + 1), value)

            try:
                value = int(self.dic_var_value['oswQualityFlagPartition'][0][0][p])
                if value < 0: value = 15
            except KeyError:
                value = 15
            ecc.codes_set_long(self.bufr, '#%d#qualityFlagForEachPartitionOfSwellWaveSpectra' % (p + 1), value)

        if np.ma.is_masked(self.dic_var_value['oswPartitions']):
            dum = self.dic_var_value['oswPartitions'].astype(np.float32)
            data_osw_partitions = dum.data
            data_osw_partitions[data_osw_partitions == -128] = 255
            data_osw_partitions[data_osw_partitions == -1] = 255
            self.dic_var_value['oswPartitions'] = data_osw_partitions

        for a in range(len(self.dic_dim_value['oswAngularBinSize'])):
            ecc.codes_set(self.bufr, "#%d#directionSpectral" % (a + 1), int(self.dic_var_value['oswPhi'][a]))
            ecc.codes_set_double_array(self.bufr, "#%d#waveNumberSpectral" % (a + 1), self.dic_var_value['oswK'][:60])
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
        output_dir = args.nc2bufr[1]
        crc = args.nc2bufr[2]
        try:
            obj = NetcdfToBufr(nc_filename, output_dir, crc)
            obj.osw_netcdf2bufr()

        except ecc.CodesInternalError as err:
            if args.verbose:
                traceback.print_exc(file=sys.stderr)
            else:
                print(err.msg, file=sys.stderr)
    else:
        logging.error("No valid argument found; try -h.")


if __name__ == "__main__":
    sys.exit(cmdline())
