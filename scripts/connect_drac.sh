#!/usr/bin/env bash
# Script to connect to a borderless set geometry screen, with the option of selecting the Windows PC/server to connect to.
# Note: a hostname is required

usage() { echo "Usage: $0 [-h <hostname>] " 1>&2; 
        echo "where viewer file = viewer_<hostname>.jnlp"
        exit 1; }

hostname="NONE"

while getopts ":u:p:h:d:ar" o; do
    case "${o}" in
        h)
            hostname=$OPTARG
            ;;
        *)
            usage
            ;;
    esac
done

shift $((OPTIND-1))
if [[ $# == 1 ]];
then
    hostname=$1
fi

if [ $hostname == "NONE" ]
then
    usage
else
    cd ${HOME}/drac
    dracViewer=viewer_${hostname}.jnlp
    if [ -f $dracViewer ]; then 
        nohup javaws $dracViewer &
    else
        echo "$dracViewer file is missing."
        usage
    fi
fi
