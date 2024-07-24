
build_dev=/bin/bash bin/create_docker_dev_c7.sh
USER_NAME=$(shell id -un)
USER_ID=$(shell id -u)
GROUP_ID=$(shell id -g)
reg=esa/mbu_c7
REGISTER?=registry.brest.cls.fr/${reg}:${USER_NAME}
name=docker_lop_dev
SRC_DIR=$(shell dirname $(shell pwd))
MBU_SRC_DIR=$(shell pwd)/..

.PHONY: dev_env


main_image:
	docker build -f Dockerfile_build_MBU_RPM_c7_py3 -t registry.brest.cls.fr/esa/docker_ipf:build_MBU_RPM_c7_py3 .

dev_env: main_image
	./create_docker_mbu_dev_c7_py3.sh

dev_run:
	docker run -v $(MBU_SRC_DIR):/src \
           -v /net/sentinel1/IPF_MAINTENANCE/ipf_test/datasets/python3:/data/workspace/processing:slave \
           -v /net:/net:slave \
           -v $(HOME):$(HOME) \
           -e ECCODES_DEFINITION_PATH=/src/src/mbu/conf:/usr/local/components/MBU-3.1/share/eccodes/definitions \
	   -ti $(REGISTER) \
	   bash

build_test_image:
	docker build --no-cache -f Dockerfile_test_c7_py3 \
           --build-arg userid=$(USER_ID) \
           --build-arg groupid=$(GROUP_ID) \
           -t registry.brest.cls.fr/esa/docker_ipf:test_mbu . 

run_test:
	docker run --rm \
          -v $(MBU_SRC_DIR):/home/user \
	  -v $(HOME):$(HOME) \
	  -v $(HOME)/data/TEST_DATA_1.2:/data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA \
	  -v /net:/net:slave \
	  -ti registry.brest.cls.fr/esa/docker_ipf:test_mbu bash

build_rpm:
	docker run -v $(MBU_SRC_DIR):/src \
           -v $(MBU_SRC_DIR):/home/user \
	   -ti $(REGISTER) \
	   /src/scripts/make-mbu-rpm
