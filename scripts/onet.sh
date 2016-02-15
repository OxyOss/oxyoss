#!/bin/bash -x 

if [ $# == 1 ] ## We have an argument, which should be a host name
then
    ssh -p 20 -Y -t russell@westley.oxyoss.net ssh -Y $1
else
    ssh -p 20 -Y russell@westley.oxyoss.net
   
fi


