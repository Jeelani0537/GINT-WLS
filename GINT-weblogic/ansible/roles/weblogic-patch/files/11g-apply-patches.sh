patch_dir=$1
stack=$2
fmw_ver=$3

if [ "$stack" = "soa" ]
then
  export ORACLE_HOME="/opt/oracle/FMW$fmw_ver/Oracle_SOA1/"
fi

export PATH=$PATH:$ORACLE_HOME/OPatch

echo "Patch directory received: $patch_dir"
echo "Stack received: $stack"
printf "\n"

for dir in $(ls $patch_dir)
do
  cd $patch_dir/$dir/oui
  opatch apply -silent
done

