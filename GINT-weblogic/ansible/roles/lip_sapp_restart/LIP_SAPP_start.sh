#!bin/bash
DomainDir=/opt/oracle/domains11.1.1.9/
cd $DomainDir
var_lip_domain=$( ls | grep -o LIP[0-9][0-9][0-9] )
var_sapp_domain=$( ls | grep -o SAPP[0-9][0-9][0-9])
cd $var_lip_domain
var_script_m2=$( ls |grep -o start_lipp-*-sto-[0-9][0-9][0-9][0-9][0-9]-m02.ikea.com_WithNodeManager.sh )
var_script_m1=$( ls |grep -o start_lipp-*-sto-[0-9][0-9][0-9][0-9][0-9]-m01.ikea.com_WithNodeManager.sh )
./start_AdminServer_WithNodeManager.sh
sleep 60s
./$var_script_m1
sleep 60s
./$var_script_m2
sleep 90s
cd $var_sapp_domain
var_script_m3=$( ls |grep -o start_sapp-*-sto-[0-9][0-9][0-9][0-9][0-9]-m02.ikea.com_WithNodeManager.sh )
var_script_m4=$( ls |grep -o start_sapp-*-sto-[0-9][0-9][0-9][0-9][0-9]-m01.ikea.com_WithNodeManager.sh )
./start_AdminServer_WithNodeManager.sh
sleep 60s
./$var_script_m1
sleep 90s
./$var_script_m2