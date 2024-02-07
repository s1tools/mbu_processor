# MBU Installation and User Manual

## 1 Introduction

### 1.1 Background/Context

The NetCDF to BUFR _conversion_ tool MBU processor was initially developed by SERCO for ESA. 

CLS took over the responsibility to maintain this software. Starting from version 2.0, the maintenance is thus performed by CLS. 

### 1.2 Purpose of this document

The purpose of this document is to describe:
-	The objective, architecture, and way to use the NetCDF to BUFR conversion tool.
-	The requirements before installation 
-	The procedure for installation

### 1.3 Document organisation

Section 1: this introduction

Section 2: the installation manual

Section 3: the user manual

Section 4: the development manual

### 1.4 Applicable and Reference Documents

#### Applicable Documents

| [IPF-ICD] | ESA Generic Processor ICD | GMES-GSEG-EOPG-TN-090016 Issue 1, Revision 0, 24 sept 2009 |
|-----------|:-------------------------:|-----------------------------------------------------------:|

#### Reference Documents

The following documents provide useful reference information associated with this document.  These documents are to be used for information only.  Changes to the date/revision number (if provided) do not make this document out of date.

| [BUFR-TR] | NetCDF to BUFR 3.0 Validation Report | DI-MPC-BUFR-VR MPC-0500 version 1.0 |
|-----------|--------------------------------------|-------------------------------------|

### 1.5 Acronyms and Definition

**IPF** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Instrument Processing Facility  
**MBU** &nbsp;&nbsp;&nbsp;   	Meteo BUfr : processor for conversion of S1 WV OCN products into Bufr format

## 2 Installation Manual

### 2.1 Requirements

#### Hardware requirements

This section describes the minimum hardware required to install and operate the software.

| Type | Description |
|-----------|-------------|
| Processor | x86_64 |
|RAM | 1Go|
|Storage|1Go|
|Network|N/A|
|Other|-|

#### Operating System

This section describes the minimum operating system required to install and operate the software.

| Type | Description |
|--------|--------------------------------------------|
| OS | CentOS 7 / Red Hat Enterprise Linux 7.8 |

#### Software requirements

This section describes the minimum software components required to install and operate the software. They are provided by CLS together with the software.
For CentOS 7.8 / RHEL 7

| Type | Description |
|------------------|--------------------------------------------|
| netcdf-4.3.3.1-5.el7.x86_64 | NetCDF library |
| hdf5-1.8.12-11.el7.x86_64 |	HDF5 library|
|blas-3.4.2-8.el7.x86_64 |	The Basic Linear Algebra Subprograms library (dependency of Numpy) |
| libgfortran-4.8.5-44.el7.x86_64	| This package contains Fortran shared library which is needed to run Fortran dynamically linked programs contained in Numpy. |
| lapack-3.4.2-8.el7.x86_64	| LAPACK (Linear Algebra PACKage) (dependency of Numpy) |
| atlas-3.10.1-12.el7.x86_64	| The ATLAS (Automatically Tuned Linear Algebra Software) (dependency of Numpy) |

### 2.2 Installation procedure

The NetCDF to Bufr transformer is a full consistent RPM containing software and its dependencies as described in Software requirements section.  
As root user:
> yum install -y /path/to/S1PD-MBU-3.0-0.x86_64.rpm

## 3 User Manual

### 3.1 Purpose of the tool

The MBU processor (Meteo BUffer data) allows to convert NetCDF files from WV-OCN products to BUFR format.  
The core BUFR converter has been implemented by ECMWF and used the library ECCODES (https://confluence.ecmwf.int/display/ECC/ecCodes+Home) a wrapping of GRIBAPI (Figure 1)  
Change with 3.0: new quality flags added for swell partitions and swell inversion in exported Bufr. At the time of writing, eccodes do not contains new codes for new quality flags yet.

### 3.2 Architecture

```
                 ---------------------------------------
INPUT: NETCDF => | bufr_encode_sentinel1               |=> OUTPUT: BUFR
                 | library: eccodes (wrapping gribapi) |
                 ---------------------------------------
```
*Figure 1 - Sample code provided by ECMWF*

ESA has implemented the wrapper interface for the PDGS (Figure 2). It takes as input  a working directory including SAFE product and a Joborder file to perform the conversion.
![Figure 2](https://github.com/s1tools/mbu_processor/blob/upload_documentation/doc/MBU_installation_manual_fig-2.png)  
*Figure 2 - Wrapping of WV OCN to BUFR*

### 3.3 Configuration

It is not expected that the user changes the configuration. Inner configuration is embedded in the MBU python package.

### 3.4 Example of manual operation

To run the MBU conversion from a JobOrder file, proceed as follows: 
```
MBUprocessor /data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/JobOrder.000001.xml
```
The output files will be available as defined in the Output section of the JobOrder file.

To run the MBU conversion from a NetCDF file, proceed as follows: 
```
bufr_encode_sentinel1 --nc2bufr path/to/the/netCDF/file.nc output_directory CRC_ID  
*example*:  
bufr_encode_sentinel1 --nc2bufr /data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/S1B_WV_OCN__2SSV_20190628T190957_20190628T191606_016900_01FCE3_C26C.SAFE/measurement/s1b-wv2-ocn-vv-20190628t191435-20190628t191438-016900-01fce3-020.nc /tmp/ C26C
```

## 4 Development manual

### 4.1 Source code

The code is organized as follows:
```
MBUProcess
├── MANIFEST.in
├── scripts
│   ├── create_docker_mbu_dev_c7_py3.sh  # create the dev environment in CentOS 7
│   ├── docker-compose.yml_template      # docker-compose template for easiest use of docker
│   ├── Dockerfile_buildMBUDev_c7_py3    # specific instruction for development environment
│   ├── Dockerfile_build_MBU_RPM_c7_py3  # docker image base script
│   ├── install_mbu_dev.sh               # install MBU source in dev mode
│   ├── make-mbu-rpm                     # RPM creation script
│   ├── mbuprocessor-rpm.spec            # specification of RPM creation
│   ├── README.md                        # description of installation/RPM/dev process
│   └── share
├── setup.py                             # python package installation file
└── src                                  # python sources
    └── mbu                              # MBU python package
```

### 4.2 Version control

The different versions of the tool are tracked in a git system operated by GitHub:
https://github.com/s1tools/mbu_processor

### 4.3 Unit tests

Under construction

### 4.4 Process to build the RPM

Create the docker image from 
```
scripts/Dockerfile_build_MBU_RPM_c6_py3
cd scripts

$ # Cent OS 7
$ make build_rpm
```
### 4.5 Validation Plan

Refer to document [Validation Plan](./MBU_test_plan.md)

### 4.6 Test Report

Refer to document [Test Report](./MBU_test_report.md)
