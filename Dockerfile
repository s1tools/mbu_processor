FROM debian:12

LABEL  Maintainer="Manuel GOACOLOU <mgoacolou@groupcls.com>"

USER root
ARG VERSION=3.1
ARG UID=1046
ARG GID=2000


RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-numpy python3-venv wget \
    && apt-get clean

RUN python3 -m venv --symlinks --system-site-packages /usr/local/components/MBU-${VERSION}/ \
    && ln -s /usr/local/components/MBU-${VERSION} /usr/local/components/MBU


# install eccodes: python package do not contains the definitions
RUN /usr/local/components/MBU-${VERSION}/bin/python3 -m pip install eccodes

# get the debian data package for definitions
RUN wget http://ftp.fr.debian.org/debian/pool/main/e/eccodes/libeccodes-data_2.38.3-1_all.deb \
    && dpkg -i libeccodes-data_2.38.3-1_all.deb \
    && rm libeccodes-data_2.38.3-1_all.deb

# setup the definitions
ENV ECCODES_DEFINITION_PATH=/usr/share/eccodes/definitions

# install MBU
ADD dist/Sentinel1_MBU_Processor-${VERSION}.0-py3-none-any.whl /tmp/Sentinel1_MBU_Processor-${VERSION}.0-py3-none-any.whl
RUN /usr/local/components/MBU-${VERSION}/bin/python3 -m pip install /tmp/Sentinel1_MBU_Processor-${VERSION}.0-py3-none-any.whl

USER ${UID}:${GID}
ENV PATH=${PATH}:/usr/local/components/MBU/bin
#ENTRYPOINT ["/usr/local/components/MBU/bin/MBUprocessor"]

