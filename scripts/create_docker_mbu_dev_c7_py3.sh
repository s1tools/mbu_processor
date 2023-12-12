#!/bin/bash
set -e

export USER_NAME=$(id -un)
export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
export reg=esa/mbu_c7
export name="docker_mbu_dev_c7"
export REGISTER=registry.brest.cls.fr/$reg:$USER_NAME

src_dir=$(dirname $(readlink -f $0))
echo $(dirname $src_dir)
docker build --no-cache \
       -t $REGISTER \
       --build-arg userid=$USER_ID \
       --build-arg groupid=$GROUP_ID \
       -f Dockerfile_buildMBUDev_c7_py3 \
       .

docker container prune -f

docker run --name $name -v $(dirname $src_dir):/src \
           -v $VIRTUAL_ENV:/docker_MBU \
           -ti $REGISTER  \
           bash /src/scripts/install_mbu_dev.sh

docker commit -m $name $name $REGISTER
