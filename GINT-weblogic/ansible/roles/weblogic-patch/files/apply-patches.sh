#script.sh $patch_dir $FMW_HOME $fmw_ver

patch_dir=$1
FMW_HOME=$2
fmw_ver=$3

opatch_home=$FMW_HOME"/OPatch"

echo "Patch directory received: $patch_dir"
printf "\n\n"

echo "FMW_Home received: $FMW_HOME"
printf "\n\n"

cd $patch_dir
for dir in $(ls $patch_dir)
do
  cd $patch_dir/$dir
  if [ -f opatch_generic.jar ]
  then
    echo "opatch_generic.jar is found"
    /opt/oracle/java/bin/java -jar opatch_generic.jar -silent oracle_home=$FMW_HOME
  else
    echo "Applying patch $patchDir through opatch"
    $opatch_home/opatch apply -silent  
  fi
done

printf "\n"
