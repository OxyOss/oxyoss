
# User specific aliases and functions
alias actcsvr08='ssh root@actcsvr08.gohosting.com.au'
alias actcsvr07='ssh root@actcsvr07.gohosting.com.au'
alias actcsvr06='ssh root@actcsvr06.gohosting.com.au'
alias actcsvr04='ssh root@actcsvr04.gohosting.com.au'
alias actcsvr03='ssh root@actcsvr03.gohosting.com.au'
alias actcsvr02='ssh root@actcsvr02.gohosting.com.au'
alias actcsvr01='ssh root@actcsvr01.gohosting.com.au'
alias nflame='ssh root@nflame.gohosting.com.au'
alias acta01='ssh 203.83.219.9'
alias actcsvr09='ssh root@110.34.54.178'
alias actcsvr10='ssh root@110.34.54.186'
alias actcsvr11='ssh root@actcsvr11.gohosting.com.au'
alias actcsvr12='ssh root@actcsvr12.gohosting.com.au'
alias actcsvr13='ssh root@actcsvr13.gohosting.com.au'
alias actcsvr14='ssh root@actcsvr14.gohosting.com.au'
alias actcsvr15='ssh root@actcsvr15.gohosting.com.au'

alias dig1='dig @ns1.gohosting.com.au'
alias dig2='dig @ns2.gohosting.com.au'
alias dig3='dig @ns3.gohosting.com.au'
alias dig8='dig @8.8.8.8'
alias digq='dig @ns1.quantumcore.com.au'
alias dig28='dig @203.83.219.28'
alias dig27='dig @203.83.219.27'

alias actcsvr16='ssh root@actcsvr16.gohosting.com.au'
alias acta01='ssh root@103.11.147.57'
alias configmgr='ssh russell.weatherburn@103.11.147.127'
alias actcbsvr01='ssh actcbsvr01.gohosting.com.au'
alias actcsvr17='ssh root@actcsvr17.gohosting.com.au'
alias actcsvr18='ssh root@actcsvr18.gohosting.com.au'
#alias russtest='ssh root@103.11.147.122'

ns() {
   # get the name servers from a whois command
   whois "$1" | grep -E 'Name Server:|Registrar |Domain Status:|^Status:|^Status Reason:|^Priority|^Eligibility|^Registrant:|^Registrant ID:|^RELEASING|^Priority'
}

getInfo() {
   # Get the data for a migration
   echo "Using google for dig commands"
   ns $1
   dig8 mx $1 | grep -Ea2 'ANSWER S|ADDITIONAL S'
   dig8 $1 | grep -Ea2 'ANSWER S|ADDITIONAL S'
   dig8 txt $1 | grep -Ea2 'ANSWER S|ADDITIONAL S'
   dig8 soa $1 | grep -Ea2 'ANSWER S|ADDITIONAL S'
   dig8 www.${1} | grep -Ea2 'ANSWER_S|ADDITIONAL_S'
}
getQCInfo() {
   # Get the data for a migration
   ns $1
   digq mx $1 | grep -Ea2 'ANSWER S|ADDITIONAL S'
   digq $1 | grep -Ea2 'ANSWER S|ADDITIONAL S'
   digq txt $1 | grep -Ea2 'ANSWER S|ADDITIONAL S'
   digq soa $1 | grep -Ea2 'ANSWER S|ADDITIONAL S'
   digq www.${1} | grep -Ea2 'ANSWER_S|ADDITIONAL_S'
}

get1nfo() {
   # Get the data for a migration
   echo "Using ns1.gohosting for dig commands"
   ns $1
   dig1 mx $1 | grep -Ea2 'ANSWER S|ADDITIONAL S'
   dig1 $1 | grep -Ea2 'ANSWER S|ADDITIONAL S'
   dig1 txt $1 | grep -Ea2 'ANSWER S|ADDITIONAL S'
   dig1 soa $1 | grep -Ea2 'ANSWER S|ADDITIONAL S'
   dig1 www.${1} | grep -Ea2 'ANSWER_S|ADDITIONAL_S'
}
