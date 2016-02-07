import sqlite3

class Database(object):

  def __init__(self, p):
    self.conn = sqlite3.connect(p)
    self.serializers = {}
    
  def reset(self):
    cursor = self.conn.cursor()
    cursor.execute('DROP TABLE matches')
    cursor.execute('DROP TABLE players')
    cursor.execute('DROP TABLE points')
    self.conn.commit()
    cursor.execute('CREATE TABLE matches ( matchid INT, playerA1id INT, playerA2id INT, playerB1id INT, playerB2id INT, pointspergame INT, gamespermatch INT, gamedate DATE, warmupstart DATETIME, warmupend DATETIME, division TEXT, round TEXT, court TEXT, refereeid INT, markerid INT, logouri1 TEXT, logouri2 TEXT, eventuri TEXT , eventlocation TEXT)')
    cursor.execute('CREATE TABLE players (playerid INT, playername TEXT)')
    cursor.execute('CREATE TABLE gamedetails (gamedetailsid INT, matchid INT, gameno INT, serverid INT, receiverid INT, recipientid INT, resultid INT, resultval INT, resultdate DATETIME, side TEXT)')
    self.conn.commit()
    cursor.close()

  def insertMatch(self, information):
    
    cursor = self.conn.cursor()
    cursor.execute('INSERT INTO matches VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', 
                   (information.matchid,
                    information.playerA1id,
                    information.playerA2id,
                    information.playerB1id,
                    information.playerB2id,
                    information.pointspergame,
                    information.gamespermatch,
                    information.gamedate,
                    information.warmupstart,
                    information.warmupend,
                    information.division,
                    information.round,
                    information.court,
                    information.refereeid,
                    information.markerid,
                    information.logouri1,
                    information.logouri2,
                    information.eventuri,
                    information.eventlocation
                    ))
    self.conn.commit()
    cursor.close()
    
  def insertPlayer(self, information):
    
    cursor = self.conn.cursor()
    cursor.execute('INSERT INTO players VALUES (?)', 
                   (information.playerid,
                    information.playername))
    self.conn.commit()
    cursor.close()
    
  def insertPoint(self, information):
    
    cursor = self.conn.cursor()
    cursor.execute('INSERT INTO gamedetails VALUES (?,?,?,?,?,?,?,?,?)', 
                   (information.gamedetailsid,
                    information.matchid, 
                    information.gameno,
                    information.serverid,
                    information.receiverid,
                    information.recipientid,
                    information.resultid,
                    information.resultval,
                    inforamtion.resultdate,
                    information.side
                    ))
