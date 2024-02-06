# MBU Test Report

## Introduction

### Background/Context

The NetCDF to BUFR conversion tool MBU processor as initially developed by SERCO for ESA.  
CLS took over the responsibility to maintain this software.  
Since version MBU 2.0 the software is maintained by CLS.

### Purpose of this document

This document shows the result of the test session performed following the validation plan.

### Document organisation

Section 1: this introduction  
Section 2: Cent OS 7 results

### Applicable and Reference Documents

#### Applicable Documents

A-1 &nbsp;&nbsp;&nbsp; GMES-DFPR-EOPG-SW-07-00006	Sentinel-1 Product Definitions & Instrument Processing Facility Development Statement of Work, Issue/Revision 4/1, 23-05-2008.  
A-2	&nbsp;&nbsp;&nbsp; Contract Change Notice N.2, Changes in ESRIN Contract No. 21722/08/I_LG, June 21, 2010  

#### Reference Documents

The following documents provide useful reference information associated with this document.  These documents are to be used for information only.  Changes to the date/revision number (if provided) do not make this document out of date.

R-1 &nbsp;&nbsp;&nbsp;	ES-RS-ESA-SY-0007	Mission Requirements Document for the European Radar Observatory Sentinel-1, Issue 1/4, ESA, July 11, 2005  
R-2	&nbsp;&nbsp;&nbsp; Lotfi A., Lefevre M., Hauser D., Chapron B., Collard F., “The impact of using the upgraded processing of ASAR Level 2 wave products in the assimilation system”, Proc. Envisat Symposium, 22-26 April 2007, Montreux  

### Acronyms and Definition

None

## Test Matrix

The following table shows the global test matrix to present test results in a synthetic view.

|Test|Description|Test Results|Final Status|  
|----|---------|------------------|--------------------|  
|MBU_INS_002	|CentOS 7 installation procedure|PASSED|	PASSED|  
|MBU_INS_004	|Centos 7 - MBUProcessor|PASSED	|PASSED|  
|MBU_REG_009	|Centos 7  - Non regression WD_MBU_PROC-000001|  	0 PASSED 26 FAILED	|PASSED The failed tests are related to a change in the way to managed fill value in MBU Process. This behavior is expected. |
|MBU_REG_010	|Centos 7  - Non regression WD_MBU_PROC-000002|	 4 PASSED 62 FAILED	|PASSED The failed tests are related to a change in the way to managed fill value in MBU Process. This behavior is expected|
|MBU_REG_011	|Centos 7  - Non regression WD_MBU_PROC-000003|	 33 PASSED 115 FAILED|	PASSED The failed tests are related to a change in the way to managed fill value in MBU Process. This behavior is expected|
|MBU_REG_012	|Centos 7  - Non regression WD_MBU_PROC_00BDBA| 6 PASSED 40 FAILED|	PASSED The failed tests are related to a change in the way to managed fill value in MBU Process. This behavior is expected|
|MBU_REG_013	|Centos 7  - Non regression WD_MBU_PROC-0122F4_IPF290|	23 PASSED 53 FAILED|	PASSED The failed tests are related to a change in the way to managed fill value in MBU Process. This behavior is expected|
|MBU_REG_014	|Centos 7  - Non regression WD_MBU_PROC_020265|	10 PASSED 14 FAILED|	PASSED The failed tests are related to a change in the way to managed fill value in MBU Process. This behavior is expected|
|MBU_REG_015	|Centos 7  - Non regression WD_MBU_PROC_0202AC|	22 PASSED 46 FAILED|	PASSED The failed tests are related to a change in the way to managed fill value in MBU Process. This behavior is expected|
|MBU_REG_016	|Centos 7  - Non regression WD_MBU_PROC_024190_IPF290|	21 PASSED 77 FAILED|	PASSED The failed tests are related to a change in the way to managed fill value in MBU Process. This behavior is expected|

*Table 1: Test matrix*
