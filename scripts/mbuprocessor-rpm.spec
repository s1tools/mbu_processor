%{!?__python3: %global __python3 /usr/local/components/MBU-3.0/bin/python3.9}
%global __python %{__python3}
%global _pylib /usr/local/components/MBU-3.0/lib/python3.9/site-packages

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%define VER %(echo $CADUVER)
%define REL %(echo $CADUREL)
Name:           S1PD-MBU
Version:        3.0
Release:        0
Summary:        MBU Processor

Group:          Applications/Archiving
License:        (C) CLS
URL:            https://cls.fr/
BuildArch:      x86_64
Requires: libcurl,hdf5,netcdf,lapack,blas,atlas
%description
Processor name: MBU (Meteo BUffer data) Processor
#%{_topdir}            %{getenv:HOME}/rpmbuild
#%{_builddir}          %{_topdir}/BUILD
#%{_rpmdir}            %{_topdir}/RPMS
#%{_sourcedir}         %{_topdir}/SOURCES
#%{_specdir}           %{_topdir}/SPECS
#%{_srcrpmdir}         %{_topdir}/SRPMS
#%{_buildrootdir}      %{_topdir}/BUILDROOT

%install
echo ${RPM_BUILD_ROOT}
cp -r /home/user/rpmbuild/BUILD/* ${RPM_BUILD_ROOT}

%clean

%files
%defattr(755,root,root,755)
%doc
/*

%changelog

%post

# instalation long file
LOG_FILE="/tmp/MBU_config_LOG.txt"

#
# log both stdout file
#
function logMsg {
    echo -En ""
    echo -e "${1}"
    echo -e "${1}" >> "${LOG_FILE}"
}

#
# log info msg
#
function logInfo {
    echo -En ""
    echo -e "[${vertfonce}INFO${neutre} ]${1}"
    echo -e "[INFO ]${1}" >> "${LOG_FILE}"
}

#
# log ok msg
#
function logOk {
    echo -En ""
    echo -e "[${vertclair}OK${neutre}   ]${1}"
    echo -e "[OK   ] ${1}" >> "${LOG_FILE}"
}

#
# log warning msg
#
function logWarning {
    echo -En ""
    echo -e "[${orange}WARN${neutre} ]${1}"
    echo -e "[WARN ]${1}" >> "${LOG_FILE}"
}

#
# log error msg
#
function logError {
    echo -En ""
    echo -e "[${rouge}ERROR${neutre}]${1}"
    echo -e "[ERROR] ${1}" >> "${LOG_FILE}"
}

#
# log cmd msg
#
function logCmd {
    echo -En ""
    echo -e "[CMD ]${1}" >> "${LOG_FILE}"
}




INSTALL_DIR="/usr/local/components/"
VERSIONNED_FOLDER_NAME="MBU-3.0"
UNVERSIONNED_FOLDER_NAME="MBU"

VERSIONNED_PROJECT_HOME=${INSTALL_DIR}/${VERSIONNED_FOLDER_NAME}
UNVERSIONNED_PROJECT_HOME=${INSTALL_DIR}/${UNVERSIONNED_FOLDER_NAME}


MBU_OWNER=piccontrol
MBU_GROUP=pic_run
# link unversioned path to new path
function link_MBU {
        echo "link_MBU"
        if [ -e "${VERSIONNED_PROJECT_HOME}" ] ; then
                logInfo "link "${VERSIONNED_PROJECT_HOME}" to "${UNVERSIONNED_PROJECT_HOME}
                ln -s ${VERSIONNED_PROJECT_HOME} ${UNVERSIONNED_PROJECT_HOME}
        else
                logError "${VERSIONNED_PROJECT_HOME} file not found could not create unversioned link ${UNVERSIONNED_PROJECT_HOME}"
        fi
}

function change_MBU_owner {
        if [[ -e "${VERSIONNED_PROJECT_HOME}" ]] ; then
                logInfo "change owner for project dir"
                chown -R ${MBU_OWNER}:${MBU_GROUP} ${VERSIONNED_PROJECT_HOME}
		chmod 775 ${VERSIONNED_PROJECT_HOME}
		chown -R ${MBU_OWNER}:${MBU_GROUP} ${UNVERSIONNED_PROJECT_HOME}
                chmod 775 ${UNVERSIONNED_PROJECT_HOME}
        else
                logError "${VERSIONNED_PROJECT_HOME} file not found could not set owner and group to ${MBU_OWNER}:${MBU_GROUP}"
                logError "${UNVERSIONNED_PROJECT_HOME} file not found could not set owner and group to ${MBU_OWNER}:${MBU_GROUP}"
        fi
}

function configure {
	link_MBU
    change_MBU_owner
}

configure

echo "Congratulations !! You installed the MBUprocessor."
echo "Have a nice beer."

