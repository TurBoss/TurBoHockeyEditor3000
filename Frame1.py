#Boa:Frame:Frame1

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

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
    music = [0,0,0,0]
    rom.seek(0x01D8DC)
    musics = rom.read(4)
    
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
    
    musicHex = ["\x00", "\x00", "\x00", "\x00"]
    
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
# Teams

class Team(object):
    
    def __init__(self, teamNameOffset, playersNameOffset):
        self.teamNameOffset = teamNameOffset
        self.playerNameOffset = playersNameOffset
    
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

[wxID_FRAME1, wxID_FRAME1ANGRYSPINCTRL1, wxID_FRAME1ANGRYSPINCTRL2, 
 wxID_FRAME1ANGRYSPINCTRL3, wxID_FRAME1ANGRYSPINCTRL4, 
 wxID_FRAME1ANGRYSPINCTRL5, wxID_FRAME1BUTTON1, wxID_FRAME1BUTTON2, 
 wxID_FRAME1CHECKBOX1, wxID_FRAME1CHOICE1, wxID_FRAME1CHOICE2, 
 wxID_FRAME1CHOICE3, wxID_FRAME1CHOICE4, wxID_FRAME1MINCTRL1, 
 wxID_FRAME1MPOWERSPINCTRL1, wxID_FRAME1MPOWERSPINCTRL2, 
 wxID_FRAME1MPOWERSPINCTRL3, wxID_FRAME1MPOWERSPINCTRL4, 
 wxID_FRAME1MPOWERSPINCTRL5, wxID_FRAME1NOTEBOOK1, wxID_FRAME1PANEL1, 
 wxID_FRAME1PANEL10, wxID_FRAME1PANEL11, wxID_FRAME1PANEL12, 
 wxID_FRAME1PANEL2, wxID_FRAME1PANEL3, wxID_FRAME1PANEL4, wxID_FRAME1PANEL5, 
 wxID_FRAME1PANEL6, wxID_FRAME1PANEL7, wxID_FRAME1PANEL8, wxID_FRAME1PANEL9, 
 wxID_FRAME1SECCTRL1, wxID_FRAME1SHOOTCTRL1, wxID_FRAME1SHOOTTEAM1CHOICE1, 
 wxID_FRAME1SHOOTTEAM1CHOICE2, wxID_FRAME1SHOOTTEAM1CHOICE3, 
 wxID_FRAME1SHOOTTEAM1CHOICE4, wxID_FRAME1SHOOTTEAM1CHOICE5, 
 wxID_FRAME1SPEEDSPINCTRL1, wxID_FRAME1SPEEDSPINCTRL2, 
 wxID_FRAME1SPEEDSPINCTRL3, wxID_FRAME1SPEEDSPINCTRL4, 
 wxID_FRAME1SPEEDSPINCTRL5, wxID_FRAME1SPOWERSPINCTRL1, 
 wxID_FRAME1SPOWERSPINCTRL2, wxID_FRAME1SPOWERSPINCTRL3, 
 wxID_FRAME1SPOWERSPINCTRL4, wxID_FRAME1SPOWERSPINCTRL5, 
 wxID_FRAME1STATICTEXT1, wxID_FRAME1STATICTEXT10, wxID_FRAME1STATICTEXT11, 
 wxID_FRAME1STATICTEXT12, wxID_FRAME1STATICTEXT13, wxID_FRAME1STATICTEXT14, 
 wxID_FRAME1STATICTEXT15, wxID_FRAME1STATICTEXT16, wxID_FRAME1STATICTEXT17, 
 wxID_FRAME1STATICTEXT18, wxID_FRAME1STATICTEXT19, wxID_FRAME1STATICTEXT2, 
 wxID_FRAME1STATICTEXT20, wxID_FRAME1STATICTEXT22, wxID_FRAME1STATICTEXT23, 
 wxID_FRAME1STATICTEXT24, wxID_FRAME1STATICTEXT25, wxID_FRAME1STATICTEXT3, 
 wxID_FRAME1STATICTEXT4, wxID_FRAME1STATICTEXT5, wxID_FRAME1STATICTEXT6, 
 wxID_FRAME1STATICTEXT7, wxID_FRAME1STATICTEXT8, wxID_FRAME1STATICTEXT9, 
 wxID_FRAME1TEAM1PLAYER1CTRL, wxID_FRAME1TEAM1PLAYER2CTRL, 
 wxID_FRAME1TEAM1PLAYER3CTRL, wxID_FRAME1TEAM1PLAYER4CTRL, 
 wxID_FRAME1TEAM1PLAYER5CTRL, wxID_FRAME1TEAM2PLAYER1CTRL, 
 wxID_FRAME1TEAM2PLAYER2CTRL, wxID_FRAME1TEAM2PLAYER3CTRL, 
 wxID_FRAME1TEAM2PLAYER4CTRL, wxID_FRAME1TEAM2PLAYER5CTRL, 
 wxID_FRAME1TEAM3PLAYER1CTRL, wxID_FRAME1TEAM3PLAYER2CTRL, 
 wxID_FRAME1TEAM3PLAYER3CTRL, wxID_FRAME1TEAM3PLAYER4CTRL, 
 wxID_FRAME1TEAM3PLAYER5CTRL, wxID_FRAME1TEAMNAMECTRL1, 
 wxID_FRAME1TEAMNAMECTRL2, wxID_FRAME1TEAMNAMECTRL3, 
 wxID_FRAME1WEIGHTSPINCTRL1, wxID_FRAME1WEIGHTSPINCTRL2, 
 wxID_FRAME1WEIGHTSPINCTRL3, wxID_FRAME1WEIGHTSPINCTRL4, 
 wxID_FRAME1WEIGHTSPINCTRL5, 
] = [wx.NewId() for _init_ctrls in range(96)]

