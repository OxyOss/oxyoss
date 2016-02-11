#!/usr/bin/python

import os
import sys
import argparse
import csv
#import indent
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring
import xml.etree.ElementTree as etree

from datetime import datetime

#import sys, os
#from xml.etree import ElementTree as ET

def get_args(args):
  parser = argparse.ArgumentParser(description = "Converts XML to CSV")
  parser.add_argument('-v','--verbose',action='store_true',dest='verbose',help='Increases messages being printed to stdout')
  parser.add_argument("inputfile", help="Please input the name of the XML file")
  parser.add_argument('-o','--outputfile',help='(optional) Output file name',nargs='?')
  args = parser.parse_args()
  ext = os.path.splitext(args.inputfile)[1].lower()
  if args.outputfile is None:
    if ext == ".csv":
      args.outputfile = os.path.splitext(args.inputfile)[0] + '.xml'

    elif ext == ".xml":
      args.outputfile = os.path.splitext(args.inputfile)[0] + '.csv'

  elif args.outputfile:
    ext2 = os.path.splitext(args.outputfile)[1].lower()
    sys.stdout.write(ext2 + "\n")
    valid_exts = [".csv", ".xml" ]
    if ext2 in valid_exts:
      outputfile = open(args.outputfile,'w')
    else:
      sys.stderr.write('Error: Invalid output file extension "%s"\n' % ext2)
      sys.exit(1)
  else:
      sys.stderr.write('ERROR: Invalid extension %s\n' % ext)
      sys.exit(1)
  return args


          
def main(argv):
  print "Hack to get information from squashscorerexport.xml file."
  args = get_args(argv[0:])
  if args is None:
    return 1
  ext = os.path.splitext(args.inputfile)[1].lower()
  if ext == ".csv":
    reader = read_csv(open(args.inputfile))
    generate_xml(reader, args.outputfile)

  if ext == ".xml":
    root = etree.parse(open(args.inputfile)).getroot()
    # generate_csv(root, args.outputfile)

  # Get the information from the XML document:
  #tree = getDataFromXML(args.inputfile)

  if args.verbose:
    print ('Verbose Selected')
  if args.verbose:
    print ('Convert to XML with set name')
  
  ss = SquashScorer(root)
  ss.calculateMatch()
  ss.generate_csv(args.outputfile)

  return 0 
  #dbname = '/home/rweatherburn/temp/squashscorer.db'

#def getDataFromXML( xmlFile='/home/rweatherburn/temp/squashscorerexport.xml'):
  #ifp = open(xmlFile, 'r')
  
  #tree = ET.parse(ifp)
  
  #ifp.close()
  
  #print tree
  #return tree

class SquashScorer:
  def __init__(self,xmlroot):
    self.root = xmlroot
    self.matchResults = []
    return 
  
  def main(self):
    print "calculateMatches"
    self.calculateMatch()
    print "generate CSV file"
    self.generate_csv()
    
  
  def calculateMatch(self):
    print "Testing: calculation of a match from the information"
    self.results = self.getResultInfo()
    matches = self.getMatches()
#    self.getPlayer( 1)
    return 0
  
  def getMatches(self):
    print "Testing: getMatches()"
    matches = self.root.findall("match")
    for match in matches:
	  matchResult = self.getMatchInfo(match)
	  if matchResult != None:
		self.matchResults.append(matchResult)
	  else:
	    print "Match was invalid"
      # for neighbor in match.iter('gamedetails'):
        # print "\t" + str(neighbor.attrib)
      # for child in match:
        # print child.attrib
        
    return matches

  def getMatchInfo(self, match):
    matchnum = match.attrib["oldmatchid"]
    ##print matchnum
    #getRallyInfo(match)
    if matchnum == "1":
      print "We have found match # " + str(matchnum)
    self.getMatchSpecifics(match)
    matchResult = self.getMatchData(match)
      
    #else:
      #pass
    
    return matchResult

  def getMatchSpecifics(self, match):
    playerA1 = match.find('playerA1id').text
    playerA2 = match.find('playerA2id').text
    playerB1 = match.find('playerB1id').text
    playerB2 = match.find('playerB2id').text
    pointspergame = match.find('pointspergame')
    gamedate = datetime.strptime(match.find('gamedate').text, '%Y-%m-%d %H:%M:%S') #match.find('gamedate').text
    
    print "Match played between " + self.getPlayer(playerA1) + " and " + self.getPlayer(playerB1)
    print "Match played on " + str(gamedate)
    return
    
  def getMatchData(self, match):
    gameNumber = 0
    currentServer = str(0)
    result = 0
    scores = {}
    playerA = match.find('playerA1id').text
    scoreA = 0
    gamesA = 0
    playerB = match.find('playerB1id').text
    scoreB = 0
    gamesB = 0
    matchResult = {}
    matchEndTime = None
    matchStartTime = None
    
    for rally in match.iter('gamedetails'):
      (matchid, gameno, serverid, receiverid, recipientid, resultid, resultval, 
       resultdate, side) = self.getRallyInfo(rally)
      if gameNumber < gameno and int(resultval) != 4:  # match still in progress
	gameNumber += 1
	rallyNumber = 0
      if serverid == currentServer:
