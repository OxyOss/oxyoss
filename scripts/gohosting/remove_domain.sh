# Usage of sed.  
# This will remove any lines which have the first argument plus the next line.  
# It takes a backup of the original file, but still should be used with caution.
sed -i.bak "/$1/,+1 d" /home/actcsvr06dns/slaves/dnslist.txt
