#pass lip/sapp as input

hname=`hostname -f`
stack=$1

storename=`echo $hname | cut -c 4-5`
storenumber=`echo $hname | cut -c 6-8`

if [[ $hname == *"4020"* ]]
then
  echo "$stack-$storename-sto-00$storenumber-m01.ikea.com"
else
  echo "$stack-$storename-sto-00$storenumber-m02.ikea.com"
fi
