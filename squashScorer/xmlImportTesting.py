#!/usr/bin/python

import os
import sys
import argparse
import csv
#import indent
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring
import xml.etree.ElementTree as etree

import sys, os
from xml.etree import ElementTree as ET

from Database import Database

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
		
	calculateMatch(root)

	return 0 
	#dbname = '/home/rweatherburn/temp/squashscorer.db'

def getDataFromXML( xmlFile='/home/rweatherburn/temp/squashscorerexport.xml'):
  ifp = open(xmlFile, 'r')
  
  tree = ET.parse(ifp)
  
  ifp.close()
  
  print tree
  return tree

def calculateMatch(root):
	print "Testing: calculation of a match from the information"
	results = getResultInfo(root)
	getMatches(root)
	get_player(root, 1)
	return 0
	
def getMatches(root):
	print "Testing: getMatches()"
	matches = root.findall("match")
	for match in matches:
		getMatchInfo(match)
		# for neighbor in match.iter('gamedetails'):
			# print "\t" + str(neighbor.attrib)
		# for child in match:
			# print child.attrib
			
# for country in root.findall('country'):
# ...   rank = country.find('rank').text
# ...   name = country.get('name')
#...   print name, rank

	return matches

def getMatchInfo(match):
	matchnum = match.attrib["oldmatchid"]
	##print matchnum
	#getRallyInfo(match)
	if matchnum == "3":
		print "We have found match # 3."
		print matchnum
		for rally in match.iter('gamedetails'):
			(matchid, gameno, serverid, receiverid, recipientid, resultid, resultval, 
			resultdate, side) = getRallyInfo(rally)
			
	else:
		pass
		
	return 

def getMatchSpecifics(match):
	playerA1 = match.find('playerA1id')
	playerA2 = match.find('playerA2id')
	playerB1 = match.find('playerB1id')
	playerB2 = match.find('playerB2id')
	pointspergame = match.find('pointspergame')
	gamedate = match.find('gamedate')
	
	
	
def getRallyInfo(gamedetail):
	matchid   	= gamedetail.find('matchid').text
	gameno    	= gamedetail.find('gameno').text
	serverid  	= gamedetail.find('serverid').text
	receiverid	= gamedetail.find('receiverid').text
	recipientid	= gamedetail.find('recipientid').text
	resultid	= gamedetail.find('resultid').text
	resultval	= gamedetail.find('resultval').text
	resultdate	= gamedetail.find('resultdate').text
	side		= gamedetail.find('side').text
	
	print 'matchid: ' + matchid + '\tgameno: ' + gameno
	return (matchid, gameno, serverid, receiverid, recipientid, resultid, resultval, 
			resultdate, side)

def getResultInfo(root):
	resultArray = {}
	print "getResultInfo()"
	results = root.findall("results")
	for result in results:
		resultArray[result.find('resultid').text] = \
			result.find('reason').text
	return resultArray
	
def getPlayer(root, playerid):
	players = root.findall('players')
	playername = "To Be Found."
	for player in players:
		if playerid == player.attrib["oldplayerid"]:
			playername = player.find("playername")
			
	return playername
	
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
