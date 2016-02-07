#!/usr/bin/python

import sys, os
from xml.etree import ElementTree as ET

from Database import Database
          
def main():
  print "Hack to get information from squashscorerexport.xml file."
  
  dbname = '/home/rweatherburn/temp/squashscorer.db'
  
  # Get the information from the XML document:
  getDataFromXML()
  
def getDataFromXML( xmlFile='/home/rweatherburn/temp/squashscorerexport.xml'):
  ifp = open(xmlFile, 'r')
  
  tree = ET.parse(ifp)
  
  ifp.close()
  
  print tree
#  while line:
#      field = line.split(',')
#      cursor.execute('INSERT INTO ' + tableName + ' VALUES (?,?,?,?,?,?,?,?)', (field[0], field[1], field[2], field[3], field[4], field[5], field[6], field[7].strip()))
#      self.conn.commit()
#      line = ifp.readline()
#      


getDataFromXML()
  