#! /usr/bin/env bash 
#set -x


CURRDIR=$(dirname $0)

while getopts ":hf:d" opt; do
  case ${opt} in 
    h ) # process option h
       echo "Usage: $0 [-h] [-f filename] [-d]"
        exit 0
       ;;
    f ) # process option f
       FNAMEOPT=$OPTARG
       ;;
    d ) # process option d
       FULL="True"
       ;;
    /? ) echo "Usage: $0 [-h] [-f filename] [-d]"
       ;;
  esac
done


if [ -z "$FNAMEOPT" ]; then
  FNAME=${CURRDIR}/doms.txt
  FIELD=12
else
  FNAME=$FNAMEOPT
  FIELD=1
fi
echo "Using $FNAME" 
#echo "Outputting to $FNAME" #temporarily, we probs don't need this in the future

#read -dp "Paste in domains to check from WHMCS todo list" doms
#read -dp doms "Paste in domains to check from WHMCS todo list" <<_EOF
#echo "Paste in domains to check from WHMCS todo list:"
#doms=$(sed '/^$/q')
#read -rep "stuff here:" doms
#IFS= read -d '' -n 1 doms
#while IFS= read -d '' -n 1 -t 2 c
#do 
#	doms+=$(echo "")
#	doms+=$c
#done


#echo $doms | tee $FNAME

for H in $(cat $FNAME | awk '{print $fieldvar}' fieldvar=$FIELD | sort | uniq) 
	do echo $H 
	if [ -z "$FULL" ]; then
		whois $H | grep Status: | grep -Ev 'server|client' 
	else
		whois $H | grep Status: 
	fi
	echo "" 
done