#	print "we have a currentServer - " + self.getPlayer(currentServer)
	pass
      else:
#	print "currentServer = " + str(currentServer) + " (" + self.getPlayer(currentServer) + ")"
	currentServer = serverid
      if int(resultval) == 1: #Point won
	if resultid == 1:
#	  print "Point won (" + self.results[str(resultid)] + ")"
	  if serverid == playerA:
	    scoreA += 1
	  else:
	    scoreB += 1
	elif resultid == 2: #Hand Out
#	  print "Hand Out (" + self.results[str(resultid)] + ")"
	  if serverid == playerA:
	    scoreB += 1
	  else:
	    scoreA += 1
	else:
	  print "Wait - this is currently undefined! (" + self.results[str(resultid)]
	print "We have a result! " + str(resultid) + ' - ' + self.results[str(resultid)] + '(' + self.getPlayer(currentServer) + ')' + str(scoreA) + '/' + str(scoreB)
	
      elif resultid == 3:
	print self.results[str(resultid)]
	# Game won
	scores[str(gameno)+'A'] = str(scoreA) 
	scores[str(gameno)+'B'] = str(scoreB)
	scoreA = 0; scoreB = 0; currentServer = 0
	if serverid == playerA:
	  gamesA += 1
	else:
	  gamesB += 1
	#if gamesA > gamesB:
	  #print "Game scores: (" + str(scores) + ") - " + str(gamesA) + "/" + str(gamesB)
	#else:
	  #print "Game scores: (" + str(scores) + ") - " + str(gamesB) + "/" + str(gamesA)
      elif resultid == 4: # Match won
	matchResult = scores
	matchEndTime = resultdate
	counter = 1
	if gamesA > gamesB:
	  # playerA won
	  print "Match won by " + self.getPlayer(playerA)
	  sys.stdout.write(matchResult[str(counter)+'A'] + '/' + matchResult[str(counter)+'B']),
	  while counter < len(matchResult)/2: 
	    sys.stdout.write(", " + matchResult[str(counter+1)+'A'] + '/' + matchResult[str(counter+1)+'B']),
	    counter += 1

	  #matchResult = scores
	elif gamesB > gamesA:  
	  print "Match won by " + self.getPlayer(playerB)
#	  matchResult = scores.reversed
	  reverseTemp = matchResult[str(counter)+'B']
	  matchResult[str(counter)+'B'] = matchResult[str(counter)+'A']
	  matchResult[str(counter)+'A'] = reverseTemp
	  sys.stdout.write(matchResult[str(counter)+'A'] + '/' + matchResult[str(counter)+'B']),
	  while counter < len(matchResult)/2:
		reverseTemp = matchResult[str(counter+1)+'B']
		matchResult[str(counter+1)+'B'] = matchResult[str(counter+1)+'A']
		matchResult[str(counter+1)+'A'] = reverseTemp
		sys.stdout.write(", " + matchResult[str(counter+1)+'A'] + '/' + matchResult[str(counter+1)+'B']),
		counter += 1
	else:
		print "Invalid match!"
		return None
	print "\n====="
      else:
	if gameNumber == 1 and resultid == 6:
	  matchStartTime =  resultdate
	#print self.results[str(resultid)]
    if gamesA > gamesB:
      matchResult['winner'] = self.getPlayer(playerA)
      matchResult['loser'] = self.getPlayer(playerB)
      matchResult['starttime'] = matchStartTime
      matchResult['endtime'] = matchEndTime
    else:
      matchResult['winner'] = self.getPlayer(playerB)
      matchResult['loser'] = self.getPlayer(playerA)
      matchResult['starttime'] = matchStartTime
      matchResult['endtime'] = matchEndTime
      
    print "matchResult: " + str(matchResult)
	
    return matchResult#, winner
      

  def getRallyInfo(self, gamedetail):
    rallyid     = gamedetail.attrib['oldgamedetailsid']
    matchid   	= gamedetail.find('matchid').text
    gameno    	= gamedetail.find('gameno').text
    serverid  	= gamedetail.find('serverid').text
    receiverid	= gamedetail.find('receiverid').text
    recipientid	= gamedetail.find('recipientid').text
    resultid	= int(gamedetail.find('resultid').text)
    resultval	= int(gamedetail.find('resultval').text)
    resultdate	= datetime.strptime(gamedetail.find('resultdate').text, '%Y-%m-%d %H:%M:%S')
    side	= gamedetail.find('side').text
    
