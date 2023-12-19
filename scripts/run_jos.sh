VERSION=$1
sudo yum install -y /home/user/S1PD-MBU-${VERSION}-0.x86_64.rpm

for jo in $(find /data/GIOVANNA/BUILD_RPM_1.2.0/TEST_DATA/ -name "JobOrder*xml")
 do
    echo $(dirname $jo)
    # run the production of bufr files
    /usr/local/components/MBU/bin/MBUprocessor $jo
    # copy results into results folder
    resultfolder=$(dirname $jo)/mbu-${VERSION}
    rm -Rf $resultfolder
    mkdir -p $resultfolder
    mv $(dirname $jo)/*bufr $resultfolder
    mv $(dirname $jo)/*INTERNALLOG $resultfolder
    mv $(dirname $jo)/*LIST $resultfolder
    echo
done