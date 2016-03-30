#!/bin/bash

#  ssltestnet Kim Holburn NLA 2001-06-08
#


version () {
  version=" @(#)ssltestnet	1.0 2004-Sep-28 "
  if [ `echo "$version"|grep -c '%'` -gt 0 ]; then
    version=" working version "
  fi
  echo "$version"
}

myfail () {
  if [ -n "$*" ]; then
    echo
    echo "Error:"
    for mess in "$@"; do
      echo $mess
    done
    echo 
  fi
  echo "ssltestnet to test an ssl connection "
  version
  echo "usage:"
  echo "ssltestnet [-v] (host:port)|(-h host -p port)  "
  echo 
  echo "  [-v (verbose)]"
  exit 1
}

#host="localhost"
#port="pop3s"
host=""
port=""
caopts=""
verbose=0
starttls=""
while [ -n "$1" ]; do
  case "$1" in
  -h) shift
      host=$1
      if [ -z "$host" ]; then
        myfail "no host following -h option"
      fi
      shift
      ;;
  -p) shift
      port=$1
      if [ -z "$port" ]; then
        myfail "no port following -p option"
      fi
      shift
      ;;
  -c) shift
#-CAfile filename
      cafile="$1"
      if [ -z "$cafile" ]; then
        myfail "no cafile following -c option"
      fi
      if [ ! -r "$cafile" ]; then
        myfail "can't read cafile \"$cafile\" "
      fi
      caopts="-verify 2 -CAfile \"$cafile\""
      shift
      ;;
  -s) starttls="-starttls smtp"; shift;;
  -v) verbose=$(( $verbose + 1)); shift;;
  --help) myfail ;;
  -*) myfail "unknown option";;
  *) break;;
  esac
done

if [ "$#" -gt 1 ]; then
  myfail "too many arguments"
fi

if [ -n "$1" ]; then
  case "$1" in
  *:*) hostp="$1";;
  *) myfail "I don't understand argument ($1)";;
  esac
else
  if [ -z "$host" ]; then
    myfail "no host specified"
  fi
  if [ -z "$port" ]; then
    myfail "no port specified"
  fi
  hostp="$host:$port"
fi
if [ -z "$hostp" ]; then
  myfail "no host and port specified"
fi
echo openssl s_client $caopts $starttls -connect "$hostp" -showcerts 
openssl s_client $caopts $starttls -connect "$hostp" -showcerts 
