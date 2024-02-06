# MBU Test Plan

## Introduction

### Background/Context

The NetCDF to BUFR conversion tool MBU processor as initially developed by SERCO for ESA.  
CLS took over the responsibility to maintain this software.  
Starting from MBU 2.0 this software is maintained by CLS.  

### Purpose of this document

This document describes the validation plan of the NetCDF to Bufr software:
- Test requirements
- Input data
- Test cases
- Test steps

### Document organisation

Section 1: this introduction  
Section 2: Test of the installation procedure  
Section 3: Test of the MBU processor software  
Section 4: Test of Non regression

### Applicable and Reference Documents

#### Applicable Documents

A-1	&nbsp;&nbsp;&nbsp; GMES-DFPR-EOPG-SW-07-00006	Sentinel-1 Product Definitions & Instrument Processing Facility Development Statement of Work, Issue/Revision 4/1, 23-05-2008.  
A-2 &nbsp;&nbsp;&nbsp;	Contract Change Notice N.2, Changes in ESRIN Contract No. 21722/08/I_LG, June 21, 2010  

#### Reference Documents

The following documents provide useful reference information associated with this document.  These documents are to be used for information only.  Changes to the date/revision number (if provided) do not make this document out of date.  

R-1	&nbsp;&nbsp;&nbsp; ES-RS-ESA-SY-0007	Mission Requirements Document for the European Radar Observatory Sentinel-1, Issue 1/4, ESA, July 11, 2005  
R-2	&nbsp;&nbsp;&nbsp; Lotfi A., Lefevre M., Hauser D., Chapron B., Collard F., “The impact of using the upgraded processing of ASAR Level 2 wave products in the assimilation system”, Proc. Envisat Symposium, 22-26 April 2007, Montreux

### Acronyms and Definition

CO: CentOS  
RH: Red Hat

## Test of the installation procedure

This test consists of the installation of MBU and verify that it works properly.  
**Test Type**: Nominal  
**Test Stubs**:
```
Cent OS 7 environment
docker run -v /path/to/rpm:/venv -v /path/to/bufr/TEST_DATA:/data/GIOVANNA/BUILD_RPM_1.2.0 -ti centos:7 bash
```
### Input Data
- MBU RPM for RH/CO 7

### Output

#### Output Data
N/A

#### Expected results, specific points to check
The installation finish without any error.

### Starting conditions

None

### Actions after test execution

None

### Test cases

|Test|Description|
|---|---|
|MBU_INS_001	|CentOS 7 installation procedure|

*Table 1: Installation procedure test cases*

### Detailed test steps
The following steps allows to test the installation procedures of MBU.
- Install RPM
```
yum install -y /venv/RPM/S1PD-MBU-3.0-0.x86_64.rpm
```
- Check presence of MBUprocessor script
```
ls /usr/local/components/
MBU MBU-3.0
ls /usr/local/components/MBU-3.0/bin/MBUprocessor
/usr/local/components/MBU-3.0/bin/MBUprocessor
```
## Test of MBUprocessor software

The test consists of launching the MBUProcessor and verify that it works properly.  
**Test Type**: Nominal  
**Test Stubs**:
```
Cent OS 7 environment:
docker run -v /path/to/rpm:/venv -v /path/to/bufr/TEST_DATA:/data/GIOVANNA/BUILD_RPM_1.2.0 -ti centos:7 bash
```

### Input Data

-	MBU RPM for RH/CO 7
-	TEST DATA provided with MBU 1.2.0:

