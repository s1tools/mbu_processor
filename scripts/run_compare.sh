data_path=$1
VERSION_REF=$2
VERSION=$3

for jo in $(find ${data_path}/${VERSION_REF}/TEST_DATA -name "JobOrder*xml")
do
    workdir=$(dirname $jo)
    orig_result_dir=${workdir}
    test_result_dir=${data_path}/${VERSION}/TEST_DATA/$(basename $workdir)

    echo $workdir
    echo "-------------------------------"

   for bufr in $(find $orig_result_dir/ -name "*bufr")

   do

       echo $bufr

       bufr_dump -p $bufr > /tmp/mbu_${VERSION_REF}

       echo $test_result_dir/$(basename $bufr)

       bufr_dump -p $test_result_dir/$(basename $bufr) > /tmp/mbu_${VERSION}

       diff -U 3 /tmp/mbu_${VERSION_REF} /tmp/mbu_${VERSION}

       echo ""

   done

done


# usage:  bash run_compare.sh /net/sentinel1/tmp/mgoacolou/test_mbu 2.1 3.1 > MBU_test_result_2.1_vs_3.1.txt

