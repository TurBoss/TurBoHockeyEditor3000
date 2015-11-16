#Boa:Frame:Frame1

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import binascii
from binascii import hexlify

import wx

#-------------------------------------------------------------------------------

CHARS = {
        'A' : '\x80',
        'B' : '\x81',
        'C' : '\x82',
        'D' : '\x83',
        'E' : '\x84',
        'F' : '\x85',
        'G' : '\x86',
        'H' : '\x87',
        'I' : '\x88',
        'J' : '\x89',
        'K' : '\x8A',
        'L' : '\x8B',
        'M' : '\x8C',
        'N' : '\x8D',
        'O' : '\x8E',
        'P' : '\x8F',
        'Q' : '\x90',
        'R' : '\x91',
        'S' : '\x92',
        'T' : '\x93',
        'U' : '\x94',
        'V' : '\x95',
        'W' : '\x96',
        'X' : '\x97',
        'Y' : '\x98',
        'Z' : '\x99',
        
        'a' : '\x9A',
        'b' : '\x9B',
        'c' : '\x9C',
        'd' : '\x9D',
        'e' : '\x9E',
        'f' : '\x9F',
        'g' : '\xA0',
        'h' : '\xA1',
        'i' : '\xA2',
        'j' : '\xA3',
        'k' : '\xA4',
        'l' : '\xA5',
        'm' : '\xA6',
        'n' : '\xA7',
        'o' : '\xA8',
        'p' : '\xA9',
        'q' : '\xAA',
        'r' : '\xAB',
        's' : '\xAC',
        't' : '\xAD',
        'u' : '\xAE',
        'v' : '\xAF',
        'w' : '\xB0',
        'x' : '\xB1',
        'y' : '\xB2',
        'z' : '\xB3',

        '0' : '\xC1',
        '1' : '\xC2',
        '2' : '\xC3',
        '3' : '\xC4',
        '4' : '\xC5',
        '5' : '\xC6',
        '6' : '\xC7',
        '7' : '\xC8',
        '8' : '\xC9',
        '9' : '\xCA',
        
        ' ' : '\xFF',
}

HEX = {v:k for k,v in CHARS.items()}

SHOOTS_CHAR = {
        '0' : '\x00',
        '1' : '\x01',
        '2' : '\x02',
        '3' : '\x03',
        '4' : '\x04',
        '5' : '\x05',
        '6' : '\x06',
        '7' : '\x07',
        '8' : '\x08',
        '9' : '\x09',
        '10' : '\x0A',
        '11' : '\x0B',
        '12' : '\x0C',
        '13' : '\x0D',
        '14' : '\x0E',
        '15' : '\x0F',
        '16' : '\x16',
        '17' : '\xFF',    
}

SHOOTS_HEX = {v:k for k,v in SHOOTS_CHAR.items()}

SHOOT_NAMES = (
        "DEFORMA LA PELOTA, DIRECTA",
        "TIRA A PUERTA Y SE PARA, AL TOCAR PUEDE IR HACIA TU PROPIA PORTERIA",
        "TIRA RECTO HASTA QUE SE DESVIA LA ULTIMA HORA",
        "VA LENTA Y SE HACE PEQUENYA",
        "REBOTA CON LA PARED PARA SALIR DIRECTA A GOL",
        "PASA DE LARGO DE LA PORTERIA Y DA VUELTAS HASTA IR DIRECTA A PUERTA",
        "SE ELEVA AL FONDO DEL CAMPO VUELVE A LINEA DE GOL Y AL CAER SUELE ENTRAR",
        "HAZE ZIG-ZAG MIENTRAS VA DIRECTO A PORTERIA",
        "SE ELEVA AL CIELO EN BOCA DE GOL Y AL CAER SUELE ENTRAR",
        "ZIG-ZAG MIENTRAS VA DIRECTO A PORTERIA (A LO PLATANO, TEAM 1) CON EFECTO ESTIRADO DE PELOTA (00)",
        "DIRECTO A PORTERIA Y A MITAD DESPARECE, APARECE MAS ADELANTE PARA IR DIRECTA A GOL",
        "TIRO DEL OSITO, PERO PARECE QUE FALLA EL SPRITE (SOLO CHICAS?)",
        "TRAS PEQUENYA 'S' DIRECTA A GOL"
        "REBOTA DE LADO A LADO HASTA SALIR DIRECTA A GOL",
        "TIRO DE REMOLINO MORTAL, DIRECTA A GOL",
        "DIRECTA, LA FICHA SE PONE NARANJA",
        "TIRO ESPECIAL, SE SUSPENDE EL PARTIDO XD",
        "TIRO FAKE, LA POLLA XD",
        "SIN ESPECIAL"
)

#-------------------------------------------------------------------------------
# File

def loadfile(file,action):
    if action == "read":
        rom = open(file,'rb')
    elif action == "write":
        rom = open(file,'r+b')
    
    return rom

def closefile(rom):
    rom.close()
    
#-------------------------------------------------------------------------------
# Time

def loadtime(rom):
    rom.seek(0x01D6C9)
    mins = rom.read(1)
    mins =  ord(mins)
    
    rom.seek(0x01D6D3)
    secs = rom.read(1)
    secs = ord(secs)
    
    return mins , secs

def savetime(rom, mins, secs):
    
    
    rom.seek(0x01D6C9)
    rom.write(convertint(int(mins)))
    
    rom.seek(0x01D6D3)
    rom.write(convertint(int(secs)))
    
#-------------------------------------------------------------------------------
# Charge

def loadcharge(rom):
    rom.seek(0x0190A6)
    charge = rom.read(1)
    charge = ord(charge)
    
    return charge

def savecharge(rom, charge):
    
    rom.seek(0x190A6)
    rom.write(convertint(int(charge)))

#-------------------------------------------------------------------------------
# Music

def loadmusic(rom):

    
    musicHex = ["\x0C", "\x0D", "\x0E", "\x0F", "\x10", "\x11"]
    music = [0,0,0,0,0]
    rom.seek(0x01D8DC)
    musics = rom.read(5)
    
    i = 0
    for data in musics:
        if data == musicHex[0]:
            music[i] = 0
        elif data == musicHex[1]:
            music[i] = 1
        elif data == musicHex[2]:
            music[i] = 2
        elif data == musicHex[3]:
            music[i] = 3
        elif data == musicHex[4]:
            music[i] = 4
        elif data == musicHex[5]:
            music[i] = 5
        i += 1
        
    return music

def savemusic(rom, music):
    
    musicHex = ["\x00", "\x00", "\x00", "\x00", "\x00"]
    
    i = 0
    for data in music:
        if data == 0:
            musicHex[i] = "\x0C"
        elif data == 1:
            musicHex[i] = "\x0D"
        elif data == 2:
            musicHex[i] = "\x0E"
        elif data == 3:
            musicHex[i] = "\x0F"
        elif data == 4:
            musicHex[i] = "\x10"
        elif data == 5:
            musicHex[i] = "\x11"
        
        i += 1
    
    rom.seek(0x1D8DC)
    for i in range(4):
        rom.write(musicHex[i])
    
#-------------------------------------------------------------------------------
# No penalty

def loadnopenalty(rom):
    penalty = "\x18"
    
    enabled = False
    
    rom.seek(0x01B637)
    data = rom.read(1)
    
    if data == penalty:
        enable = False
    else:
        enable = True
    
    return enable

def savenopenalty(rom, enable):
    
    rom.seek(0x01B637)
    
    if enable:
        rom.write("\x17")
    else:
        rom.write("\x18")

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Teams

class Team(object):
    
    def __init__(self, teamNameOffset, teamStatsOffset, playerNameOffset, playerShootOffset):
        self.teamNameOffset = teamNameOffset
        self.playerNameOffset = playerNameOffset
        self.playerShootOffset = playerShootOffset
        self.teamStatsOffset = teamStatsOffset
    
    def loadteam(self, rom):
        
        # Team name
        
        rom.seek(self.teamNameOffset)
        teamname = rom.read(8)
        
        # Players name
        
        playersname = ['' for i in range(5)]
        
        rom.seek( self.playerNameOffset[0] )
        playersname[0] = rom.read(4)
        
        rom.seek( self.playerNameOffset[1] )
        playersname[1] = rom.read(4)
        
        rom.seek( self.playerNameOffset[2] )
        playersname[2] = rom.read(4)
        
        rom.seek( self.playerNameOffset[3] )
        playersname[3] = rom.read(4)
        
        rom.seek( self.playerNameOffset[4] )
        playersname[4] = rom.read(4)
        
        return teamname, playersname

    def saveteam(self, rom, teamname, players):

        # Team Name
        
        rom.seek(self.teamNameOffset)
        rom.write(teamname)
        
        # Players Name
        
        rom.seek( self.playerNameOffset[0] )
        rom.write(players[0])
        
        rom.seek( self.playerNameOffset[1] )
        rom.write(players[1])
        
        rom.seek( self.playerNameOffset[2] )
        rom.write(players[2])
        
        rom.seek( self.playerNameOffset[3] )
        rom.write(players[3])
        
        rom.seek( self.playerNameOffset[4] )
        rom.write(players[4])

    def readTeamStats(self, rom):
        
        rom.seek(self.teamStatsOffset)
        teamStats = rom.read(2)
        
        return teamStats
    
    def writeTeamStats(self, rom, attack, defense):
        
        attackHex = convertint(attack)
        defenseHex = convertint(defense)
        
        stats = attackHex + defenseHex
        
        
        rom.seek(self.teamStatsOffset)
        rom.write(stats)
        
    def sShootRead(self, rom):
        
        playerShoot = ['' for i in range(5)]
        playerShootHex = ['' for i in range(5)]
        
        rom.seek( self.playerShootOffset[0] )
        playerShootHex[0] = rom.read(1)
        
        rom.seek( self.playerShootOffset[1] )
        playerShootHex[1] = rom.read(1)
        
        rom.seek( self.playerShootOffset[2] )
        playerShootHex[2] = rom.read(1)
        
        rom.seek( self.playerShootOffset[3] )
        playerShootHex[3] = rom.read(1)
        
        rom.seek( self.playerShootOffset[4] )
        playerShootHex[4] = rom.read(1)
        
        i = 0
        for hex in playerShootHex:
            
            pattern = re.compile(r'(' + '|'.join(SHOOTS_HEX.keys()) + r')')
            result = pattern.sub(lambda x: SHOOTS_HEX[x.group()], hex)
            
            playerShoot[i] = result
            i+=1
        
        return playerShoot

    def sShootWrite(self, rom, index):
        
        pattern = re.compile(r'\b(' + '|'.join(SHOOTS_CHAR.keys()) + r')\b')
        
        result = ''
        
        for c in index:
            hex = pattern.sub(lambda x: SHOOTS_CHAR[x.group()], str(c))
            
            if hex == ' ':
                hex = '\xFF'
            
            result += hex
        
        
        rom.seek(self.playerShootOffset[0])
        rom.write(result[0])
        
        rom.seek(self.playerShootOffset[1])
        rom.write(result[1])
        
        rom.seek(self.playerShootOffset[2])
        rom.write(result[2])
        
        rom.seek(self.playerShootOffset[3])
        rom.write(result[3])
        
        rom.seek(self.playerShootOffset[4])
        rom.write(result[4])


#-------------------------------------------------------------------------------
# utils


def convertint(int_value):
   encoded = format(int_value, 'x')

   length = len(encoded)
   encoded = encoded.zfill(length+length%2)

   return encoded.decode('hex')

def strtohex(string):
    
    string = string.encode('utf8')
    pattern = re.compile(r'\b(' + '|'.join(CHARS.keys()) + r')\b')
    
    result = ''
    
    for c in string:
        hex = pattern.sub(lambda x: CHARS[x.group()], c)
        
        if hex == ' ':
            hex = '\xFF'
        
        result += hex
    
    return result