|Name|Description|
|---|---|
|WD_MBU_PROC-000001  	|Working directory (JobOrder + NetCDF) provided with MBU 1.2.0|
|WD_MBU_PROC-000002	|Working directory (JobOrder + NetCDF) provided with MBU 1.2.0|
|WD_MBU_PROC-000003	|Working directory (JobOrder + NetCDF) provided with MBU 1.2.|
|WD_MBU_PROC_00BDBA |Working directory (JobOrder + NetCDF) provided with MBU 1.2.0|
|WD_MBU_PROC-0122F4_IPF290	|Working directory (JobOrder + NetCDF) provided with MBU 1.2.0|
|WD_MBU_PROC_020265	|Working directory (JobOrder + NetCDF) provided with MBU 1.2.0|
|WD_MBU_PROC_0202AC	|Working directory (JobOrder + NetCDF) provided with MBU 1.2.0|
|WD_MBU_PROC_024190_IPF290	|Working directory (JobOrder + NetCDF) provided with MBU 1.2.0|

*Table 2: Test data*

### Output
#### Output Data
N/A

#### Expected results, specific points to check

The execution finish without any error.  
The new quality flags are present.

### Starting Conditions
Installation test must be done without error.  
Add of MBU Processor in the path:
```
export PATH=$PATH:/usr/local/components/MBU-3.0/bin
```
### Actions after test execution

None

### Test cases

The test cases are the following: 
|Test|Description|
|---|---|
|MBU_INS_004	|Centos 7 - MBUProcessor|

*Table 3: Run MBU Processor test cases*

### Detailed test steps

The following steps allows to perform the MBU launching tests.
- Run execution for one JobOrder
```
MBUprocessor /data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/JobOrder.000001.xml
```
- Check presence of bufr files
```
ls /data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/
JobOrder.000001.xml
S1B_WV_OCN__2SSV_20190628T190957_20190628T191606_016900_01FCE3_C26C.SAFE
WD_MBU_PROC-000001.INTERNALLOG
WD_MBU_PROC-000001.LIST
s1b-wv1-mbu-vv-20190628t190957-20190628t191000-016900-01fce3-001_C26C.bufr
s1b-wv1-mbu-vv-20190628t191026-20190628t191029-016900-01fce3-003_C26C.bufr
s1b-wv1-mbu-vv-20190628t191055-20190628t191058-016900-01fce3-005_C26C.bufr
s1b-wv1-mbu-vv-20190628t191125-20190628t191128-016900-01fce3-007_C26C.bufr
s1b-wv1-mbu-vv-20190628t191154-20190628t191157-016900-01fce3-009_C26C.bufr
s1b-wv1-mbu-vv-20190628t191223-20190628t191226-016900-01fce3-011_C26C.bufr
s1b-wv1-mbu-vv-20190628t191252-20190628t191255-016900-01fce3-013_C26C.bufr
s1b-wv1-mbu-vv-20190628t191322-20190628t191325-016900-01fce3-015_C26C.bufr
s1b-wv1-mbu-vv-20190628t191351-20190628t191354-016900-01fce3-017_C26C.bufr
s1b-wv1-mbu-vv-20190628t191420-20190628t191423-016900-01fce3-019_C26C.bufr
s1b-wv1-mbu-vv-20190628t191450-20190628t191453-016900-01fce3-021_C26C.bufr
s1b-wv1-mbu-vv-20190628t191519-20190628t191522-016900-01fce3-023_C26C.bufr
s1b-wv1-mbu-vv-20190628t191548-20190628t191551-016900-01fce3-025_C26C.bufr
s1b-wv2-mbu-vv-20190628t191011-20190628t191014-016900-01fce3-002_C26C.bufr
s1b-wv2-mbu-vv-20190628t191041-20190628t191044-016900-01fce3-004_C26C.bufr
s1b-wv2-mbu-vv-20190628t191110-20190628t191113-016900-01fce3-006_C26C.bufr
s1b-wv2-mbu-vv-20190628t191139-20190628t191142-016900-01fce3-008_C26C.bufr
s1b-wv2-mbu-vv-20190628t191209-20190628t191211-016900-01fce3-010_C26C.bufr
s1b-wv2-mbu-vv-20190628t191238-20190628t191241-016900-01fce3-012_C26C.bufr
s1b-wv2-mbu-vv-20190628t191307-20190628t191310-016900-01fce3-014_C26C.bufr
s1b-wv2-mbu-vv-20190628t191336-20190628t191339-016900-01fce3-016_C26C.bufr
s1b-wv2-mbu-vv-20190628t191406-20190628t191409-016900-01fce3-018_C26C.bufr
s1b-wv2-mbu-vv-20190628t191435-20190628t191438-016900-01fce3-020_C26C.bufr
s1b-wv2-mbu-vv-20190628t191504-20190628t191507-016900-01fce3-022_C26C.bufr
s1b-wv2-mbu-vv-20190628t191534-20190628t191537-016900-01fce3-024_C26C.bufr
s1b-wv2-mbu-vv-20190628t191603-20190628t191606-016900-01fce3-026_C26C.bufr 
```

