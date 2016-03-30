#!/bin/bash

if [ -z "$1" ]; then
  echo "no argument"
  exit 1
fi

newcerts=newcerts
cert="$1"
file=""
mess=""
for i in "$cert" "$cert.cert.pem" "$newcerts/$cert" "$newcerts/$cert.cert.pem"; do
  if [ ! -e "$i" ]; then
    mess="$mess
no file "$i" found"
    continue
  fi
  if [ ! -s "$i" ]; then
    mess="$mess
file "$i" empty"
    continue
  fi
  file="$i"
  break
done

if [ -z "$file" ]; then
  echo "$mess"
  exit 2
fi

echo "file \"$file\" found"

certfile=${file##*/}
certdir=${file%/*}

openssl x509 -hash -noout -in "$file"