def hextostr(hex):
    
    pattern = re.compile(r'(' + '|'.join(HEX.keys()) + r')')
    result = pattern.sub(lambda x: HEX[x.group()], hex)    

    return result

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1ANGRYSPINTEAM1CTRL1, wxID_FRAME1ANGRYSPINTEAM1CTRL2, 
 wxID_FRAME1ANGRYSPINTEAM1CTRL3, wxID_FRAME1ANGRYSPINTEAM1CTRL4, 
 wxID_FRAME1ANGRYSPINTEAM1CTRL5, wxID_FRAME1BUTTON1, wxID_FRAME1BUTTON2, 
 wxID_FRAME1CHECKBOX1, wxID_FRAME1CHOICE1, wxID_FRAME1CHOICE2, 
 wxID_FRAME1CHOICE3, wxID_FRAME1CHOICE4, wxID_FRAME1CHOICE5, 
 wxID_FRAME1MINCTRL1, wxID_FRAME1MPOWERSPINTEAM1CTRL1, 
 wxID_FRAME1MPOWERSPINTEAM1CTRL2, wxID_FRAME1MPOWERSPINTEAM1CTRL3, 
 wxID_FRAME1MPOWERSPINTEAM1CTRL4, wxID_FRAME1MPOWERSPINTEAM1CTRL5, 
 wxID_FRAME1NOTEBOOK1, wxID_FRAME1PANEL1, wxID_FRAME1PANEL2, 
 wxID_FRAME1PANEL3, wxID_FRAME1PANEL4, wxID_FRAME1PANEL5, wxID_FRAME1PANEL6, 
 wxID_FRAME1PANEL7, wxID_FRAME1PANEL8, wxID_FRAME1PANEL9, wxID_FRAME1SECCTRL1, 
 wxID_FRAME1SHOOTCTRL1, wxID_FRAME1SHOOTTEAM1CHOICE1, 
 wxID_FRAME1SHOOTTEAM1CHOICE2, wxID_FRAME1SHOOTTEAM1CHOICE3, 
 wxID_FRAME1SHOOTTEAM1CHOICE4, wxID_FRAME1SHOOTTEAM1CHOICE5, 
 wxID_FRAME1SPEEDSPINTEAM1CTRL1, wxID_FRAME1SPEEDSPINTEAM1CTRL2, 
 wxID_FRAME1SPEEDSPINTEAM1CTRL3, wxID_FRAME1SPEEDSPINTEAM1CTRL4, 
 wxID_FRAME1SPEEDSPINTEAM1CTRL5, wxID_FRAME1SPOWERSPINTEAM1CTRL1, 
 wxID_FRAME1SPOWERSPINTEAM1CTRL2, wxID_FRAME1SPOWERSPINTEAM1CTRL3, 
 wxID_FRAME1SPOWERSPINTEAM1CTRL4, wxID_FRAME1SPOWERSPINTEAM1CTRL5, 
 wxID_FRAME1STATICTEXT1, wxID_FRAME1STATICTEXT10, wxID_FRAME1STATICTEXT11, 
 wxID_FRAME1STATICTEXT12, wxID_FRAME1STATICTEXT13, wxID_FRAME1STATICTEXT14, 
 wxID_FRAME1STATICTEXT15, wxID_FRAME1STATICTEXT16, wxID_FRAME1STATICTEXT17, 
 wxID_FRAME1STATICTEXT18, wxID_FRAME1STATICTEXT19, wxID_FRAME1STATICTEXT2, 
 wxID_FRAME1STATICTEXT20, wxID_FRAME1STATICTEXT21, wxID_FRAME1STATICTEXT22, 
 wxID_FRAME1STATICTEXT23, wxID_FRAME1STATICTEXT24, wxID_FRAME1STATICTEXT25, 
 wxID_FRAME1STATICTEXT26, wxID_FRAME1STATICTEXT27, wxID_FRAME1STATICTEXT28, 
 wxID_FRAME1STATICTEXT29, wxID_FRAME1STATICTEXT3, wxID_FRAME1STATICTEXT30, 
 wxID_FRAME1STATICTEXT31, wxID_FRAME1STATICTEXT32, wxID_FRAME1STATICTEXT33, 
 wxID_FRAME1STATICTEXT34, wxID_FRAME1STATICTEXT35, wxID_FRAME1STATICTEXT36, 
 wxID_FRAME1STATICTEXT37, wxID_FRAME1STATICTEXT38, wxID_FRAME1STATICTEXT39, 
 wxID_FRAME1STATICTEXT4, wxID_FRAME1STATICTEXT40, wxID_FRAME1STATICTEXT41, 
 wxID_FRAME1STATICTEXT42, wxID_FRAME1STATICTEXT43, wxID_FRAME1STATICTEXT44, 
 wxID_FRAME1STATICTEXT45, wxID_FRAME1STATICTEXT46, wxID_FRAME1STATICTEXT47, 
 wxID_FRAME1STATICTEXT48, wxID_FRAME1STATICTEXT49, wxID_FRAME1STATICTEXT5, 
 wxID_FRAME1STATICTEXT50, wxID_FRAME1STATICTEXT51, wxID_FRAME1STATICTEXT6, 
 wxID_FRAME1STATICTEXT7, wxID_FRAME1STATICTEXT8, wxID_FRAME1STATICTEXT9, 
 wxID_FRAME1TEAM1ATTACKSPINCTRL1, wxID_FRAME1TEAM1DEFENSESPINCTRL1, 
 wxID_FRAME1TEAM1PLAYER1CTRL, wxID_FRAME1TEAM1PLAYER2CTRL, 
 wxID_FRAME1TEAM1PLAYER3CTRL, wxID_FRAME1TEAM1PLAYER4CTRL, 
 wxID_FRAME1TEAM1PLAYER5CTRL, wxID_FRAME1TEAM2ATTACKSPINCTRL1, 
 wxID_FRAME1TEAM2DEFENSESPINCTRL1, wxID_FRAME1TEAM2PLAYER1CTRL, 
 wxID_FRAME1TEAM2PLAYER2CTRL, wxID_FRAME1TEAM2PLAYER3CTRL, 
 wxID_FRAME1TEAM2PLAYER4CTRL, wxID_FRAME1TEAM2PLAYER5CTRL, 
 wxID_FRAME1TEAM3ATTACKSPINCTRL1, wxID_FRAME1TEAM3DEFENSESPINCTRL1, 
 wxID_FRAME1TEAM3PLAYER1CTRL, wxID_FRAME1TEAM3PLAYER2CTRL, 
 wxID_FRAME1TEAM3PLAYER3CTRL, wxID_FRAME1TEAM3PLAYER4CTRL, 
 wxID_FRAME1TEAM3PLAYER5CTRL, wxID_FRAME1TEAM4ATTACKSPINCTRL1, 
 wxID_FRAME1TEAM4DEFENSESPINCTRL1, wxID_FRAME1TEAM4PLAYER1CTRL, 
 wxID_FRAME1TEAM4PLAYER2CTRL, wxID_FRAME1TEAM4PLAYER3CTRL, 
 wxID_FRAME1TEAM4PLAYER4CTRL, wxID_FRAME1TEAM4PLAYER5CTRL, 
 wxID_FRAME1TEAM5ATTACKSPINCTRL1, wxID_FRAME1TEAM5DEFENSESPINCTRL1, 
 wxID_FRAME1TEAM5PLAYER1CTRL, wxID_FRAME1TEAM5PLAYER2CTRL, 
 wxID_FRAME1TEAM5PLAYER3CTRL, wxID_FRAME1TEAM5PLAYER4CTRL, 
 wxID_FRAME1TEAM5PLAYER5CTRL, wxID_FRAME1TEAM6ATTACKSPINCTRL1, 
 wxID_FRAME1TEAM6DEFENSESPINCTRL1, wxID_FRAME1TEAM6PLAYER1CTRL, 
 wxID_FRAME1TEAM6PLAYER2CTRL, wxID_FRAME1TEAM6PLAYER3CTRL, 
 wxID_FRAME1TEAM6PLAYER4CTRL, wxID_FRAME1TEAM6PLAYER5CTRL, 
 wxID_FRAME1TEAM7ATTACKSPINCTRL1, wxID_FRAME1TEAM7DEFENSESPINCTRL1, 
 wxID_FRAME1TEAM7PLAYER1CTRL, wxID_FRAME1TEAM7PLAYER2CTRL, 
 wxID_FRAME1TEAM7PLAYER3CTRL, wxID_FRAME1TEAM7PLAYER4CTRL, 
 wxID_FRAME1TEAM7PLAYER5CTRL, wxID_FRAME1TEAM8ATTACKSPINCTRL1, 
 wxID_FRAME1TEAM8DEFENSESPINCTRL1, wxID_FRAME1TEAM8PLAYER1CTRL, 
 wxID_FRAME1TEAM8PLAYER2CTRL, wxID_FRAME1TEAM8PLAYER3CTRL, 
 wxID_FRAME1TEAM8PLAYER4CTRL, wxID_FRAME1TEAM8PLAYER5CTRL, 
 wxID_FRAME1TEAMNAMECTRL1, wxID_FRAME1TEAMNAMECTRL2, wxID_FRAME1TEAMNAMECTRL3, 
 wxID_FRAME1TEAMNAMECTRL4, wxID_FRAME1TEAMNAMECTRL5, wxID_FRAME1TEAMNAMECTRL6, 
 wxID_FRAME1TEAMNAMECTRL7, wxID_FRAME1TEAMNAMECTRL8, 
 wxID_FRAME1WEIGHTSPINTEAM1CTRL1, wxID_FRAME1WEIGHTSPINTEAM1CTRL2, 
 wxID_FRAME1WEIGHTSPINTEAM1CTRL3, wxID_FRAME1WEIGHTSPINTEAM1CTRL4, 
 wxID_FRAME1WEIGHTSPINTEAM1CTRL5, 
] = [wx.NewId() for _init_ctrls in range(167)]