-	Check the success by printing the tail of WD_MBU_PROC-000001.INTERNALLOG file:
```
tail -n 30 /data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/WD_MBU_PROC-000001.INTERNALLOG 
Created output BUFR file /data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv2-mbu-vv-20190628t191603-20190628t191606-016900-01fce3-026_C26C.bufr
prepareOutputs 
listOutputBUFR: 
{'burfProducts': ['/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv1-mbu-vv-20190628t190957-20190628t191000-016900-01fce3-001_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv2-mbu-vv-20190628t191011-20190628t191014-016900-01fce3-002_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv1-mbu-vv-20190628t191026-20190628t191029-016900-01fce3-003_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv2-mbu-vv-20190628t191041-20190628t191044-016900-01fce3-004_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv1-mbu-vv-20190628t191055-20190628t191058-016900-01fce3-005_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv2-mbu-vv-20190628t191110-20190628t191113-016900-01fce3-006_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv1-mbu-vv-20190628t191125-20190628t191128-016900-01fce3-007_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv2-mbu-vv-20190628t191139-20190628t191142-016900-01fce3-008_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv1-mbu-vv-20190628t191154-20190628t191157-016900-01fce3-009_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv2-mbu-vv-20190628t191209-20190628t191211-016900-01fce3-010_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv1-mbu-vv-20190628t191223-20190628t191226-016900-01fce3-011_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv2-mbu-vv-20190628t191238-20190628t191241-016900-01fce3-012_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv1-mbu-vv-20190628t191252-20190628t191255-016900-01fce3-013_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv2-mbu-vv-20190628t191307-20190628t191310-016900-01fce3-014_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv1-mbu-vv-20190628t191322-20190628t191325-016900-01fce3-015_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv2-mbu-vv-20190628t191336-20190628t191339-016900-01fce3-016_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv1-mbu-vv-20190628t191351-20190628t191354-016900-01fce3-017_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv2-mbu-vv-20190628t191406-20190628t191409-016900-01fce3-018_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv1-mbu-vv-20190628t191420-20190628t191423-016900-01fce3-019_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv2-mbu-vv-20190628t191435-20190628t191438-016900-01fce3-020_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv1-mbu-vv-20190628t191450-20190628t191453-016900-01fce3-021_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv2-mbu-vv-20190628t191504-20190628t191507-016900-01fce3-022_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv1-mbu-vv-20190628t191519-20190628t191522-016900-01fce3-023_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv2-mbu-vv-20190628t191534-20190628t191537-016900-01fce3-024_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv1-mbu-vv-20190628t191548-20190628t191551-016900-01fce3-025_C26C.bufr',
                  '/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/WD_MBU_PROC-000001/s1b-wv2-mbu-vv-20190628t191603-20190628t191606-016900-01fce3-026_C26C.bufr']}
Run completed in 2.030670642852783 seconds:
```

## Test Non regression

This test checks the bufr format produced by MBU  
**Test Type**: Nominal  
**Test Stubs**:
```
Cent OS 7 environment
docker run -v /path/to/rpm:/venv -v /path/to/bufr/TEST_DATA:/data/GIOVANNA/BUILD_RPM_1.2.0 -ti centos:7 bash
```

### Input Data
-	MBU RPM for RH/CO 7
-	Reference TEST DATA: .bufr files test data provided with MBU 1.2:

