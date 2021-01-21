===========================
MBU Processor build process
===========================

build main
==========

these commands build the mais docker image with all needed except MBUProcess python package

```bash
cd /path/to/MBUProcess/scripts

# CentOS 6
docker build -f Dockerfile_build_MBU_RPM_c6_py3 -t registry.brest.cls.fr/esa/docker_ipf:build_MBU_RPM_c6_py3

# CentOS 7
docker build -f Dockerfile_build_MBU_RPM_c7_py3 -t registry.brest.cls.fr/esa/docker_ipf:build_MBU_RPM_c7_py3 
```


build developper image
======================

this add the user with same ids as the linux user who start the script
it also install MBUProcess package in developer mode

```bash
cd /path/to/MBUProcess/scripts

# CentOS 6
./create_docker_mbu_dev_c6_py3.sh

# CentOS 7
./create_docker_mbu_dev_c7_py3.sh
```

run in developper mode
======================

only docker
-----------

```
# CentOS 6
docker run -v /path/to/MBUProcess:/src \
           -v /net/sentinel1/IPF_MAINTENANCE/ipf_test/datasets/python3:/data/workspace/processing:slave \
	   -ti registry.brest.cls.fr/esa/mbu:${USER} \
	   bash

# CentOS 7
docker run -v /path/to/MBUProcess:/src \
           -v /net/sentinel1/IPF_MAINTENANCE/ipf_test/datasets/python3:/data/workspace/processing:slave \
	   -ti registry.brest.cls.fr/esa/mbu_c7:${USER} \
	   bash
```

docker-compose
--------------

initialise the docker-compose file

```
cd /path/to/MBUProcess/scripts
# use envsubst to make the docker-compose.yml
envsubst < docker-compose.yml_template > docker-compose.yml
```

run

```
docker-compose run MBU_c6 bash
docker-compose run MBU_c7 bash
```


build rpm
=========



only docker
-----------

```
# CentOS 6
docker run -v /path/to/MBUProcess:/src \
           -v /path/to/output_rpms:/home/user \
	   -ti registry.brest.cls.fr/esa/mbu:${USER} \
	   /src/scripts/make-mbu-rpm

# CentOS 7
docker run -v /path/to/MBUProcess:/src \
           -v /path/to/output_rpms:/home/user \
	   -ti registry.brest.cls.fr/esa/mbu_c7:${USER} \
	   /src/scripts/make-mbu-rpm
```
RPMS must copyied some else at each steps because these process overwrite the results

docker-compose
--------------

initialise the docker-compose file first if not done


```
docker-compose run MBU_c6 /src/scripts/make-mbu-rpm
docker-compose run MBU_c7 /src/scripts/make-mbu-rpm
```

RPMS must copyied some else at each steps because these process overwrite the results