class Frame1(wx.Frame):
    def _init_coll_notebook1_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panel2, select=False,
              text=u'Team 1')
        parent.AddPage(imageId=-1, page=self.panel3, select=False,
              text=u'Team 2')
        parent.AddPage(imageId=-1, page=self.panel4, select=True,
              text=u'Team 3')
        parent.AddPage(imageId=-1, page=self.panel5, select=False,
              text=u'Team 4')
        parent.AddPage(imageId=-1, page=self.panel6, select=False,
              text=u'Team 5')
        parent.AddPage(imageId=-1, page=self.panel7, select=False,
              text=u'Team 6')
        parent.AddPage(imageId=-1, page=self.panel8, select=False,
              text=u'Team 7')
        parent.AddPage(imageId=-1, page=self.panel9, select=False,
              text=u'Team 8')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(350, 279), size=wx.Size(850, 428),
              style=wx.DEFAULT_FRAME_STYLE, title=u'TurBo Hockey Editor 3000')
        self.SetClientSize(wx.Size(842, 401))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(842, 401),
              style=wx.TAB_TRAVERSAL)
        self.panel1.SetToolTipString(u'')

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'Time', name='staticText1', parent=self.panel1,
              pos=wx.Point(64, 24), size=wx.Size(29, 14), style=0)

        self.minCtrl1 = wx.TextCtrl(id=wxID_FRAME1MINCTRL1, name=u'minCtrl1',
              parent=self.panel1, pos=wx.Point(56, 40), size=wx.Size(24, 21),
              style=0, value=u'0')
        self.minCtrl1.SetLabelText(u'0')
        self.minCtrl1.SetMaxLength(1)
        self.minCtrl1.SetToolTipString(u'Minutes')
        self.minCtrl1.Bind(wx.EVT_TEXT, self.OnMinCtrl1Text,
              id=wxID_FRAME1MINCTRL1)

        self.secCtrl1 = wx.TextCtrl(id=wxID_FRAME1SECCTRL1, name=u'secCtrl1',
              parent=self.panel1, pos=wx.Point(80, 40), size=wx.Size(24, 21),
              style=0, value=u'0')
        self.secCtrl1.SetLabelText(u'0')
        self.secCtrl1.SetMaxLength(1)
        self.secCtrl1.SetToolTipString(u'Seconds')
        self.secCtrl1.SetInsertionPoint(1)
        self.secCtrl1.SetHelpText(u'')
        self.secCtrl1.Bind(wx.EVT_TEXT, self.OnSecCtrl1Text,
              id=wxID_FRAME1SECCTRL1)

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label=u'Charge Time', name='staticText2', parent=self.panel1,
              pos=wx.Point(128, 24), size=wx.Size(60, 14), style=0)

        self.shootCtrl1 = wx.TextCtrl(id=wxID_FRAME1SHOOTCTRL1,
              name=u'shootCtrl1', parent=self.panel1, pos=wx.Point(144, 40),
              size=wx.Size(32, 21), style=0, value=u'0')
        self.shootCtrl1.SetLabelText(u'0')
        self.shootCtrl1.SetToolTipString(u'Super shoot time')
        self.shootCtrl1.SetMaxLength(3)
        self.shootCtrl1.Bind(wx.EVT_TEXT, self.OnShootCtrl1Text,
              id=wxID_FRAME1SHOOTCTRL1)

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label=u'Field 1', name='staticText3', parent=self.panel1,
              pos=wx.Point(232, 24), size=wx.Size(31, 14), style=0)

        self.staticText4 = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label=u'Field 2', name='staticText4', parent=self.panel1,
              pos=wx.Point(296, 24), size=wx.Size(31, 14), style=0)

        self.staticText5 = wx.StaticText(id=wxID_FRAME1STATICTEXT5,
              label=u'Field 3', name='staticText5', parent=self.panel1,
              pos=wx.Point(360, 24), size=wx.Size(31, 14), style=0)

        self.staticText6 = wx.StaticText(id=wxID_FRAME1STATICTEXT6,
              label=u'Field 4', name='staticText6', parent=self.panel1,
              pos=wx.Point(424, 24), size=wx.Size(31, 14), style=0)

        self.choice1 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE1,
              name='choice1', parent=self.panel1, pos=wx.Point(480, 40),
              size=wx.Size(48, 21), style=0)
        self.choice1.SetToolTipString(u'Field 5 music theme')
        self.choice1.Bind(wx.EVT_CHOICE, self.OnChoice1Choice,
              id=wxID_FRAME1CHOICE1)

        self.choice2 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE2,
              name='choice2', parent=self.panel1, pos=wx.Point(288, 40),
              size=wx.Size(48, 21), style=0)
        self.choice2.SetToolTipString(u'Field 2 music theme')
        self.choice2.Bind(wx.EVT_CHOICE, self.OnChoice2Choice,
              id=wxID_FRAME1CHOICE2)

        self.choice3 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE3,
              name='choice3', parent=self.panel1, pos=wx.Point(352, 40),
              size=wx.Size(48, 21), style=0)
        self.choice3.SetToolTipString(u'Field 3 music theme')
        self.choice3.Bind(wx.EVT_CHOICE, self.OnChoice3Choice,
              id=wxID_FRAME1CHOICE3)

        self.choice4 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE4,
              name='choice4', parent=self.panel1, pos=wx.Point(416, 40),
              size=wx.Size(48, 21), style=0)
        self.choice4.SetToolTipString(u'Field 4 music theme')
        self.choice4.Bind(wx.EVT_CHOICE, self.OnChoice4Choice,
              id=wxID_FRAME1CHOICE4)

        self.staticText7 = wx.StaticText(id=wxID_FRAME1STATICTEXT7,
              label=u'Music', name='staticText7', parent=self.panel1,
              pos=wx.Point(360, 8), size=wx.Size(26, 14), style=0)

        self.checkBox1 = wx.CheckBox(id=wxID_FRAME1CHECKBOX1,
              label=u'No Penalty', name='checkBox1', parent=self.panel1,
              pos=wx.Point(552, 40), size=wx.Size(70, 13), style=0)
        self.checkBox1.SetValue(False)
        self.checkBox1.SetToolTipString(u'Enable / Disable penalty')
        self.checkBox1.Bind(wx.EVT_CHECKBOX, self.OnCheckBox1Checkbox,
              id=wxID_FRAME1CHECKBOX1)

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label=u'Load',
              name='button1', parent=self.panel1, pos=wx.Point(752, 8),
              size=wx.Size(75, 23), style=0)
        self.button1.SetToolTipString(u'Load rom')
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME1BUTTON1)

        self.button2 = wx.Button(id=wxID_FRAME1BUTTON2, label=u'Save',
              name='button2', parent=self.panel1, pos=wx.Point(752, 40),
              size=wx.Size(75, 23), style=0)
        self.button2.SetToolTipString(u'Save rom')
        self.button2.Enable(False)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button,
              id=wxID_FRAME1BUTTON2)

        self.notebook1 = wx.Notebook(id=wxID_FRAME1NOTEBOOK1, name='notebook1',
              parent=self.panel1, pos=wx.Point(8, 72), size=wx.Size(824, 320),
              style=0)
        self.notebook1.SetToolTipString(u'')

        self.panel8 = wx.Panel(id=wxID_FRAME1PANEL8, name='panel8',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(816, 294),
              style=wx.TAB_TRAVERSAL)

        self.panel9 = wx.Panel(id=wxID_FRAME1PANEL9, name='panel9',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(816, 294),
              style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id=wxID_FRAME1PANEL2, name='panel2',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(816, 294),
              style=wx.TAB_TRAVERSAL)
        self.panel2.SetToolTipString(u'')

        self.teamNameCtrl1 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL1,
              name=u'teamNameCtrl1', parent=self.panel2, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl1.SetMaxLength(8)
        self.teamNameCtrl1.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl1Text,
              id=wxID_FRAME1TEAMNAMECTRL1)

        self.sPowerSpinTeam1Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM1CTRL1,
              initial=1, max=5, min=1, name=u'sPowerSpinTeam1Ctrl1',
              parent=self.panel2, pos=wx.Point(240, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam1Ctrl1.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam1Ctrl1Text,
              id=wxID_FRAME1SPOWERSPINTEAM1CTRL1)

        self.staticText8 = wx.StaticText(id=wxID_FRAME1STATICTEXT8,
              label=u'Team name :', name='staticText8', parent=self.panel2,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.staticText20 = wx.StaticText(id=wxID_FRAME1STATICTEXT20,
              label=u'7', name='staticText20', parent=self.panel2,
              pos=wx.Point(552, 48), size=wx.Size(6, 14), style=0)

        self.team1Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM1PLAYER5CTRL,
              name=u'team1Player5Ctrl', parent=self.panel2, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team1Player5Ctrl.SetMaxLength(4)
        self.team1Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam1Player5CtrlText,
              id=wxID_FRAME1TEAM1PLAYER5CTRL)

        self.team1Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM1PLAYER4CTRL,
              name=u'team1Player4Ctrl', parent=self.panel2, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team1Player4Ctrl.SetMaxLength(4)
        self.team1Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam1Player4CtrlText,
              id=wxID_FRAME1TEAM1PLAYER4CTRL)

        self.team1Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM1PLAYER1CTRL,
              name=u'team1Player1Ctrl', parent=self.panel2, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team1Player1Ctrl.SetMaxLength(4)
        self.team1Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam1Player1CtrlText,
              id=wxID_FRAME1TEAM1PLAYER1CTRL)

        self.mPowerSpinTeam1Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM1CTRL4,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam1Ctrl4',
              parent=self.panel2, pos=wx.Point(328, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.mPowerSpinTeam1Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM1CTRL5,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam1Ctrl5',
              parent=self.panel2, pos=wx.Point(328, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.mPowerSpinTeam1Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM1CTRL2,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam1Ctrl2',
              parent=self.panel2, pos=wx.Point(328, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.mPowerSpinTeam1Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM1CTRL3,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam1Ctrl3',
              parent=self.panel2, pos=wx.Point(328, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.mPowerSpinTeam1Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINTEAM1CTRL1,
              initial=1, max=5, min=1, name=u'mPowerSpinTeam1Ctrl1',
              parent=self.panel2, pos=wx.Point(328, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.weightSpinTeam1Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM1CTRL4,
              initial=1, max=5, min=1, name=u'weightSpinTeam1Ctrl4',
              parent=self.panel2, pos=wx.Point(464, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.weightSpinTeam1Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM1CTRL5,
              initial=1, max=5, min=1, name=u'weightSpinTeam1Ctrl5',
              parent=self.panel2, pos=wx.Point(464, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.weightSpinTeam1Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM1CTRL2,
              initial=1, max=5, min=1, name=u'weightSpinTeam1Ctrl2',
              parent=self.panel2, pos=wx.Point(464, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.weightSpinTeam1Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM1CTRL3,
              initial=1, max=5, min=1, name=u'weightSpinTeam1Ctrl3',
              parent=self.panel2, pos=wx.Point(464, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.weightSpinTeam1Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINTEAM1CTRL1,
              initial=1, max=5, min=1, name=u'weightSpinTeam1Ctrl1',
              parent=self.panel2, pos=wx.Point(464, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.sPowerSpinTeam1Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM1CTRL4,
              initial=1, max=5, min=1, name=u'sPowerSpinTeam1Ctrl4',
              parent=self.panel2, pos=wx.Point(240, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam1Ctrl4.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam1Ctrl4Text,
              id=wxID_FRAME1SPOWERSPINTEAM1CTRL4)

        self.sPowerSpinTeam1Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM1CTRL5,
              initial=1, max=5, min=1, name=u'sPowerSpinTeam1Ctrl5',
              parent=self.panel2, pos=wx.Point(240, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam1Ctrl5.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam1Ctrl5Text,
              id=wxID_FRAME1SPOWERSPINTEAM1CTRL5)

        self.sPowerSpinTeam1Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM1CTRL2,
              initial=1, max=5, min=1, name=u'sPowerSpinTeam1Ctrl2',
              parent=self.panel2, pos=wx.Point(240, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam1Ctrl2.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam1Ctrl2Text,
              id=wxID_FRAME1SPOWERSPINTEAM1CTRL2)

        self.staticText9 = wx.StaticText(id=wxID_FRAME1STATICTEXT9,
              label=u'Name', name='staticText9', parent=self.panel2,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.speedSpinTeam1Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM1CTRL1,
              initial=1, max=3, min=1, name=u'speedSpinTeam1Ctrl1',
              parent=self.panel2, pos=wx.Point(400, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.speedSpinTeam1Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM1CTRL2,
              initial=1, max=3, min=1, name=u'speedSpinTeam1Ctrl2',
              parent=self.panel2, pos=wx.Point(400, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.speedSpinTeam1Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM1CTRL3,
              initial=1, max=3, min=1, name=u'speedSpinTeam1Ctrl3',
              parent=self.panel2, pos=wx.Point(400, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.speedSpinTeam1Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM1CTRL4,
              initial=1, max=3, min=1, name=u'speedSpinTeam1Ctrl4',
              parent=self.panel2, pos=wx.Point(400, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.speedSpinTeam1Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINTEAM1CTRL5,
              initial=1, max=3, min=1, name=u'speedSpinTeam1Ctrl5',
              parent=self.panel2, pos=wx.Point(400, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.team1Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM1PLAYER3CTRL,
              name=u'team1Player3Ctrl', parent=self.panel2, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team1Player3Ctrl.SetMaxLength(4)
        self.team1Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam1Player3CtrlText,
              id=wxID_FRAME1TEAM1PLAYER3CTRL)

        self.team1Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM1PLAYER2CTRL,
              name=u'team1Player2Ctrl', parent=self.panel2, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team1Player2Ctrl.SetMaxLength(4)
        self.team1Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam1Player2CtrlText,
              id=wxID_FRAME1TEAM1PLAYER2CTRL)

        self.sPowerSpinTeam1Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINTEAM1CTRL3,
              initial=1, max=5, min=1, name=u'sPowerSpinTeam1Ctrl3',
              parent=self.panel2, pos=wx.Point(240, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.sPowerSpinTeam1Ctrl3.Bind(wx.EVT_TEXT,
              self.OnSPowerSpinTeam1Ctrl3Text,
              id=wxID_FRAME1SPOWERSPINTEAM1CTRL3)

        self.staticText10 = wx.StaticText(id=wxID_FRAME1STATICTEXT10,
              label=u'Start Power', name='staticText10', parent=self.panel2,
              pos=wx.Point(232, 32), size=wx.Size(57, 14), style=0)

        self.staticText11 = wx.StaticText(id=wxID_FRAME1STATICTEXT11,
              label=u'Max Power', name='staticText11', parent=self.panel2,
              pos=wx.Point(320, 32), size=wx.Size(53, 14), style=0)

        self.staticText12 = wx.StaticText(id=wxID_FRAME1STATICTEXT12,
              label=u'Speed', name='staticText12', parent=self.panel2,
              pos=wx.Point(400, 32), size=wx.Size(30, 14), style=0)

        self.staticText13 = wx.StaticText(id=wxID_FRAME1STATICTEXT13,
              label=u'Weight', name='staticText13', parent=self.panel2,
              pos=wx.Point(464, 32), size=wx.Size(34, 14), style=0)

        self.staticText14 = wx.StaticText(id=wxID_FRAME1STATICTEXT14,
              label=u'Angry', name='staticText14', parent=self.panel2,
              pos=wx.Point(544, 32), size=wx.Size(29, 14), style=0)

        self.staticText15 = wx.StaticText(id=wxID_FRAME1STATICTEXT15,
              label=u'Special Shot', name='staticText15', parent=self.panel2,
              pos=wx.Point(664, 32), size=wx.Size(58, 14), style=0)

        self.staticText16 = wx.StaticText(id=wxID_FRAME1STATICTEXT16,
              label=u'5', name='staticText16', parent=self.panel2,
              pos=wx.Point(256, 48), size=wx.Size(6, 14), style=0)
        self.staticText16.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))

        self.staticText17 = wx.StaticText(id=wxID_FRAME1STATICTEXT17,
              label=u'5', name='staticText17', parent=self.panel2,
              pos=wx.Point(344, 48), size=wx.Size(6, 14), style=0)

        self.staticText18 = wx.StaticText(id=wxID_FRAME1STATICTEXT18,
              label=u'3', name='staticText18', parent=self.panel2,
              pos=wx.Point(416, 48), size=wx.Size(12, 14), style=0)

        self.staticText19 = wx.StaticText(id=wxID_FRAME1STATICTEXT19,
              label=u'5', name='staticText19', parent=self.panel2,
              pos=wx.Point(480, 48), size=wx.Size(6, 14), style=0)

        self.angrySpinTeam1Ctrl4 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM1CTRL4,
              initial=1, max=7, min=1, name=u'angrySpinTeam1Ctrl4',
              parent=self.panel2, pos=wx.Point(536, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.angrySpinTeam1Ctrl5 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM1CTRL5,
              initial=1, max=7, min=1, name=u'angrySpinTeam1Ctrl5',
              parent=self.panel2, pos=wx.Point(536, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.angrySpinTeam1Ctrl2 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM1CTRL2,
              initial=1, max=7, min=1, name=u'angrySpinTeam1Ctrl2',
              parent=self.panel2, pos=wx.Point(536, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.angrySpinTeam1Ctrl3 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM1CTRL3,
              initial=1, max=7, min=1, name=u'angrySpinTeam1Ctrl3',
              parent=self.panel2, pos=wx.Point(536, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.angrySpinTeam1Ctrl1 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINTEAM1CTRL1,
              initial=1, max=7, min=1, name=u'angrySpinTeam1Ctrl1',
              parent=self.panel2, pos=wx.Point(536, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.panel3 = wx.Panel(id=wxID_FRAME1PANEL3, name='panel3',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(816, 294),
              style=wx.TAB_TRAVERSAL)
        self.panel3.SetToolTipString(u'')

        self.panel4 = wx.Panel(id=wxID_FRAME1PANEL4, name='panel4',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(816, 294),
              style=wx.TAB_TRAVERSAL)
        self.panel4.SetToolTipString(u'')

        self.panel5 = wx.Panel(id=wxID_FRAME1PANEL5, name='panel5',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(816, 294),
              style=wx.TAB_TRAVERSAL)

        self.panel6 = wx.Panel(id=wxID_FRAME1PANEL6, name='panel6',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(816, 294),
              style=wx.TAB_TRAVERSAL)

        self.panel7 = wx.Panel(id=wxID_FRAME1PANEL7, name='panel7',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(816, 294),
              style=wx.TAB_TRAVERSAL)

        self.staticText22 = wx.StaticText(id=wxID_FRAME1STATICTEXT22,
              label=u'Team name :', name='staticText22', parent=self.panel3,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.teamNameCtrl2 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL2,
              name=u'teamNameCtrl2', parent=self.panel3, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl2.SetMaxLength(8)
        self.teamNameCtrl2.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl2Text,
              id=wxID_FRAME1TEAMNAMECTRL2)

        self.staticText23 = wx.StaticText(id=wxID_FRAME1STATICTEXT23,
              label=u'Name', name='staticText23', parent=self.panel3,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.team2Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM2PLAYER1CTRL,
              name=u'team2Player1Ctrl', parent=self.panel3, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team2Player1Ctrl.SetMaxLength(4)
        self.team2Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam2Player1CtrlText,
              id=wxID_FRAME1TEAM2PLAYER1CTRL)

        self.team2Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM2PLAYER2CTRL,
              name=u'team2Player2Ctrl', parent=self.panel3, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team2Player2Ctrl.SetMaxLength(4)
        self.team2Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam2Player2CtrlText,
              id=wxID_FRAME1TEAM2PLAYER2CTRL)

        self.team2Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM2PLAYER3CTRL,
              name=u'team2Player3Ctrl', parent=self.panel3, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team2Player3Ctrl.SetMaxLength(4)
        self.team2Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam2Player3CtrlText,
              id=wxID_FRAME1TEAM2PLAYER3CTRL)

        self.team2Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM2PLAYER4CTRL,
              name=u'team2Player4Ctrl', parent=self.panel3, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team2Player4Ctrl.SetMaxLength(4)
        self.team2Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam2Player4CtrlText,
              id=wxID_FRAME1TEAM2PLAYER4CTRL)

        self.team2Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM2PLAYER5CTRL,
              name=u'team2Player5Ctrl', parent=self.panel3, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team2Player5Ctrl.SetMaxLength(4)
        self.team2Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam2Player5CtrlText,
              id=wxID_FRAME1TEAM2PLAYER5CTRL)

        self.staticText24 = wx.StaticText(id=wxID_FRAME1STATICTEXT24,
              label=u'Team name :', name='staticText24', parent=self.panel4,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.teamNameCtrl3 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL3,
              name=u'teamNameCtrl3', parent=self.panel4, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl3.SetMaxLength(8)
        self.teamNameCtrl3.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl3Text,
              id=wxID_FRAME1TEAMNAMECTRL3)

        self.staticText25 = wx.StaticText(id=wxID_FRAME1STATICTEXT25,
              label=u'Name', name='staticText25', parent=self.panel4,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.team3Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM3PLAYER1CTRL,
              name=u'team3Player1Ctrl', parent=self.panel4, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team3Player1Ctrl.SetMaxLength(4)
        self.team3Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam3Player1CtrlText,
              id=wxID_FRAME1TEAM3PLAYER1CTRL)

        self.team3Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM3PLAYER2CTRL,
              name=u'team3Player2Ctrl', parent=self.panel4, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team3Player2Ctrl.SetMaxLength(4)
        self.team3Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam3Player2CtrlText,
              id=wxID_FRAME1TEAM3PLAYER2CTRL)

        self.team3Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM3PLAYER3CTRL,
              name=u'team3Player3Ctrl', parent=self.panel4, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team3Player3Ctrl.SetMaxLength(4)
        self.team3Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam3Player3CtrlText,
              id=wxID_FRAME1TEAM3PLAYER3CTRL)

        self.team3Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM3PLAYER4CTRL,
              name=u'team3Player4Ctrl', parent=self.panel4, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team3Player4Ctrl.SetMaxLength(4)
        self.team3Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam3Player4CtrlText,
              id=wxID_FRAME1TEAM3PLAYER4CTRL)

        self.team3Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM3PLAYER5CTRL,
              name=u'team3Player5Ctrl', parent=self.panel4, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team3Player5Ctrl.SetMaxLength(4)
        self.team3Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam3Player5CtrlText,
              id=wxID_FRAME1TEAM3PLAYER5CTRL)

        self.shootTeam1Choice1 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM1CHOICE1, name=u'shootTeam1Choice1',
              parent=self.panel2, pos=wx.Point(600, 64), size=wx.Size(200, 21),
              style=0)
        self.shootTeam1Choice1.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice1Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE1)

        self.shootTeam1Choice2 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM1CHOICE2, name=u'shootTeam1Choice2',
              parent=self.panel2, pos=wx.Point(600, 96), size=wx.Size(200, 21),
              style=0)
        self.shootTeam1Choice2.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice2Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE2)

        self.shootTeam1Choice3 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM1CHOICE3, name=u'shootTeam1Choice3',
              parent=self.panel2, pos=wx.Point(600, 128), size=wx.Size(200, 21),
              style=0)
        self.shootTeam1Choice3.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice3Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE3)

        self.shootTeam1Choice4 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM1CHOICE4, name=u'shootTeam1Choice4',
              parent=self.panel2, pos=wx.Point(600, 160), size=wx.Size(200, 21),
              style=0)
        self.shootTeam1Choice4.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice4Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE4)

        self.shootTeam1Choice5 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM1CHOICE5, name=u'shootTeam1Choice5',
              parent=self.panel2, pos=wx.Point(600, 192), size=wx.Size(200, 21),
              style=0)
        self.shootTeam1Choice5.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice5Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE5)

        self.team1AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM1ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team1AttackSpinCtrl1',
              parent=self.panel2, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team1AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam1AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM1ATTACKSPINCTRL1)

        self.team1DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM1DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team1DefenseSpinCtrl1',
              parent=self.panel2, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team1DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam1DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM1DEFENSESPINCTRL1)

        self.staticText21 = wx.StaticText(id=wxID_FRAME1STATICTEXT21,
              label=u'Team attack', name='staticText21', parent=self.panel2,
              pos=wx.Point(40, 48), size=wx.Size(59, 14), style=0)

        self.staticText26 = wx.StaticText(id=wxID_FRAME1STATICTEXT26,
              label=u'Team defense', name='staticText26', parent=self.panel2,
              pos=wx.Point(40, 120), size=wx.Size(69, 14), style=0)

        self.choice5 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE5,
              name='choice5', parent=self.panel1, pos=wx.Point(224, 40),
              size=wx.Size(48, 21), style=0)
        self.choice5.SetToolTipString(u'Field 1 music theme')
        self.choice5.Bind(wx.EVT_CHOICE, self.OnChoice5Choice,
              id=wxID_FRAME1CHOICE5)

        self.staticText27 = wx.StaticText(id=wxID_FRAME1STATICTEXT27,
              label=u'Field 5', name='staticText27', parent=self.panel1,
              pos=wx.Point(488, 24), size=wx.Size(31, 14), style=0)

        self.staticText28 = wx.StaticText(id=wxID_FRAME1STATICTEXT28,
              label=u'Team name :', name='staticText28', parent=self.panel5,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.staticText29 = wx.StaticText(id=wxID_FRAME1STATICTEXT29,
              label=u'Name', name='staticText29', parent=self.panel5,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.staticText30 = wx.StaticText(id=wxID_FRAME1STATICTEXT30,
              label=u'Team name :', name='staticText30', parent=self.panel6,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.staticText31 = wx.StaticText(id=wxID_FRAME1STATICTEXT31,
              label=u'Name', name='staticText31', parent=self.panel6,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.staticText32 = wx.StaticText(id=wxID_FRAME1STATICTEXT32,
              label=u'Team name :', name='staticText32', parent=self.panel7,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.staticText33 = wx.StaticText(id=wxID_FRAME1STATICTEXT33,
              label=u'Name', name='staticText33', parent=self.panel7,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.staticText34 = wx.StaticText(id=wxID_FRAME1STATICTEXT34,
              label=u'Team name :', name='staticText34', parent=self.panel8,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.staticText35 = wx.StaticText(id=wxID_FRAME1STATICTEXT35,
              label=u'Name', name='staticText35', parent=self.panel8,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.staticText36 = wx.StaticText(id=wxID_FRAME1STATICTEXT36,
              label=u'Team name :', name='staticText36', parent=self.panel9,
              pos=wx.Point(16, 16), size=wx.Size(62, 14), style=0)

        self.staticText37 = wx.StaticText(id=wxID_FRAME1STATICTEXT37,
              label=u'Name', name='staticText37', parent=self.panel9,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.teamNameCtrl4 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL4,
              name=u'teamNameCtrl4', parent=self.panel5, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl4.SetMaxLength(8)
        self.teamNameCtrl4.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl4Text,
              id=wxID_FRAME1TEAMNAMECTRL4)

        self.teamNameCtrl5 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL5,
              name=u'teamNameCtrl5', parent=self.panel6, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl5.SetMaxLength(8)
        self.teamNameCtrl5.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl5Text,
              id=wxID_FRAME1TEAMNAMECTRL5)

        self.teamNameCtrl6 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL6,
              name=u'teamNameCtrl6', parent=self.panel7, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl6.SetMaxLength(8)
        self.teamNameCtrl6.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl6Text,
              id=wxID_FRAME1TEAMNAMECTRL6)

        self.teamNameCtrl7 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL7,
              name=u'teamNameCtrl7', parent=self.panel8, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl7.SetMaxLength(8)
        self.teamNameCtrl7.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl7Text,
              id=wxID_FRAME1TEAMNAMECTRL7)

        self.teamNameCtrl8 = wx.TextCtrl(id=wxID_FRAME1TEAMNAMECTRL8,
              name=u'teamNameCtrl8', parent=self.panel9, pos=wx.Point(96, 16),
              size=wx.Size(110, 21), style=0, value=u'')
        self.teamNameCtrl8.SetMaxLength(8)
        self.teamNameCtrl8.Bind(wx.EVT_TEXT, self.OnTeamNameCtrl8Text,
              id=wxID_FRAME1TEAMNAMECTRL8)

        self.team4Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM4PLAYER1CTRL,
              name=u'team4Player1Ctrl', parent=self.panel5, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team4Player1Ctrl.SetMaxLength(4)
        self.team4Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam4Player1CtrlText,
              id=wxID_FRAME1TEAM4PLAYER1CTRL)

        self.team4Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM4PLAYER2CTRL,
              name=u'team4Player2Ctrl', parent=self.panel5, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team4Player2Ctrl.SetMaxLength(4)
        self.team4Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam4Player2CtrlText,
              id=wxID_FRAME1TEAM4PLAYER2CTRL)

        self.team4Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM4PLAYER3CTRL,
              name=u'team4Player3Ctrl', parent=self.panel5, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team4Player3Ctrl.SetMaxLength(4)
        self.team4Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam4Player3CtrlText,
              id=wxID_FRAME1TEAM4PLAYER3CTRL)

        self.team4Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM4PLAYER4CTRL,
              name=u'team4Player4Ctrl', parent=self.panel5, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team4Player4Ctrl.SetMaxLength(4)
        self.team4Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam4Player4CtrlText,
              id=wxID_FRAME1TEAM4PLAYER4CTRL)

        self.team4Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM4PLAYER5CTRL,
              name=u'team4Player5Ctrl', parent=self.panel5, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team4Player5Ctrl.SetMaxLength(4)
        self.team4Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam4Player5CtrlText,
              id=wxID_FRAME1TEAM4PLAYER5CTRL)

        self.team5Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM5PLAYER1CTRL,
              name=u'team5Player1Ctrl', parent=self.panel6, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team5Player1Ctrl.SetMaxLength(4)
        self.team5Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam5Player1CtrlText,
              id=wxID_FRAME1TEAM5PLAYER1CTRL)

        self.team5Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM5PLAYER2CTRL,
              name=u'team5Player2Ctrl', parent=self.panel6, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team5Player2Ctrl.SetMaxLength(4)
        self.team5Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam5Player2CtrlText,
              id=wxID_FRAME1TEAM5PLAYER2CTRL)

        self.team5Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM5PLAYER3CTRL,
              name=u'team5Player3Ctrl', parent=self.panel6, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team5Player3Ctrl.SetMaxLength(4)
        self.team5Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam5Player3CtrlText,
              id=wxID_FRAME1TEAM5PLAYER3CTRL)

        self.team5Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM5PLAYER4CTRL,
              name=u'team5Player4Ctrl', parent=self.panel6, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team5Player4Ctrl.SetMaxLength(4)
        self.team5Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam5Player4CtrlText,
              id=wxID_FRAME1TEAM5PLAYER4CTRL)

        self.team5Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM5PLAYER5CTRL,
              name=u'team5Player5Ctrl', parent=self.panel6, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team5Player5Ctrl.SetMaxLength(4)
        self.team5Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam5Player5CtrlText,
              id=wxID_FRAME1TEAM5PLAYER5CTRL)

        self.team6Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM6PLAYER1CTRL,
              name=u'team6Player1Ctrl', parent=self.panel7, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team6Player1Ctrl.SetMaxLength(4)
        self.team6Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam6Player1CtrlText,
              id=wxID_FRAME1TEAM6PLAYER1CTRL)

        self.team6Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM6PLAYER2CTRL,
              name=u'team6Player2Ctrl', parent=self.panel7, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team6Player2Ctrl.SetMaxLength(4)
        self.team6Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam6Player2CtrlText,
              id=wxID_FRAME1TEAM6PLAYER2CTRL)

        self.team6Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM6PLAYER3CTRL,
              name=u'team6Player3Ctrl', parent=self.panel7, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team6Player3Ctrl.SetMaxLength(4)
        self.team6Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam6Player3CtrlText,
              id=wxID_FRAME1TEAM6PLAYER3CTRL)

        self.team6Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM6PLAYER4CTRL,
              name=u'team6Player4Ctrl', parent=self.panel7, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team6Player4Ctrl.SetMaxLength(4)
        self.team6Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam6Player4CtrlText,
              id=wxID_FRAME1TEAM6PLAYER4CTRL)

        self.team6Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM6PLAYER5CTRL,
              name=u'team6Player5Ctrl', parent=self.panel7, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team6Player5Ctrl.SetMaxLength(4)
        self.team6Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam6Player5CtrlText,
              id=wxID_FRAME1TEAM6PLAYER5CTRL)

        self.team7Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM7PLAYER1CTRL,
              name=u'team7Player1Ctrl', parent=self.panel8, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team7Player1Ctrl.SetMaxLength(4)
        self.team7Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam7Player1CtrlText,
              id=wxID_FRAME1TEAM7PLAYER1CTRL)

        self.team7Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM7PLAYER2CTRL,
              name=u'team7Player2Ctrl', parent=self.panel8, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team7Player2Ctrl.SetMaxLength(4)
        self.team7Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam7Player2CtrlText,
              id=wxID_FRAME1TEAM7PLAYER2CTRL)

        self.team7Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM7PLAYER3CTRL,
              name=u'team7Player3Ctrl', parent=self.panel8, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team7Player3Ctrl.SetMaxLength(4)
        self.team7Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam7Player3CtrlText,
              id=wxID_FRAME1TEAM7PLAYER3CTRL)

        self.team7Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM7PLAYER4CTRL,
              name=u'team7Player4Ctrl', parent=self.panel8, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team7Player4Ctrl.SetMaxLength(4)
        self.team7Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam7Player4CtrlText,
              id=wxID_FRAME1TEAM7PLAYER4CTRL)

        self.team7Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM7PLAYER5CTRL,
              name=u'team7Player5Ctrl', parent=self.panel8, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team7Player5Ctrl.SetMaxLength(4)
        self.team7Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam7Player5CtrlText,
              id=wxID_FRAME1TEAM7PLAYER5CTRL)

        self.team8Player1Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM8PLAYER1CTRL,
              name=u'team8Player1Ctrl', parent=self.panel9, pos=wx.Point(136,
              64), size=wx.Size(56, 21), style=0, value=u'')
        self.team8Player1Ctrl.SetMaxLength(4)
        self.team8Player1Ctrl.Bind(wx.EVT_TEXT, self.OnTeam8Player1CtrlText,
              id=wxID_FRAME1TEAM8PLAYER1CTRL)

        self.team8Player2Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM8PLAYER2CTRL,
              name=u'team8Player2Ctrl', parent=self.panel9, pos=wx.Point(136,
              96), size=wx.Size(56, 21), style=0, value=u'')
        self.team8Player2Ctrl.SetMaxLength(4)
        self.team8Player2Ctrl.Bind(wx.EVT_TEXT, self.OnTeam8Player2CtrlText,
              id=wxID_FRAME1TEAM8PLAYER2CTRL)

        self.team8Player3Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM8PLAYER3CTRL,
              name=u'team8Player3Ctrl', parent=self.panel9, pos=wx.Point(136,
              128), size=wx.Size(56, 21), style=0, value=u'')
        self.team8Player3Ctrl.SetMaxLength(4)
        self.team8Player3Ctrl.Bind(wx.EVT_TEXT, self.OnTeam8Player3CtrlText,
              id=wxID_FRAME1TEAM8PLAYER3CTRL)

        self.team8Player4Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM8PLAYER4CTRL,
              name=u'team8Player4Ctrl', parent=self.panel9, pos=wx.Point(136,
              160), size=wx.Size(56, 21), style=0, value=u'')
        self.team8Player4Ctrl.SetMaxLength(4)
        self.team8Player4Ctrl.Bind(wx.EVT_TEXT, self.OnTeam8Player4CtrlText,
              id=wxID_FRAME1TEAM8PLAYER4CTRL)

        self.team8Player5Ctrl = wx.TextCtrl(id=wxID_FRAME1TEAM8PLAYER5CTRL,
              name=u'team8Player5Ctrl', parent=self.panel9, pos=wx.Point(136,
              192), size=wx.Size(56, 21), style=0, value=u'')
        self.team8Player5Ctrl.SetMaxLength(4)
        self.team8Player5Ctrl.Bind(wx.EVT_TEXT, self.OnTeam8Player5CtrlText,
              id=wxID_FRAME1TEAM8PLAYER5CTRL)

        self.staticText38 = wx.StaticText(id=wxID_FRAME1STATICTEXT38,
              label=u'Team attack', name='staticText38', parent=self.panel3,
              pos=wx.Point(40, 48), size=wx.Size(59, 14), style=0)

        self.staticText39 = wx.StaticText(id=wxID_FRAME1STATICTEXT39,
              label=u'Team defense', name='staticText39', parent=self.panel3,
              pos=wx.Point(40, 120), size=wx.Size(68, 14), style=0)

        self.team2AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM2ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team2AttackSpinCtrl1',
              parent=self.panel3, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team2AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam2AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM2ATTACKSPINCTRL1)

        self.team2DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM2DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team2DefenseSpinCtrl1',
              parent=self.panel3, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team2DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam2DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM2DEFENSESPINCTRL1)

        self.team3AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM3ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team3AttackSpinCtrl1',
              parent=self.panel4, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team3AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam3AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM3ATTACKSPINCTRL1)

        self.team3DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM3DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team3DefenseSpinCtrl1',
              parent=self.panel4, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team3DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam3DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM3DEFENSESPINCTRL1)

        self.staticText40 = wx.StaticText(id=wxID_FRAME1STATICTEXT40,
              label=u'Team attack', name='staticText40', parent=self.panel4,
              pos=wx.Point(40, 48), size=wx.Size(59, 14), style=0)

        self.staticText41 = wx.StaticText(id=wxID_FRAME1STATICTEXT41,
              label=u'Team defense', name='staticText41', parent=self.panel4,
              pos=wx.Point(40, 120), size=wx.Size(68, 14), style=0)

        self.staticText42 = wx.StaticText(id=wxID_FRAME1STATICTEXT42,
              label=u'Team attack', name='staticText42', parent=self.panel5,
              pos=wx.Point(40, 48), size=wx.Size(59, 14), style=0)

        self.staticText43 = wx.StaticText(id=wxID_FRAME1STATICTEXT43,
              label=u'Team defense', name='staticText43', parent=self.panel5,
              pos=wx.Point(40, 120), size=wx.Size(68, 14), style=0)

        self.team4AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM4ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team4AttackSpinCtrl1',
              parent=self.panel5, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team4AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam4AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM4ATTACKSPINCTRL1)

        self.team4DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM4DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team4DefenseSpinCtrl1',
              parent=self.panel5, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team4DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam4DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM4DEFENSESPINCTRL1)

        self.team5AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM5ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team5AttackSpinCtrl1',
              parent=self.panel6, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team5AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam5AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM5ATTACKSPINCTRL1)

        self.team5DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM5DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team5DefenseSpinCtrl1',
              parent=self.panel6, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team5DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam5DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM5DEFENSESPINCTRL1)

        self.staticText44 = wx.StaticText(id=wxID_FRAME1STATICTEXT44,
              label=u'Team attack', name='staticText44', parent=self.panel6,
              pos=wx.Point(40, 48), size=wx.Size(59, 14), style=0)

        self.staticText45 = wx.StaticText(id=wxID_FRAME1STATICTEXT45,
              label=u'Team defense', name='staticText45', parent=self.panel6,
              pos=wx.Point(40, 120), size=wx.Size(68, 14), style=0)

        self.staticText46 = wx.StaticText(id=wxID_FRAME1STATICTEXT46,
              label=u'Team attack', name='staticText46', parent=self.panel7,
              pos=wx.Point(40, 48), size=wx.Size(59, 14), style=0)

        self.staticText47 = wx.StaticText(id=wxID_FRAME1STATICTEXT47,
              label=u'Team defense', name='staticText47', parent=self.panel7,
              pos=wx.Point(40, 120), size=wx.Size(68, 14), style=0)

        self.team6AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM6ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team6AttackSpinCtrl1',
              parent=self.panel7, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team6AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam6AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM6ATTACKSPINCTRL1)

        self.team6DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM6DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team6DefenseSpinCtrl1',
              parent=self.panel7, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team6DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam6DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM6DEFENSESPINCTRL1)

        self.staticText48 = wx.StaticText(id=wxID_FRAME1STATICTEXT48,
              label=u'Team attack', name='staticText48', parent=self.panel8,
              pos=wx.Point(40, 48), size=wx.Size(60, 14), style=0)

        self.staticText49 = wx.StaticText(id=wxID_FRAME1STATICTEXT49,
              label=u'Team defense', name='staticText49', parent=self.panel8,
              pos=wx.Point(40, 120), size=wx.Size(68, 14), style=0)

        self.team7AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM7ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team7AttackSpinCtrl1',
              parent=self.panel8, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team7AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam7AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM7ATTACKSPINCTRL1)

        self.team7DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM7DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team7DefenseSpinCtrl1',
              parent=self.panel8, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team7DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam7DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM7DEFENSESPINCTRL1)

        self.staticText50 = wx.StaticText(id=wxID_FRAME1STATICTEXT50,
              label=u'Team attack', name='staticText50', parent=self.panel9,
              pos=wx.Point(40, 48), size=wx.Size(59, 14), style=0)

        self.staticText51 = wx.StaticText(id=wxID_FRAME1STATICTEXT51,
              label=u'Team defense', name='staticText51', parent=self.panel9,
              pos=wx.Point(40, 120), size=wx.Size(68, 14), style=0)

        self.team8AttackSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM8ATTACKSPINCTRL1,
              initial=0, max=255, min=0, name=u'team8AttackSpinCtrl1',
              parent=self.panel9, pos=wx.Point(48, 80), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team8AttackSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam8AttackSpinCtrl1Text,
              id=wxID_FRAME1TEAM8ATTACKSPINCTRL1)

        self.team8DefenseSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1TEAM8DEFENSESPINCTRL1,
              initial=0, max=7, min=0, name=u'team8DefenseSpinCtrl1',
              parent=self.panel9, pos=wx.Point(48, 152), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)
        self.team8DefenseSpinCtrl1.Bind(wx.EVT_TEXT,
              self.OnTeam8DefenseSpinCtrl1Text,
              id=wxID_FRAME1TEAM8DEFENSESPINCTRL1)

        self._init_coll_notebook1_Pages(self.notebook1)

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self.rom = 0
        
        self.minutes = 0
        self.seconds = 0
        
        self.superShoot = 0
        
        self.music = [0,0,0,0,0]
        
        self.Teams = 8
        self.Players = 5
        
        for i in range(1,7):
            self.choice1.Append("%d" % i)
            self.choice1.SetSelection(0)
        for i in range(1,7):
            self.choice2.Append("%d" % i)
            self.choice2.SetSelection(0)
        for i in range(1,7):
            self.choice3.Append("%d" % i)
            self.choice3.SetSelection(0)
        for i in range(1,7):
            self.choice4.Append("%d" % i)
            self.choice4.SetSelection(0)
        for i in range(1,7):
            self.choice5.Append("%d" % i)
            self.choice5.SetSelection(0)
        
        self.noPenalty = False
        
        self.teamAttack = ['' for x in range (self.Teams)]
        self.teamDefense = ['' for x in range (self.Teams)]
        
        self.sShootSelection = [['0' for x in range(self.Players)] for x in range(self.Teams)]
        self.sShootSelectionHex = [['\x00' for x in range(self.Players)] for x in range(self.Teams)]
        
        self.ShootNames = SHOOT_NAMES
        
        for name in self.ShootNames:
            self.shootTeam1Choice1.Append("%s" % name)
            self.shootTeam1Choice1.SetSelection(0)
        for name in self.ShootNames:
            self.shootTeam1Choice2.Append("%s" % name)
            self.shootTeam1Choice2.SetSelection(0)
        for name in self.ShootNames:
            self.shootTeam1Choice3.Append("%s" % name)
            self.shootTeam1Choice3.SetSelection(0)
        for name in self.ShootNames:
            self.shootTeam1Choice4.Append("%s" % name)
            self.shootTeam1Choice4.SetSelection(0)
        for name in self.ShootNames:
            self.shootTeam1Choice5.Append("%s" % name)
            self.shootTeam1Choice5.SetSelection(0)
        
        
        self.teamName =     ['' for x in range(self.Teams)]
        self.teamHexName =  ['' for x in range(self.Teams)]
        
        
        self.teamPlayerNames =      ['' for x in range(self.Teams)]
        self.teamPlayerHexNames =   ['' for x in range(self.Teams)]
        self.teamPlayerStats =      ['' for x in range(self.Teams)] 
        self.teamPlayerHexStats =   ['' for x in range(self.Teams)]
        
        for i in range(self.Teams):
            self.teamPlayerNames[i]        = ['' for x in range(self.Players)]
            self.teamPlayerHexNames[i]     = ['' for x in range(self.Players)]
            self.teamPlayerStats[i]        = [['' for x in range(6)] for x in range(5)]
            self.teamPlayerHexStats[i]     = [['' for x in range(6)] for x in range(5)]
        
        team1NameOffset = 0x0105E9
        team1StatsOffset = 0x01B3B7
        players1NameOffset = (0x0107CD, 0x0107DA, 0x0107F4, 0x010801, 0x0107E7)
        players1ShootOffset = (0x01B138, 0x01B141, 0x01B14A, 0x01B153, 0x01B15C)
        
        team2NameOffset = 0x0105F9
        team2StatsOffset = 0x01B3B9
        players2NameOffset = (0x01085C, 0x010869, 0x010876, 0x010883, 0x010890)
        players2ShootOffset = (0x01B138, 0x01B141, 0x01B14A, 0x01B153, 0x01B15C)
        
        team3NameOffset = 0x010609
        team3StatsOffset = 0x01B3BB
        players3NameOffset = (0x01089D, 0x0108AA, 0x0108B7, 0x0108C4, 0x0108D1)
        players3ShootOffset = (0x01B138, 0x01B141, 0x01B14A, 0x01B153, 0x01B15C)
        
        team4NameOffset = 0x010619
        team4StatsOffset = 0x01B3BF
        players4NameOffset = (0x01091F, 0x01092C, 0x010939, 0x010946, 0x010953)
        players4ShootOffset = (0x01B138, 0x01B141, 0x01B14A, 0x01B153, 0x01B15C)
        
        team5NameOffset = 0x010639
        team5StatsOffset = 0x01B3C1
        players5NameOffset = (0x010960, 0x01096D, 0x01097A, 0x010987, 0x010994)
        players5ShootOffset = (0x01B138, 0x01B141, 0x01B14A, 0x01B153, 0x01B15C)
        
        team6NameOffset = 0x010651
        team6StatsOffset = 0x01B3C5
        players6NameOffset = (0x0108DE, 0x0108EB, 0x0108F8, 0x010905, 0x010912)
        players6ShootOffset = (0x01B138, 0x01B141, 0x01B14A, 0x01B153, 0x01B15C)
        
        team7NameOffset = 0x010671
        team7StatsOffset = 0x01B3C7
        players7NameOffset = (0x0109A1, 0x0109AE, 0x0109BB, 0x0109C8, 0x0109D5)
        players7ShootOffset = (0x01B138, 0x01B141, 0x01B14A, 0x01B153, 0x01B15C)
        
        team8NameOffset = 0x0106a1
        team8StatsOffset = 0x01B3C9
        players8NameOffset = (0x010A64, 0x010A71, 0x010A7E, 0x010A8B, 0x010A98)
        players8ShootOffset = (0x01B138, 0x01B141, 0x01B14A, 0x01B153, 0x01B15C)
        
        self.team1 = Team(team1NameOffset, team1StatsOffset, players1NameOffset, players1ShootOffset)
        self.team2 = Team(team2NameOffset, team2StatsOffset, players2NameOffset, players2ShootOffset)
        self.team3 = Team(team3NameOffset, team3StatsOffset, players3NameOffset, players3ShootOffset)
        self.team4 = Team(team4NameOffset, team4StatsOffset, players4NameOffset, players4ShootOffset)
        self.team5 = Team(team5NameOffset, team5StatsOffset, players5NameOffset, players5ShootOffset)
        self.team6 = Team(team6NameOffset, team6StatsOffset, players6NameOffset, players6ShootOffset)
        self.team7 = Team(team7NameOffset, team7StatsOffset, players7NameOffset, players7ShootOffset)
        self.team8 = Team(team8NameOffset, team8StatsOffset, players8NameOffset, players8ShootOffset)
        
        
        
        