#    if rallyid == str(198):
#      print 'matchid: ' + matchid + '\tgameno: ' + gameno + '\tplayed at ' + datetime.strftime(resultdate,'%Y-%m-%d %H:%M:%S')
    return (matchid, gameno, serverid, receiverid, recipientid, resultid, resultval, 
		    resultdate, side)

  def getResultInfo(self):
	  resultArray = {}
	  print "getResultInfo()"
	  results = self.root.findall("results")
	  for result in results:
		  resultArray[result.find('resultid').text] = \
			  result.find('reason').text
	  return resultArray
	  
  def getPlayer(self, playerid):
	  players = self.root.findall('players')
	  playername = "To Be Found."
	  for player in players:
		  if playerid == player.attrib["oldplayerid"]:
			  playername = player.find("playername").text;
			  
	  return playername
	
  def getReasonDecisions(self, reasonid):
    reasonDecisions = self.root.findall('reasondecisions')
    reason = "To Be Found."
    for decision in reasonDecisions:
      if reasonid == decision.attrib["gamedetialsid"]:
	reasonText = decision.find("reason")
	
    return reason
  
  def generate_csv(self, outfile):
	import unicodedata
	print "In Generate CSV function"
	with open(outfile, 'w') as file_:
		writer = csv.writer(file_, delimiter=",",dialect=csv.excel)
      
		for M in self.matchResults: 
			print "Create the wString array"
			print str(M)
			print '----'
			wString = []
			date=datetime.strftime(M['starttime'],'%d-%m-%Y')
			event="TBC"
			venue="TBC"
			round="TBC"
			winner=M['winner'].encode('ascii', 'ignore')
			result="def"
			loser=M['loser'].encode('ascii', 'ignore')
			ranking="TBC"
			position="TBC"
			Qual="Not rank"
			if M.has_key('1A'):
				G1A=M['1A']
				G1B=M['1B']
			else:
				G1A=""
				G1B=""
			if M.has_key('2A'):
				G2A=M['2A']
				G2B=M['2B']
			else:
				G2A=""
				G2B=""
			if M.has_key('3A'):
				G3A=M['3A']
				G3B=M['3B']
			else:
				G3A=""
				G3B=""
			if M.has_key('4A'):
				G4A=M['4A']
				G4B=M['4B']
			else:
				G4A=""
				G4B=""
			if M.has_key('5A'):
				G5A=M['5A']
				G5B=M['5B']
			else:
				G5A=""
				G5B=""
			starttime=datetime.strftime(M['starttime'],'%H:%M:%S')
			if M['endtime'] == None:
				endtime=datetime.strftime(M['starttime'],'%H:%M:%S')
			else:
				endtime=datetime.strftime(M['endtime'],'%H:%M:%S')
			wString.append(date)
			wString.append(event)
			wString.append(venue)
			wString.append(round)
			wString.append(winner)
			wString.append(ranking)
			wString.append(result)
			wString.append(loser)
			wString.append(ranking)
			wString.append(position)
			wString.append(Qual)
			wString.append(G1A)
			wString.append(G1B)
			wString.append(G2A)
			wString.append(G2B)
			wString.append(G3A)
			wString.append(G3B)
			wString.append(G4A)
			wString.append(G4B)
			wString.append(G5A)
			wString.append(G5B)
			wString.append(starttime)
			wString.append(endtime)

			print "print the wString array"
			print str(M)
			print str(wString)
			writer.writerow(wString)
	
	return
    
	
def generate_csv(root, outfile):

    with open(outfile, 'w') as file_:

        writer = csv.writer(file_, delimiter="\t")
	# for a in zip(root.findall("players")):
		# sys.stdout.write(str([x.text for x in a]) + '\n')
    for a in zip(root.findall("drillholes/hole/collar"),
                 root.findall("drillholes/hole/toe"),
                 root.findall("drillholes/hole/cost")):
        writer.writerow([x.text for x in a])
		
def generate_xml(reader,outfile):
    root = Element('Solution')
    root.set('version','1.0')
    tree = ElementTree(root)        
    head = SubElement(root, 'DrillHoles')
    description = SubElement(head,'description')
    current_group = None
    i = 0
    for row in reader:
        if i > 0:
            x1,y1,z1,x2,y2,z2,cost = row
            if current_group is None or i != current_group.text:
                current_group = SubElement(description, 'hole',{'hole_id':"%s"%i})

                collar = SubElement (current_group, 'collar',{'':', '.join((x1,y1,z1))}),
                toe = SubElement (current_group, 'toe',{'':', '.join((x2,y2,z2))})
                cost = SubElement(current_group, 'cost',{'':cost})
        i+=1
    head.set('total_holes', '%s'%i)
    #indent.indent(root)
    tree.write(outfile)


if (__name__ == "__main__"):
    sys.exit(main(sys.argv))
