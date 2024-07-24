MBU Processor build process
===========================

build main
----------

these commands build the main docker image with all needed except MBUProcess python package

```bash
cd /path/to/MBUProcess/scripts

# CentOS 7
docker build -f Dockerfile_build_MBU_RPM_c7_py3 -t registry.brest.cls.fr/esa/docker_ipf:build_MBU_RPM_c7_py3 .
```


build developper image
----------------------

this add the user with same ids as the linux user who start the script
it also install MBUProcess package in developer mode

```bash
cd /path/to/MBUProcess/scripts

# CentOS 7
./create_docker_mbu_dev_c7_py3.sh
```

run in developper mode
----------------------

```
# CentOS 7
docker run -v /path/to/MBUProcess:/src \
           -v /net/sentinel1/IPF_MAINTENANCE/ipf_test/datasets/python3:/data/workspace/processing:slave \
           -e ECCODES_DEFINITION_PATH=/src/src/mbu/conf:/usr/local/components/MBU-3.1/share/eccodes/definitions \
	   -ti registry.brest.cls.fr/esa/mbu_c7:${USER} \
	   bash
```

build rpm
---------


```bash
# CentOS 7
docker run -v /path/to/MBUProcess:/src \
           -v /path/to/output_rpms:/home/user \
	   -ti registry.brest.cls.fr/esa/mbu_c7:${USER} \
	   /src/scripts/make-mbu-rpm
```
RPMS must copyied some else at each steps because these process overwrite the results


install RPM
-----------

### centOS 7

```bash
docker run -v /home/mgoacolou/pyve/docker_IPF_py3:/venv \
           -v /home/mgoacolou/pyve/docker_IPF_py3/src/bufr/02-MBU_RPM/software/MBU_1.2.0:/data/GIOVANNA/BUILD_RPM_1.2.0 \
	   -ti centos:7 bash

yum install epel-release

# dowload dependencies
yum install --downloadonly --downloaddir=/venv/rpmbuild_c7/RPMS/x86_64/ /venv/rpmbuild_c7/RPMS/x86_64/S1PD-MBU-2.0-0.x86_64.rpm

yum install -y /venv/rpmbuild_c7/RPMS/x86_64/S1PD-MBU-2.0-0.x86_64.rpm
export PATH=$PATH:/usr/local/components/MBU/bin/

```


compare previous version
------------------------

```bash
orig_result_dir=/home/mgoacolou/pyve/docker_IPF_py3/src/bufr/02-MBU_RPM/software/MBU_1.2.0/TEST_DATA_orig
test_result_dir=/home/mgoacolou/pyve/docker_IPF_py3/src/bufr/02-MBU_RPM/software/MBU_1.2.0/TEST_DATA_test

for workdir in $(ls $orig_result_dir)
do echo $workdir
   for bufr in $(find $orig_result_dir/$workdir/ -name "*bufr")
   do
       echo $bufr
       bufr_dump -p $bufr > /tmp/mbu_1.2
       echo $test_result_dir/$workdir/$(basename $bufr)
       bufr_dump -p $test_result_dir/$workdir/$(basename $bufr) > /tmp/mbu_2.0
       diff -U 3 /tmp/mbu_1.2 /tmp/mbu_2.0
       echo ""
   done
done
```