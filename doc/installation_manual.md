# MBU Installation and User Manual



## Introduction


### Background/Context

The NetCDF to BUFR _conversion_ tool MBU processor was initially developed by SERCO for ESA. 

CLS took over the responsibility to maintain this software. Starting from version 2.0, the maintenance is thus performed by CLS. 

```
                 ---------------------------------------
INPUT: NETCDF => | bufr_encode_sentinel1               |=> OUTPUT: BUFR
                 | library: eccodes (wrapping gribapi) |
                 ---------------------------------------
```
