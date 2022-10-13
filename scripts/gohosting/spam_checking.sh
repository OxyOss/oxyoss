#!/usr/bin/env bash

function pause(){
  # pause without echoing to the terminal, expect 1 character
  read -s -n 1 -p "Press a key to resume..."
  echo ""
}

echo "Checking the number of mails in the exim queue"
pause
# display the queue, pipe through to a summary executable
exim -bp | exiqsumm
pause

echo "get sorted list of mail senders"
pause
exim -bpr | grep "<" | awk {'print $4'} | cut -d "<" -f 2 | cut -d ">" -f 1 | sort -n | uniq -c | sort -n
pause

echo "Get the duplicated subjects from the Exim main log"
pause
awk -F"T=\"" '/<=/ {print $2}' /var/log/exim_mainlog | cut -d\" -f1 | sort | uniq -c | sort -n
pause

echo "Get the user who sent the mail with a specific subject
read -p "enter the subject of the spam: " subject  
read -p subject  "enter the subject of the spam: " 
grep "$subject" /var/log/exim_mainlog | awk '{print $5}' | sort | uniq -c | sort -n
pause

echo 'Get the IP address(es) of the spam sending'
read -p "Enter the sender email address: " sender 
grep "<= $sender" /var/log/exim_mainlog | grep "$subject" | grep -o "\[[0-9.]*\]" | sort -n | uniq -c | sort -n
pause

echo "Probably should block those IPs in the firewall.  Try:"
echo "csf -d IP"
pause

echo "Checking the current queue.  This will allow you to see if it is a script or a login which is causing the SPAM to be sent"
exim -bp | less

read -p "Enter in a message id to view the contents: " msgid

exim -Mvh $msgid

echo "If this looks fine, it is probably a script which is causing the issues."
pause

grep cwd /var/log/exim_mainlog | grep -v /var/spool | awk -F" cwd" '{print $2}' | awk '{print $1}' | sort | uniq -c | sort -n | less

echo "You can check out the script using the access logs for apache"
echo "grep "mailer.php" /home/<user>/access-logs/<domain>* | awk '{print $1}' | sort -n | uniq -c | sort -n

pause


echo "Get the list of messages which have an auth_id in the headers"
read -p "Enter sender name: " auth_sender
find /var/spool/exim/input -name "*-H -exec grep -q "\-auth_id" {} \; -print | 
find /var/spool/exim/input -name "*-H" -exec grep -q "\-auth_id $auth_sender" {} \; -print | awk -F/ '{print $7}' | cut -d\- -f1-3
# add this to remove | xargs exim -Mvh 

#alternatively, you can remove all the deferred mail messages and undeliverables
# find /var/spool/exim/input -name "*-H" -exec grep -q "Subject: Mail delivery failed: returning message to sender" {} \; -print | awk -F/ '{print $7}' | cut -d\- -f1-3 | xargs exim -Mrm
