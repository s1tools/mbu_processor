#!/bin/bash
export USER_NAME=$(id -un)
export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
export reg=esa/mbu
export name="docker_mbu_dev"

src_dir=$(dirname $(readlink -f $0))

docker build --no-cache \
       -t registry.brest.cls.fr/$reg:$USER_NAME \
       --build-arg userid=$USER_ID --build-arg groupid=$GROUP_ID \
       -f Dockerfile_buildMBUDev_c6_py3 \
       .

docker container prune -f

docker run --name $name -v $(dirname $src_dir):/src \
           -v $VIRTUAL_ENV:/docker_MBU \
           -ti registry.brest.cls.fr/$reg:$USER_NAME  \
           bash /src/scripts/install_mbu_dev.sh

docker commit -m $name $name registry.brest.cls.fr/$reg:$USER_NAME
