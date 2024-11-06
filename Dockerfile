FROM debian:12 AS builder

MAINTAINER Manuel GOACOLOU <mgoacolou@groupcls.com>

USER root
ARG VERSION=3.1


RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-numpy python3-venv

RUN python3 -m venv --symlinks --system-site-packages /usr/local/components/MBU-${VERSION}/ \
    && ln -s /usr/local/components/MBU-${VERSION} /usr/local/components/MBU


RUN /usr/local/components/MBU-${VERSION}/bin/python3 -m pip install eccodes

ADD debian/libeccodes-data_2.38.3-1_all.deb /tmp
RUN dpkg -i /tmp/libeccodes-data_2.38.3-1_all.deb
ENV ECCODES_DEFINITION_PATH=/usr/share/eccodes/definitions

ADD dist/Sentinel1_MBU_Processor-${VERSION}.0-py3-none-any.whl /tmp/Sentinel1_MBU_Processor-${VERSION}.0-py3-none-any.whl
RUN /usr/local/components/MBU-${VERSION}/bin/python3 -m pip install /tmp/Sentinel1_MBU_Processor-${VERSION}.0-py3-none-any.whl

