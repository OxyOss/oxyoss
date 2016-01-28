#!/bin/bash

# make svn backup
# will make a backup date stamped.
# usage:
# make_backup.sh [<dir>]

SRCDIR=/export/svn
#DSTDIR=/export/data/temp/svn_backup
DATE=$(date '+%y-%m-%d_%H.%M.%S')
if [ -n "$1" ]; then
  DSTDIR="${1//%d/$DATE}"
else
#  DSTDIR="/media/usb/svn_backup_$DATE"
  DSTDIR="/export/backup/svn_backup_$DATE"
fi
if [ ! -d "$DSTDIR" ]; then
  mkdir "$DSTDIR"
  if [ ! -d "$DSTDIR" ]; then
    echo "Error: Failed to create destination directory"
    exit 2
  fi
else
  echo -n "Directory ($DSTDIR) exists, delete old backup (y/N)?: "
  read answer
  case "$answer" in
  y*|Y*);;
  *) echo "Error: User stopped script"
    exit 3;;
  esac
  echo "deleting directory ($DSTDIR) ..."
  /bin/rm -fr $DSTDIR/*
fi

echo "Start backup destination=($DSTDIR)"
#exit 3
cd "$SRCDIR"

for i in *; do
  if [ -f "$i" ]; then
    cp $SRCDIR/${i} $DSTDIR/${i}
    continue
  fi
  if [ "${i%_repos}" != "$i" ]; then 
    svnadmin hotcopy $SRCDIR/${i} $DSTDIR/${i}
    continue
  fi
  if [ "${i%_test}" != "$i" ]; then 
    svnadmin hotcopy $SRCDIR/${i} $DSTDIR/${i}
    continue
  fi
done

tar -czf "$DSTDIR.tar.gz" "$DSTDIR"
