datset_path=$1
VERSION_REF=$2
VERSION=$3

for jo in $(find ${datset_path} -name "JobOrder*xml")
do
    workdir=$(dirname $jo)
    orig_result_dir=${workdir}/mbu-${VERSION_REF}
    test_result_dir=${workdir}/mbu-${VERSION}

    echo $workdir
    echo "-------------------------------"

   for bufr in $(find $orig_result_dir/ -name "*bufr")

   do

       echo $bufr

       bufr_dump -p $bufr > /tmp/mbu_2.0

       echo $test_result_dir/$(basename $bufr)

       bufr_dump -p $test_result_dir/$(basename $bufr) > /tmp/mbu_3.0

       diff -U 3 /tmp/mbu_2.0 /tmp/mbu_3.0

       echo ""

   done

done


# usage:  bash run_compare.sh /home/mgoacolou/data/TEST_DATA_1.2 2.0 3.0 > MBU_test_result_2.0_vs_3.0.txt