class Frame1(wx.Frame):
    def _init_coll_notebook1_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.panel2, select=True,
              text=u'Team 1')
        parent.AddPage(imageId=-1, page=self.panel3, select=False,
              text=u'Team 2')
        parent.AddPage(imageId=-1, page=self.panel4, select=False,
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
        parent.AddPage(imageId=-1, page=self.panel10, select=False,
              text=u'Team 9')
        parent.AddPage(imageId=-1, page=self.panel11, select=False,
              text=u'Team 10')
        parent.AddPage(imageId=-1, page=self.panel12, select=False,
              text=u'Team 11')

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(331, 286), size=wx.Size(845, 425),
              style=wx.DEFAULT_FRAME_STYLE, title=u'TurBo Hockey Editor 3000')
        self.SetClientSize(wx.Size(837, 398))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(837, 398),
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
              pos=wx.Point(120, 24), size=wx.Size(60, 14), style=0)

        self.shootCtrl1 = wx.TextCtrl(id=wxID_FRAME1SHOOTCTRL1,
              name=u'shootCtrl1', parent=self.panel1, pos=wx.Point(136, 40),
              size=wx.Size(32, 21), style=0, value=u'0')
        self.shootCtrl1.SetLabelText(u'0')
        self.shootCtrl1.SetToolTipString(u'Super shoot time')
        self.shootCtrl1.SetMaxLength(3)
        self.shootCtrl1.Bind(wx.EVT_TEXT, self.OnShootCtrl1Text,
              id=wxID_FRAME1SHOOTCTRL1)

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label=u'Field 1', name='staticText3', parent=self.panel1,
              pos=wx.Point(200, 24), size=wx.Size(31, 14), style=0)

        self.staticText4 = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label=u'Field 2', name='staticText4', parent=self.panel1,
              pos=wx.Point(264, 24), size=wx.Size(31, 14), style=0)

        self.staticText5 = wx.StaticText(id=wxID_FRAME1STATICTEXT5,
              label=u'Field 3', name='staticText5', parent=self.panel1,
              pos=wx.Point(328, 24), size=wx.Size(31, 14), style=0)

        self.staticText6 = wx.StaticText(id=wxID_FRAME1STATICTEXT6,
              label=u'Field 4', name='staticText6', parent=self.panel1,
              pos=wx.Point(392, 24), size=wx.Size(31, 14), style=0)

        self.choice1 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE1,
              name='choice1', parent=self.panel1, pos=wx.Point(192, 40),
              size=wx.Size(48, 21), style=0)
        self.choice1.SetToolTipString(u'Field 1 music theme')
        self.choice1.Bind(wx.EVT_CHOICE, self.OnChoice1Choice,
              id=wxID_FRAME1CHOICE1)

        self.choice2 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE2,
              name='choice2', parent=self.panel1, pos=wx.Point(256, 40),
              size=wx.Size(48, 21), style=0)
        self.choice2.SetToolTipString(u'Field 2 music theme')
        self.choice2.Bind(wx.EVT_CHOICE, self.OnChoice2Choice,
              id=wxID_FRAME1CHOICE2)

        self.choice3 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE3,
              name='choice3', parent=self.panel1, pos=wx.Point(320, 40),
              size=wx.Size(48, 21), style=0)
        self.choice3.SetToolTipString(u'Field 3 music theme')
        self.choice3.Bind(wx.EVT_CHOICE, self.OnChoice3Choice,
              id=wxID_FRAME1CHOICE3)

        self.choice4 = wx.Choice(choices=[], id=wxID_FRAME1CHOICE4,
              name='choice4', parent=self.panel1, pos=wx.Point(384, 40),
              size=wx.Size(48, 21), style=0)
        self.choice4.SetToolTipString(u'Field 4 music theme')
        self.choice4.Bind(wx.EVT_CHOICE, self.OnChoice4Choice,
              id=wxID_FRAME1CHOICE4)

        self.staticText7 = wx.StaticText(id=wxID_FRAME1STATICTEXT7,
              label=u'Music', name='staticText7', parent=self.panel1,
              pos=wx.Point(296, 8), size=wx.Size(26, 14), style=0)

        self.checkBox1 = wx.CheckBox(id=wxID_FRAME1CHECKBOX1,
              label=u'No Penalty', name='checkBox1', parent=self.panel1,
              pos=wx.Point(464, 40), size=wx.Size(70, 13), style=0)
        self.checkBox1.SetValue(False)
        self.checkBox1.SetToolTipString(u'Enable / Disable penalty')
        self.checkBox1.Bind(wx.EVT_CHECKBOX, self.OnCheckBox1Checkbox,
              id=wxID_FRAME1CHECKBOX1)

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label=u'Load',
              name='button1', parent=self.panel1, pos=wx.Point(632, 8),
              size=wx.Size(75, 23), style=0)
        self.button1.SetToolTipString(u'Load rom')
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME1BUTTON1)

        self.button2 = wx.Button(id=wxID_FRAME1BUTTON2, label=u'Save',
              name='button2', parent=self.panel1, pos=wx.Point(632, 40),
              size=wx.Size(75, 23), style=0)
        self.button2.SetToolTipString(u'Save rom')
        self.button2.Enable(False)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button,
              id=wxID_FRAME1BUTTON2)

        self.notebook1 = wx.Notebook(id=wxID_FRAME1NOTEBOOK1, name='notebook1',
              parent=self.panel1, pos=wx.Point(8, 72), size=wx.Size(824, 320),
              style=0)
        self.notebook1.SetToolTipString(u'')

        self.panel12 = wx.Panel(id=wxID_FRAME1PANEL12, name='panel12',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(816, 294),
              style=wx.TAB_TRAVERSAL)

        self.panel10 = wx.Panel(id=wxID_FRAME1PANEL10, name='panel10',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(816, 294),
              style=wx.TAB_TRAVERSAL)

        self.panel11 = wx.Panel(id=wxID_FRAME1PANEL11, name='panel11',
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(816, 294),
              style=wx.TAB_TRAVERSAL)

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

        self.sPowerSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINCTRL1,
              initial=1, max=5, min=1, name=u'sPowerSpinCtrl1',
              parent=self.panel2, pos=wx.Point(240, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

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

        self.mPowerSpinCtrl4 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINCTRL4,
              initial=1, max=5, min=1, name=u'mPowerSpinCtrl4',
              parent=self.panel2, pos=wx.Point(328, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.mPowerSpinCtrl5 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINCTRL5,
              initial=1, max=5, min=1, name=u'mPowerSpinCtrl5',
              parent=self.panel2, pos=wx.Point(328, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.mPowerSpinCtrl2 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINCTRL2,
              initial=1, max=5, min=1, name=u'mPowerSpinCtrl2',
              parent=self.panel2, pos=wx.Point(328, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.mPowerSpinCtrl3 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINCTRL3,
              initial=1, max=5, min=1, name=u'mPowerSpinCtrl3',
              parent=self.panel2, pos=wx.Point(328, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.mPowerSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1MPOWERSPINCTRL1,
              initial=1, max=5, min=1, name=u'mPowerSpinCtrl1',
              parent=self.panel2, pos=wx.Point(328, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.weightSpinCtrl4 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINCTRL4,
              initial=1, max=5, min=1, name=u'weightSpinCtrl4',
              parent=self.panel2, pos=wx.Point(464, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.weightSpinCtrl5 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINCTRL5,
              initial=1, max=5, min=1, name=u'weightSpinCtrl5',
              parent=self.panel2, pos=wx.Point(464, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.weightSpinCtrl2 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINCTRL2,
              initial=1, max=5, min=1, name=u'weightSpinCtrl2',
              parent=self.panel2, pos=wx.Point(464, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.weightSpinCtrl3 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINCTRL3,
              initial=1, max=5, min=1, name=u'weightSpinCtrl3',
              parent=self.panel2, pos=wx.Point(464, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.weightSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1WEIGHTSPINCTRL1,
              initial=1, max=5, min=1, name=u'weightSpinCtrl1',
              parent=self.panel2, pos=wx.Point(464, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.sPowerSpinCtrl4 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINCTRL4,
              initial=1, max=5, min=1, name=u'sPowerSpinCtrl4',
              parent=self.panel2, pos=wx.Point(240, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.sPowerSpinCtrl5 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINCTRL5,
              initial=1, max=5, min=1, name=u'sPowerSpinCtrl5',
              parent=self.panel2, pos=wx.Point(240, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.sPowerSpinCtrl2 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINCTRL2,
              initial=1, max=5, min=1, name=u'sPowerSpinCtrl2',
              parent=self.panel2, pos=wx.Point(240, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.staticText9 = wx.StaticText(id=wxID_FRAME1STATICTEXT9,
              label=u'Name', name='staticText9', parent=self.panel2,
              pos=wx.Point(144, 48), size=wx.Size(27, 14), style=0)

        self.speedSpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINCTRL1,
              initial=1, max=3, min=1, name=u'speedSpinCtrl1',
              parent=self.panel2, pos=wx.Point(400, 64), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.speedSpinCtrl2 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINCTRL2,
              initial=1, max=3, min=1, name=u'speedSpinCtrl2',
              parent=self.panel2, pos=wx.Point(400, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.speedSpinCtrl3 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINCTRL3,
              initial=1, max=3, min=1, name=u'speedSpinCtrl3',
              parent=self.panel2, pos=wx.Point(400, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.speedSpinCtrl4 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINCTRL4,
              initial=1, max=3, min=1, name=u'speedSpinCtrl4',
              parent=self.panel2, pos=wx.Point(400, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.speedSpinCtrl5 = wx.SpinCtrl(id=wxID_FRAME1SPEEDSPINCTRL5,
              initial=1, max=3, min=1, name=u'speedSpinCtrl5',
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

        self.sPowerSpinCtrl3 = wx.SpinCtrl(id=wxID_FRAME1SPOWERSPINCTRL3,
              initial=1, max=5, min=1, name=u'sPowerSpinCtrl3',
              parent=self.panel2, pos=wx.Point(240, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.staticText10 = wx.StaticText(id=wxID_FRAME1STATICTEXT10,
              label=u'Start Power', name='staticText10', parent=self.panel2,
              pos=wx.Point(240, 32), size=wx.Size(57, 14), style=0)

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
              pos=wx.Point(616, 32), size=wx.Size(58, 14), style=0)

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

        self.angrySpinCtrl4 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINCTRL4,
              initial=1, max=7, min=1, name=u'angrySpinCtrl4',
              parent=self.panel2, pos=wx.Point(536, 160), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.angrySpinCtrl5 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINCTRL5,
              initial=1, max=7, min=1, name=u'angrySpinCtrl5',
              parent=self.panel2, pos=wx.Point(536, 192), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.angrySpinCtrl2 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINCTRL2,
              initial=1, max=7, min=1, name=u'angrySpinCtrl2',
              parent=self.panel2, pos=wx.Point(536, 96), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.angrySpinCtrl3 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINCTRL3,
              initial=1, max=7, min=1, name=u'angrySpinCtrl3',
              parent=self.panel2, pos=wx.Point(536, 128), size=wx.Size(48, 21),
              style=wx.SP_ARROW_KEYS)

        self.angrySpinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1ANGRYSPINCTRL1,
              initial=1, max=7, min=1, name=u'angrySpinCtrl1',
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
              parent=self.panel2, pos=wx.Point(600, 64), size=wx.Size(106, 21),
              style=0)
        self.shootTeam1Choice1.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice1Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE1)

        self.shootTeam1Choice2 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM1CHOICE2, name=u'shootTeam1Choice2',
              parent=self.panel2, pos=wx.Point(600, 96), size=wx.Size(106, 21),
              style=0)
        self.shootTeam1Choice2.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice2Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE2)

        self.shootTeam1Choice3 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM1CHOICE3, name=u'shootTeam1Choice3',
              parent=self.panel2, pos=wx.Point(600, 128), size=wx.Size(106, 21),
              style=0)
        self.shootTeam1Choice3.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice3Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE3)

        self.shootTeam1Choice4 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM1CHOICE4, name=u'shootTeam1Choice4',
              parent=self.panel2, pos=wx.Point(600, 160), size=wx.Size(106, 21),
              style=0)
        self.shootTeam1Choice4.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice4Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE4)

        self.shootTeam1Choice5 = wx.Choice(choices=[],
              id=wxID_FRAME1SHOOTTEAM1CHOICE5, name=u'shootTeam1Choice5',
              parent=self.panel2, pos=wx.Point(600, 192), size=wx.Size(106, 21),
              style=0)
        self.shootTeam1Choice5.Bind(wx.EVT_CHOICE,
              self.OnShootTeam1Choice5Choice, id=wxID_FRAME1SHOOTTEAM1CHOICE5)

        self._init_coll_notebook1_Pages(self.notebook1)

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self.rom = 0
        
        self.minutes = 0
        self.seconds = 0
        
        self.superShoot = 0
        
        self.music = [0,0,0,0]
        
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
        
        self.noPenalty = False
        
        self.sShootSelection = [[0 for x in range(5)] for x in range(11)]
        
        self.ShootNames = (
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
                        "COMO SI FUESE 00 (TODOS IGUAL LOS SIGUIENTES)",
                        "SIN ESPECIAL"
                        )
        
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
        
        
        self.teamName =     ['' for x in range(11)]
        self.teamHexName =  ['' for x in range(11)]
        
        self.Teams = 11
        
        self.teamPlayerNames =      ['' for x in range(self.Teams)]
        self.teamPlayerHexNames =   ['' for x in range(self.Teams)]
        self.teamPlayerStats =      ['' for x in range(self.Teams)] 
        self.teamPlayerHexStats =   ['' for x in range(self.Teams)]
        
        for i in range(self.Teams):
            self.teamPlayerNames[i]        = ['' for x in range(5)]
            self.teamPlayerHexNames[i]     = ['' for x in range(5)]
            self.teamPlayerStats[i]        = [['' for x in range(6)] for x in range(5)]
            self.teamPlayerHexStats[i]     = [['' for x in range(6)] for x in range(5)]
        
        team1NameOffset = 0x0105E9
        players1NameOffset = (0x0107CD, 0x0107DA, 0x0107F4, 0x010801, 0x0107E7)
        
        team2NameOffset = 0x0105F9
        players2NameOffset = (0x01085C, 0x010869, 0x010876, 0x010883, 0x010890)
        
        team3NameOffset = 0x010609
        players3NameOffset = (0x01089D, 0x0108AA, 0x0108B7, 0x0108C4, 0x0108D1)
        
        self.team1 = Team(team1NameOffset,players1NameOffset)
        self.team2 = Team(team2NameOffset,players2NameOffset)
        self.team3 = Team(team3NameOffset,players3NameOffset)

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

    def OnCheckBox1Checkbox(self, event):
        event.Skip()
        self.noPenalty = self.checkBox1.GetValue()

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
                
                for i in range(5):
                    self.teamPlayerNames[0][i] = hextostr(self.teamPlayerHexNames[0][i])
                
                self.team1Player1Ctrl.SetValue(self.teamPlayerNames[0][0])
                self.team1Player2Ctrl.SetValue(self.teamPlayerNames[0][1])
                self.team1Player3Ctrl.SetValue(self.teamPlayerNames[0][2])
                self.team1Player4Ctrl.SetValue(self.teamPlayerNames[0][3])
                self.team1Player5Ctrl.SetValue(self.teamPlayerNames[0][4])
                
                # Team 2
                
                self.teamHexName[1], self.teamPlayerHexNames[1] = self.team2.loadteam(self.rom)
                
                self.teamName[1] = hextostr(self.teamHexName[1])
                self.teamNameCtrl2.SetValue(self.teamName[1])
                
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
                
                for i in range(5):
                    self.teamPlayerNames[2][i] = hextostr(self.teamPlayerHexNames[2][i])
                
                self.team3Player1Ctrl.SetValue(self.teamPlayerNames[2][0])
                self.team3Player2Ctrl.SetValue(self.teamPlayerNames[2][1])
                self.team3Player3Ctrl.SetValue(self.teamPlayerNames[2][2])
                self.team3Player4Ctrl.SetValue(self.teamPlayerNames[2][3])
                self.team3Player5Ctrl.SetValue(self.teamPlayerNames[2][4])
                
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
                
                closefile(self.rom)
                
                
        finally:
            dlg.Destroy()

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

    def OnShootTeam1Choice1Choice(self, event):
        event.Skip()
        self.sShootSelection[0][0] = self.shootTeam1Choice1.GetSelection()

    def OnShootTeam1Choice2Choice(self, event):
        event.Skip()
        self.sShootSelection[0][1] = self.shootTeam1Choice1.GetSelection()

    def OnShootTeam1Choice4Choice(self, event):
        event.Skip()
        self.sShootSelection[0][2] = self.shootTeam1Choice1.GetSelection()

    def OnShootTeam1Choice3Choice(self, event):
        event.Skip()
        self.sShootSelection[0][3] = self.shootTeam1Choice1.GetSelection()

    def OnShootTeam1Choice5Choice(self, event):
        event.Skip()
        self.sShootSelection[0][4] = self.shootTeam1Choice1.GetSelection()
