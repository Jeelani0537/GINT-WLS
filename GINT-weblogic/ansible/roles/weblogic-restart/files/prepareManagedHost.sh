server=$1
adminhost=$2

id=${server: -1}
echo ${adminhost//a01/m0${id}} | sed 's/ikeadta/ikeadt/g' | sed 's/ikeaa/ikea/g'
