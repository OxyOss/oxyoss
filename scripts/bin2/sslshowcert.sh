#!/bin/sh

if [ -z "$1" ]; then
  echo "no argument"
  exit 1
fi

cert="$1"

if [ ! -r "$cert" ]; then
  echo -c "no file \"$cert\" trying "
  cert="req/$1.cert.pem"
  echo " trying \"$cert\" "
fi
if [ ! -r "$cert" ]; then
  echo "no file \"$cert\" giving up "
  exit
fi

openssl x509 -in "$cert" -text