#-------------------------------------------------------------------------------

    def OnMinCtrl1Text(self, event):
        event.Skip()
        self.minutes = self.minCtrl1.GetValue()

    def OnSecCtrl1Text(self, event):
        event.Skip()
        self.seconds = self.secCtrl1.GetValue()

    def OnShootCtrl1Text(self, event):
        event.Skip()
        self.superShoot = self.shootCtrl1.GetValue()

    def OnChoice1Choice(self, event):
        event.Skip()
        self.music[0] = self.choice1.GetSelection()
        
    def OnChoice2Choice(self, event):
        event.Skip()
        self.music[1] = self.choice2.GetSelection()
        
    def OnChoice3Choice(self, event):
        event.Skip()
        self.music[2] = self.choice3.GetSelection()
        
    def OnChoice4Choice(self, event):
        event.Skip()
        self.music[3] = self.choice4.GetSelection()
        
    def OnChoice5Choice(self, event):
        event.Skip()
        self.music[4] = self.choice4.GetSelection()

    def OnCheckBox1Checkbox(self, event):
        event.Skip()
        self.noPenalty = self.checkBox1.GetValue()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnButton1Button(self, event):
        event.Skip()
        dlg = wx.FileDialog(self, 'Open Ike Ike Hockey ROM', '.', '', '*.nes', wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                
                self.rom = loadfile(filename, "read")
                
                # General Game Settings
                
                self.minutes , self.seconds = loadtime(self.rom)
                self.minCtrl1.SetValue("%d" % self.minutes)
                self.secCtrl1.SetValue("%2d" % self.seconds)
                
                self.superShoot = loadcharge(self.rom)
                self.shootCtrl1.SetValue("%d" % self.superShoot)
                
                self.music = loadmusic(self.rom)
                self.choice1.SetSelection(self.music[0])
                self.choice2.SetSelection(self.music[1])
                self.choice3.SetSelection(self.music[2])
                self.choice4.SetSelection(self.music[3])
                
                self.noPenalty = loadnopenalty(self.rom)
                self.checkBox1.SetValue(self.noPenalty)
                
                # Team Settings
                
                # Team 1
                
                self.teamHexName[0], self.teamPlayerHexNames[0] = self.team1.loadteam(self.rom)
                
                self.teamName[0] = hextostr(self.teamHexName[0])
                self.teamNameCtrl1.SetValue(self.teamName[0])
                
                team1Stats = self.team1.readTeamStats(self.rom)
                
                self.team1Attack = int(hexlify(team1Stats[0]), 16)
                self.team1Defense = int(hexlify(team1Stats[1]), 16)
                
                self.team1AttackSpinCtrl1.SetValue(self.team1Attack)
                self.team1DefenseSpinCtrl1.SetValue(self.team1Defense)
                
                for i in range(5):
                    self.teamPlayerNames[0][i] = hextostr(self.teamPlayerHexNames[0][i])
                
                self.team1Player1Ctrl.SetValue(self.teamPlayerNames[0][0])
                self.team1Player2Ctrl.SetValue(self.teamPlayerNames[0][1])
                self.team1Player3Ctrl.SetValue(self.teamPlayerNames[0][2])
                self.team1Player4Ctrl.SetValue(self.teamPlayerNames[0][3])
                self.team1Player5Ctrl.SetValue(self.teamPlayerNames[0][4])
                
                self.sShootSelection[0] = self.team1.sShootRead(self.rom)
                
                self.shootTeam1Choice1.SetSelection(int(self.sShootSelection[0][0]))
                self.shootTeam1Choice2.SetSelection(int(self.sShootSelection[0][1]))
                self.shootTeam1Choice3.SetSelection(int(self.sShootSelection[0][2]))
                self.shootTeam1Choice4.SetSelection(int(self.sShootSelection[0][3]))
                self.shootTeam1Choice5.SetSelection(int(self.sShootSelection[0][4]))
                
                # Team 2
                
                self.teamHexName[1], self.teamPlayerHexNames[1] = self.team2.loadteam(self.rom)
                
                self.teamName[1] = hextostr(self.teamHexName[1])
                self.teamNameCtrl2.SetValue(self.teamName[1])
                
                team2Stats = self.team2.readTeamStats(self.rom)
                
                self.team2Attack = int(hexlify(team2Stats[0]), 16)
                self.team2Defense = int(hexlify(team2Stats[1]), 16)
                
                self.team2AttackSpinCtrl1.SetValue(self.team2Attack)
                self.team2DefenseSpinCtrl1.SetValue(self.team2Defense)
                
                for i in range(5):
                    self.teamPlayerNames[1][i] = hextostr(self.teamPlayerHexNames[1][i])
                
                self.team2Player1Ctrl.SetValue(self.teamPlayerNames[1][0])
                self.team2Player2Ctrl.SetValue(self.teamPlayerNames[1][1])
                self.team2Player3Ctrl.SetValue(self.teamPlayerNames[1][2])
                self.team2Player4Ctrl.SetValue(self.teamPlayerNames[1][3])
                self.team2Player5Ctrl.SetValue(self.teamPlayerNames[1][4])
                
                # Team 3
                
                self.teamHexName[2], self.teamPlayerHexNames[2] = self.team3.loadteam(self.rom)
                
                self.teamName[2] = hextostr(self.teamHexName[2])
                self.teamNameCtrl3.SetValue(self.teamName[2])
                
                team3Stats = self.team3.readTeamStats(self.rom)
                
                self.team3Attack = int(hexlify(team3Stats[0]), 16)
                self.team3Defense = int(hexlify(team3Stats[1]), 16)
                
                self.team3AttackSpinCtrl1.SetValue(self.team3Attack)
                self.team3DefenseSpinCtrl1.SetValue(self.team3Defense)
                
                for i in range(5):
                    self.teamPlayerNames[2][i] = hextostr(self.teamPlayerHexNames[2][i])
                
                self.team3Player1Ctrl.SetValue(self.teamPlayerNames[2][0])
                self.team3Player2Ctrl.SetValue(self.teamPlayerNames[2][1])
                self.team3Player3Ctrl.SetValue(self.teamPlayerNames[2][2])
                self.team3Player4Ctrl.SetValue(self.teamPlayerNames[2][3])
                self.team3Player5Ctrl.SetValue(self.teamPlayerNames[2][4])
                
                # Team 4
                
                self.teamHexName[3], self.teamPlayerHexNames[3] = self.team4.loadteam(self.rom)
                
                self.teamName[3] = hextostr(self.teamHexName[3])
                self.teamNameCtrl4.SetValue(self.teamName[3])
                
                team4Stats = self.team4.readTeamStats(self.rom)
                
                self.team4Attack = int(hexlify(team4Stats[0]), 16)
                self.team4Defense = int(hexlify(team4Stats[1]), 16)
                
                self.team4AttackSpinCtrl1.SetValue(self.team4Attack)
                self.team4DefenseSpinCtrl1.SetValue(self.team4Defense)
                
                for i in range(5):
                    self.teamPlayerNames[3][i] = hextostr(self.teamPlayerHexNames[3][i])
                
                self.team4Player1Ctrl.SetValue(self.teamPlayerNames[3][0])
                self.team4Player2Ctrl.SetValue(self.teamPlayerNames[3][1])
                self.team4Player3Ctrl.SetValue(self.teamPlayerNames[3][2])
                self.team4Player4Ctrl.SetValue(self.teamPlayerNames[3][3])
                self.team4Player5Ctrl.SetValue(self.teamPlayerNames[3][4])
                
                # Team 5
                
                self.teamHexName[4], self.teamPlayerHexNames[4] = self.team5.loadteam(self.rom)
                
                self.teamName[4] = hextostr(self.teamHexName[4])
                self.teamNameCtrl5.SetValue(self.teamName[4])
                
                team5Stats = self.team5.readTeamStats(self.rom)
                
                self.team5Attack = int(hexlify(team5Stats[0]), 16)
                self.team5Defense = int(hexlify(team5Stats[1]), 16)
                
                self.team5AttackSpinCtrl1.SetValue(self.team5Attack)
                self.team5DefenseSpinCtrl1.SetValue(self.team5Defense)
                
                for i in range(5):
                    self.teamPlayerNames[4][i] = hextostr(self.teamPlayerHexNames[4][i])
                
                self.team5Player1Ctrl.SetValue(self.teamPlayerNames[4][0])
                self.team5Player2Ctrl.SetValue(self.teamPlayerNames[4][1])
                self.team5Player3Ctrl.SetValue(self.teamPlayerNames[4][2])
                self.team5Player4Ctrl.SetValue(self.teamPlayerNames[4][3])
                self.team5Player5Ctrl.SetValue(self.teamPlayerNames[4][4])
                
                # Team 6
                
                self.teamHexName[5], self.teamPlayerHexNames[5] = self.team6.loadteam(self.rom)
                
                self.teamName[5] = hextostr(self.teamHexName[5])
                self.teamNameCtrl6.SetValue(self.teamName[5])
                
                team6Stats = self.team6.readTeamStats(self.rom)
                
                self.team6Attack = int(hexlify(team6Stats[0]), 16)
                self.team6Defense = int(hexlify(team6Stats[1]), 16)
                
                self.team6AttackSpinCtrl1.SetValue(self.team6Attack)
                self.team6DefenseSpinCtrl1.SetValue(self.team6Defense)
                
                for i in range(5):
                    self.teamPlayerNames[5][i] = hextostr(self.teamPlayerHexNames[5][i])
                
                self.team6Player1Ctrl.SetValue(self.teamPlayerNames[5][0])
                self.team6Player2Ctrl.SetValue(self.teamPlayerNames[5][1])
                self.team6Player3Ctrl.SetValue(self.teamPlayerNames[5][2])
                self.team6Player4Ctrl.SetValue(self.teamPlayerNames[5][3])
                self.team6Player5Ctrl.SetValue(self.teamPlayerNames[5][4])
                
                # Team 7
                
                self.teamHexName[6], self.teamPlayerHexNames[6] = self.team7.loadteam(self.rom)
                
                self.teamName[6] = hextostr(self.teamHexName[6])
                self.teamNameCtrl7.SetValue(self.teamName[6])
                
                team7Stats = self.team7.readTeamStats(self.rom)
                
                self.team7Attack = int(hexlify(team7Stats[0]), 16)
                self.team7Defense = int(hexlify(team7Stats[1]), 16)
                
                self.team7AttackSpinCtrl1.SetValue(self.team7Attack)
                self.team7DefenseSpinCtrl1.SetValue(self.team7Defense)
                
                for i in range(5):
                    self.teamPlayerNames[6][i] = hextostr(self.teamPlayerHexNames[6][i])
                
                self.team7Player1Ctrl.SetValue(self.teamPlayerNames[6][0])
                self.team7Player2Ctrl.SetValue(self.teamPlayerNames[6][1])
                self.team7Player3Ctrl.SetValue(self.teamPlayerNames[6][2])
                self.team7Player4Ctrl.SetValue(self.teamPlayerNames[6][3])
                self.team7Player5Ctrl.SetValue(self.teamPlayerNames[6][4])
                
                # Team 8
                
                self.teamHexName[7], self.teamPlayerHexNames[7] = self.team8.loadteam(self.rom)
                
                self.teamName[7] = hextostr(self.teamHexName[7])
                self.teamNameCtrl8.SetValue(self.teamName[7])
                
                team8Stats = self.team8.readTeamStats(self.rom)
                
                self.team8Attack = int(hexlify(team8Stats[0]), 16)
                self.team8Defense = int(hexlify(team8Stats[1]), 16)
                
                self.team8AttackSpinCtrl1.SetValue(self.team8Attack)
                self.team8DefenseSpinCtrl1.SetValue(self.team8Defense)
                
                for i in range(5):
                    self.teamPlayerNames[7][i] = hextostr(self.teamPlayerHexNames[7][i])
                
                self.team8Player1Ctrl.SetValue(self.teamPlayerNames[7][0])
                self.team8Player2Ctrl.SetValue(self.teamPlayerNames[7][1])
                self.team8Player3Ctrl.SetValue(self.teamPlayerNames[7][2])
                self.team8Player4Ctrl.SetValue(self.teamPlayerNames[7][3])
                self.team8Player5Ctrl.SetValue(self.teamPlayerNames[7][4])
                
                closefile(self.rom)
        finally:
            dlg.Destroy()
            self.button2.Enable(True)

    def OnButton2Button(self, event):
        event.Skip()
        dlg = wx.FileDialog(self, 'Save Ike Ike Hockey ROM', '.', '', '*.nes', wx.SAVE)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                
                self.rom = loadfile(filename, "write")

                # General Game Settings
                                
                savetime(self.rom, self.minutes, self.seconds)
                savecharge(self.rom, self.superShoot)
                savemusic(self.rom, self.music)
                savenopenalty(self.rom, self.noPenalty)

                # Team Settings
                
                self.team1.saveteam(self.rom, self.teamHexName[0], self.teamPlayerHexNames[0])
                self.team2.saveteam(self.rom, self.teamHexName[1], self.teamPlayerHexNames[1])
                self.team3.saveteam(self.rom, self.teamHexName[2], self.teamPlayerHexNames[2])
                self.team4.saveteam(self.rom, self.teamHexName[3], self.teamPlayerHexNames[3])
                self.team5.saveteam(self.rom, self.teamHexName[4], self.teamPlayerHexNames[4])
                self.team6.saveteam(self.rom, self.teamHexName[5], self.teamPlayerHexNames[5])
                self.team7.saveteam(self.rom, self.teamHexName[6], self.teamPlayerHexNames[6])
                self.team8.saveteam(self.rom, self.teamHexName[7], self.teamPlayerHexNames[7])
                
                self.team1.writeTeamStats(self.rom, self.team1Attack, self.team1Defense)
                self.team2.writeTeamStats(self.rom, self.team2Attack, self.team2Defense)
                self.team3.writeTeamStats(self.rom, self.team3Attack, self.team3Defense)
                self.team4.writeTeamStats(self.rom, self.team4Attack, self.team4Defense)
                self.team5.writeTeamStats(self.rom, self.team5Attack, self.team5Defense)
                self.team6.writeTeamStats(self.rom, self.team6Attack, self.team6Defense)
                self.team7.writeTeamStats(self.rom, self.team7Attack, self.team7Defense)
                self.team8.writeTeamStats(self.rom, self.team8Attack, self.team8Defense)
                
                self.team1.sShootWrite(self.rom, self.sShootSelection[0])
                
                closefile(self.rom)
                
                
        finally:
            dlg.Destroy()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnTeamNameCtrl1Text(self, event):
        event.Skip()
        self.teamName[0] = self.teamNameCtrl1.GetValue()
        self.teamHexName[0] = strtohex(self.teamName[0])

    def OnTeam1Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[0][0] = self.team1Player1Ctrl.GetValue()
        self.teamPlayerHexNames[0][0] = strtohex(self.teamPlayerNames[0][0])

    def OnTeam1Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[0][1] = self.team1Player2Ctrl.GetValue()
        self.teamPlayerHexNames[0][1] = strtohex(self.teamPlayerNames[0][1])

    def OnTeam1Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[0][2] = self.team1Player3Ctrl.GetValue()
        self.teamPlayerHexNames[0][2] = strtohex(self.teamPlayerNames[0][2])

    def OnTeam1Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[0][3] = self.team1Player4Ctrl.GetValue()
        self.teamPlayerHexNames[0][3] = strtohex(self.teamPlayerNames[0][3])

    def OnTeam1Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[0][4] = self.team1Player5Ctrl.GetValue()
        self.teamPlayerHexNames[0][4] = strtohex(self.teamPlayerNames[0][4])

#-------------------------------------------------------------------------------

    def OnTeamNameCtrl2Text(self, event):
        event.Skip()
        self.teamName[1] = self.teamNameCtrl2.GetValue()
        self.teamHexName[1] = strtohex(self.teamName[1])

    def OnTeam2Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[1][0] = self.team2Player1Ctrl.GetValue()
        self.teamPlayerHexNames[1][0] = strtohex(self.teamPlayerNames[1][0])

    def OnTeam2Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[1][1] = self.team2Player2Ctrl.GetValue()
        self.teamPlayerHexNames[1][1] = strtohex(self.teamPlayerNames[1][1])

    def OnTeam2Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[1][2] = self.team2Player3Ctrl.GetValue()
        self.teamPlayerHexNames[1][2] = strtohex(self.teamPlayerNames[1][2])

    def OnTeam2Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[1][3] = self.team2Player4Ctrl.GetValue()
        self.teamPlayerHexNames[1][3] = strtohex(self.teamPlayerNames[1][3])

    def OnTeam2Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[1][4] = self.team2Player5Ctrl.GetValue()
        self.teamPlayerHexNames[1][4] = strtohex(self.teamPlayerNames[1][4])

#-------------------------------------------------------------------------------

    def OnTeamNameCtrl3Text(self, event):
        event.Skip()
        self.teamName[2] = self.teamNameCtrl3.GetValue()
        self.teamHexName[2] = strtohex(self.teamName[2])

    def OnTeam3Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[2][0] = self.team3Player1Ctrl.GetValue()
        self.teamPlayerHexNames[2][0] = strtohex(self.teamPlayerNames[2][0])

    def OnTeam3Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[2][1] = self.team3Player2Ctrl.GetValue()
        self.teamPlayerHexNames[2][1] = strtohex(self.teamPlayerNames[2][1])

    def OnTeam3Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[2][2] = self.team3Player3Ctrl.GetValue()
        self.teamPlayerHexNames[2][2] = strtohex(self.teamPlayerNames[2][2])

    def OnTeam3Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[2][3] = self.team3Player4Ctrl.GetValue()
        self.teamPlayerHexNames[2][3] = strtohex(self.teamPlayerNames[2][3])

    def OnTeam3Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[2][4] = self.team3Player5Ctrl.GetValue()
        self.teamPlayerHexNames[2][4] = strtohex(self.teamPlayerNames[2][4])

#-------------------------------------------------------------------------------

    def OnTeamNameCtrl4Text(self, event):
        event.Skip()
        self.teamName[3] = self.teamNameCtrl4.GetValue()
        self.teamHexName[3] = strtohex(self.teamName[3])

    def OnTeam4Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[3][0] = self.team4Player1Ctrl.GetValue()
        self.teamPlayerHexNames[3][0] = strtohex(self.teamPlayerNames[3][0])

    def OnTeam4Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[3][1] = self.team4Player2Ctrl.GetValue()
        self.teamPlayerHexNames[3][1] = strtohex(self.teamPlayerNames[3][1])

    def OnTeam4Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[3][2] = self.team4Player3Ctrl.GetValue()
        self.teamPlayerHexNames[3][2] = strtohex(self.teamPlayerNames[3][2])

    def OnTeam4Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[3][3] = self.team4Player4Ctrl.GetValue()
        self.teamPlayerHexNames[3][3] = strtohex(self.teamPlayerNames[3][3])

    def OnTeam4Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[3][4] = self.team4Player5Ctrl.GetValue()
        self.teamPlayerHexNames[3][4] = strtohex(self.teamPlayerNames[3][4])

#-------------------------------------------------------------------------------

    def OnTeamNameCtrl5Text(self, event):
        event.Skip()
        self.teamName[4] = self.teamNameCtrl5.GetValue()
        self.teamHexName[4] = strtohex(self.teamName[4])
    
    def OnTeam5Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[4][0] = self.team5Player1Ctrl.GetValue()
        self.teamPlayerHexNames[4][0] = strtohex(self.teamPlayerNames[4][0])

    def OnTeam5Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[4][1] = self.team5Player2Ctrl.GetValue()
        self.teamPlayerHexNames[4][1] = strtohex(self.teamPlayerNames[4][1])

    def OnTeam5Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[4][2] = self.team5Player3Ctrl.GetValue()
        self.teamPlayerHexNames[4][2] = strtohex(self.teamPlayerNames[4][2])

    def OnTeam5Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[4][3] = self.team5Player4Ctrl.GetValue()
        self.teamPlayerHexNames[4][3] = strtohex(self.teamPlayerNames[4][3])

    def OnTeam5Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[4][4] = self.team5Player5Ctrl.GetValue()
        self.teamPlayerHexNames[4][4] = strtohex(self.teamPlayerNames[4][4])

#-------------------------------------------------------------------------------

    def OnTeamNameCtrl6Text(self, event):
        event.Skip()
        self.teamName[5] = self.teamNameCtrl6.GetValue()
        self.teamHexName[5] = strtohex(self.teamName[5])

    def OnTeam6Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[5][0] = self.team6Player1Ctrl.GetValue()
        self.teamPlayerHexNames[5][0] = strtohex(self.teamPlayerNames[5][0])

    def OnTeam6Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[5][1] = self.team6Player2Ctrl.GetValue()
        self.teamPlayerHexNames[5][1] = strtohex(self.teamPlayerNames[5][1])

    def OnTeam6Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[5][2] = self.team6Player3Ctrl.GetValue()
        self.teamPlayerHexNames[5][2] = strtohex(self.teamPlayerNames[5][2])

    def OnTeam6Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[5][3] = self.team6Player4Ctrl.GetValue()
        self.teamPlayerHexNames[5][3] = strtohex(self.teamPlayerNames[5][3])

    def OnTeam6Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[5][4] = self.team6Player5Ctrl.GetValue()
        self.teamPlayerHexNames[5][4] = strtohex(self.teamPlayerNames[5][4])
        
#-------------------------------------------------------------------------------

    def OnTeamNameCtrl7Text(self, event):
        event.Skip()
        self.teamName[6] = self.teamNameCtrl7.GetValue()
        self.teamHexName[6] = strtohex(self.teamName[6])
        
    def OnTeam7Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[6][0] = self.team7Player1Ctrl.GetValue()
        self.teamPlayerHexNames[6][0] = strtohex(self.teamPlayerNames[6][0])

    def OnTeam7Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[6][1] = self.team7Player2Ctrl.GetValue()
        self.teamPlayerHexNames[6][1] = strtohex(self.teamPlayerNames[6][1])

    def OnTeam7Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[6][2] = self.team7Player3Ctrl.GetValue()
        self.teamPlayerHexNames[6][2] = strtohex(self.teamPlayerNames[6][2])

    def OnTeam7Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[6][3] = self.team7Player4Ctrl.GetValue()
        self.teamPlayerHexNames[6][3] = strtohex(self.teamPlayerNames[6][3])

    def OnTeam7Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[6][4] = self.team7Player5Ctrl.GetValue()
        self.teamPlayerHexNames[6][4] = strtohex(self.teamPlayerNames[6][4])
        
#-------------------------------------------------------------------------------

    def OnTeamNameCtrl8Text(self, event):
        event.Skip()
        self.teamName[7] = self.teamNameCtrl8.GetValue()
        self.teamHexName[7] = strtohex(self.teamName[7])

    def OnTeam8Player1CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[7][0] = self.team8Player1Ctrl.GetValue()
        self.teamPlayerHexNames[7][0] = strtohex(self.teamPlayerNames[7][0])

    def OnTeam8Player2CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[7][1] = self.team8Player2Ctrl.GetValue()
        self.teamPlayerHexNames[7][1] = strtohex(self.teamPlayerNames[7][1])

    def OnTeam8Player3CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[7][2] = self.team8Player3Ctrl.GetValue()
        self.teamPlayerHexNames[7][2] = strtohex(self.teamPlayerNames[7][2])

    def OnTeam8Player4CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[7][3] = self.team8Player4Ctrl.GetValue()
        self.teamPlayerHexNames[7][3] = strtohex(self.teamPlayerNames[7][3])

    def OnTeam8Player5CtrlText(self, event):
        event.Skip()
        self.teamPlayerNames[7][4] = self.team8Player5Ctrl.GetValue()
        self.teamPlayerHexNames[7][4] = strtohex(self.teamPlayerNames[7][4])

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnShootTeam1Choice1Choice(self, event):
        event.Skip()
        self.sShootSelection[0][0] = self.shootTeam1Choice1.GetSelection()

    def OnShootTeam1Choice2Choice(self, event):
        event.Skip()
        self.sShootSelection[0][1] = self.shootTeam1Choice1.GetSelection()

    def OnShootTeam1Choice3Choice(self, event):
        event.Skip()
        self.sShootSelection[0][2] = self.shootTeam1Choice1.GetSelection()

    def OnShootTeam1Choice4Choice(self, event):
        event.Skip()
        self.sShootSelection[0][3] = self.shootTeam1Choice1.GetSelection()

    def OnShootTeam1Choice5Choice(self, event):
        event.Skip()
        self.sShootSelection[0][4] = self.shootTeam1Choice1.GetSelection()

#-------------------------------------------------------------------------------

    def OnSPowerSpinTeam1Ctrl1Text(self, event):
        event.Skip()

    def OnSPowerSpinTeam1Ctrl2Text(self, event):
        event.Skip()

    def OnSPowerSpinTeam1Ctrl3Text(self, event):
        event.Skip()

    def OnSPowerSpinTeam1Ctrl4Text(self, event):
        event.Skip()

    def OnSPowerSpinTeam1Ctrl5Text(self, event):
        event.Skip()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

    def OnTeam1AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team1Attack = self.team1AttackSpinCtrl1.GetValue()
        
    def OnTeam1DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team1Defense = self.team1DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnTeam2AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team2Attack = self.team2AttackSpinCtrl1.GetValue()

    def OnTeam2DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team2Defense = self.team2DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnTeam3AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team3Attack = self.team3AttackSpinCtrl1.GetValue()

    def OnTeam3DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team3Defense = self.team3DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnTeam4AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team4Attack = self.team4AttackSpinCtrl1.GetValue()

    def OnTeam4DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team4Defense = self.team4DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnTeam5AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team5Attack = self.team5AttackSpinCtrl1.GetValue()

    def OnTeam5DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team5Defense = self.team5DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnTeam6AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team6Attack = self.team6AttackSpinCtrl1.GetValue()

    def OnTeam6DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team6Defense = self.team6DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnTeam7AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team7Attack = self.team7AttackSpinCtrl1.GetValue()

    def OnTeam7DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team7Defense = self.team7DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------

    def OnTeam8AttackSpinCtrl1Text(self, event):
        event.Skip()
        self.team8Attack = self.team8AttackSpinCtrl1.GetValue()

    def OnTeam8DefenseSpinCtrl1Text(self, event):
        event.Skip()
        self.team8Defense = self.team8DefenseSpinCtrl1.GetValue()

#-------------------------------------------------------------------------------
