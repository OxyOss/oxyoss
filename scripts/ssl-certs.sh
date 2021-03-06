#!/bin/bash

DB="-d sql:$HOME/.pki/nssdb"

case "$1" in

    list)
        certutil $DB -L
        ;; details)
        certutil $DB -L -n "$2"
        ;; add-ca)
        certutil $DB -A -t "$2" -n "$3" -i "$4"
        ;; add)
        pk12util $DB -i "$2"
        ;; del)
        certutil $DB -D -n "$2"
        ;;
        echo "Usage [list|details|add-ca|add|del]"
        echo " \"details\" requires <nickname>"
        echo " \"add-ca\" requires <trustargs> <nickname> <certificate filename>"
        echo " \"add\" requires <filename>"
        echo " \"del\" requires <nickname>"
        exit 1
        ;;
esac ~

