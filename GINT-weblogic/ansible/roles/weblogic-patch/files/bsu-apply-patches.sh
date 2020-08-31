#script.sh $fmwver

fmwver=$1

cd /opt/oracle/FMW$fmwver/utils/bsu/cache_dir

if [ -f bsu_update.sh ]
then
  echo "Found bsu_update.sh"
  cp /opt/oracle/FMW$fmwver/utils/bsu/cache_dir/bsu_update.sh /opt/oracle/FMW$fmwver/utils/bsu/
  cd /opt/oracle/FMW$fmwver/utils/bsu/
  . ./bsu_update.sh install
else
  patch_id=`ls *.jar | awk -F'.' '{print $1}'`
  [[ ! -z "$patch_id" ]] && cd /opt/oracle/FMW$fmwver/utils/bsu && sed -i 's/Xms512m/Xms8g/g' bsu.sh && sed -i 's/Xmx1g/Xmx8g/g' bsu.sh && sed -i 's/Xms2g/Xms8g/g' bsu.sh && sed -i 's/Xmx2g/Xmx8g/g' bsu.sh && ./bsu.sh -install -patch_download_dir=/opt/oracle/FMW$fmwver/utils/bsu/cache_dir -patchlist=$patch_id -prod_dir=/opt/oracle/FMW$fmwver/wlserver_10.3
fi
