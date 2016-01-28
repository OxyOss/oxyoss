# Simple encryption script.
openssl des3 -salt -in $1 -out $1.des3