|Name	|Description|
|---|---|
|WD_MBU_PROC-000001  	|.bufr files provided with MBU 1.2.0|
|WD_MBU_PROC-000002	|.bufr files provided with MBU 1.2.0|
|WD_MBU_PROC-000003	|.bufr files provided with MBU 1.2.0|
|WD_MBU_PROC_00BDBA  	|.bufr files provided with MBU 1.2.0|
|WD_MBU_PROC-0122F4_IPF290	|.bufr files provided with MBU 1.2.0|
|WD_MBU_PROC_020265	|.bufr files provided with MBU 1.2.0|
|WD_MBU_PROC_0202AC	|.bufr files provided with MBU 1.2.0|
|WD_MBU_PROC_024190_IPF290	|.bufr files provided with MBU 1.2.0|

*Table 4 : Test data*

### Output

#### Output Data
All reference bufr files  
MBU_test_result_2.0_vs_3.0.txt containing all comparison results.

#### Expected results, specific points to check
The installation finish without any error.  
All job orders work without any error on terminal.  
There are the same number of bufr files as in previous test data.  
3.0 files contain new quality flags.  

### Starting Conditions

Installation of RPM must be done as describe in “installation test”.  
Add of MBU Processor in the path:
```
export PATH=$PATH:/usr/local/components/MBU-3.0/bin
```

### Actions after test execution

None

### Test cases

The test case consists of run the MBU processor over all JobOrder. Then, a script will compare all the .bufr files produced with the reference .bufr files.  
The test cases are the following:

|Test Id|	Description|
|---|---|
|MBU_REG_009	|Centos 7 - Non regression WD_MBU_PROC-000001 | 
|MBU_REG_010	|Centos 7 - Non regression WD_MBU_PROC-000002|
|MBU_REG_011	|Centos 7 - Non regression WD_MBU_PROC-000003|
|MBU_REG_012	|Centos 7 - Non regression WD_MBU_PROC_00BDBA  |
|MBU_REG_013	|Centos 7 - Non regression WD_MBU_PROC-0122F4_IPF290|
|MBU_REG_014	|Centos 7 - Non regression WD_MBU_PROC_020265|
|MBU_REG_015	|Centos 7  - Non regression WD_MBU_PROC_0202AC|
|MBU_REG_016	|Centos 7  - Non regression WD_MBU_PROC_024190_IPF290|

*Table 5: Non-regression test cases*

### Detailed test steps

The following steps allows to perform the non-regression tests.
-	Run MBUprocessor on all JobOrder with 2.0
```
make run_test
docker run --rm \
          -v /home/mgoacolou/pyve/docker_IPF/src/mbu_processor/scripts/..:/home/user \
  -v /home/mgoacolou:/home/mgoacolou \
  -v /home/mgoacolou/data/TEST_DATA_1.2:/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA \
  -v /net:/net:slave \
  -ti registry.brest.cls.fr/esa/docker_ipf:test_mbu bash
bash-4.2$ cd scripts/
bash-4.2$ bash run_jos.sh 2.0
Loaded plugins: fastestmirror, ovl
...
```

-	Run MBUprocessor on all JobOrder with 3.0
```
make run_test
docker run --rm \
          -v /home/mgoacolou/pyve/docker_IPF/src/mbu_processor/scripts/..:/home/user \
  -v /home/mgoacolou:/home/mgoacolou \
  -v /home/mgoacolou/data/TEST_DATA_1.2:/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA \
  -v /net:/net:slave \
  -ti registry.brest.cls.fr/esa/docker_ipf:test_mbu bash
bash-4.2$ cd scripts/
bash-4.2$ bash run_jos.sh 2.0
Loaded plugins: fastestmirror, ovl
...
```
-	Run comparaison script
```
bash run_compare.sh /home/mgoacolou/data/TEST_DATA_1.2 2.0 3.0 > MBU_test_result_2.0_vs_3.0.txt
```














