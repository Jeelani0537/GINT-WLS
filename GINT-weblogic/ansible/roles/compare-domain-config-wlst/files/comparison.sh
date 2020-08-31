#!bin/bash

tmp_dir=$1
flag=1

debug()
{ 
  first=$1
  second=$2
  echo "#############################################################################################################"
  echo "Items on left are from $first and right are from $second"
  echo "#############################################################################################################"
}

for f in `ls $tmp_dir`
do
  #eval file$flag=$tmp_dir/$f
  eval file$flag=$f
  flag=$((flag+1))
done

#echo "$file1 | $file2"

debug $file1 $file2
diff -y $tmp_dir/$file1 $tmp_dir/$file2
debug $file1 $file2
