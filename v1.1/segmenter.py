#!/usr/bin/python
def xstr(s):
  if s is None:
     return ''
  return s

"""
In the Week class the dates parsed are translated in week days and in 
a formatted version
"""


class Week:

   def __init__(self, startDate):
      
      self.dow = []
      startDateFormatted = datetime.datetime.strptime(startDate, "%d/%m/%Y")


      self.dow.append(startDateFormatted)
      for x in xrange(1,7):
         self.dow.append(startDateFormatted + datetime.timedelta(days=x))

   def getFormattedDate(self, unFormattedDate):

      unFormattedDateNumber = re.findall('([0-9]{1,2})', unFormattedDate, re.I)

      if len(unFormattedDateNumber) > 0:
         for d in self.dow:
            if int(d.day) == int(unFormattedDateNumber[0]):
               
               return d.strftime("%Y-%m-%d")
               
            else:
               return ""
      
"""
Concordance class is used for reading the contents of the configuration file
corresponding to a guide and storing the start date and end date
"""
class Concordance:

   def __init__(self, concordanceFile):
      
      self.configFilename = {}
      self.startDate = {}
      self.endDate = {}

      concordanceFileHandle = open( concordanceFile, "rU" )
      
      for line in concordanceFileHandle:

         barcode=re.split('\t', line)[20]

         self.configFilename[barcode] = re.split('\t', line)[25]

         self.startDate[barcode] = re.split('\t', line)[32]
         self.endDate[barcode] = re.split('\t', line)[33]
      concordanceFileHandle.close()
      
"""
In Config class a list holding the values for the data to be segmented is created. 
The values are read from the corresponding configuration file of the TV guide at hand
"""

class Config:

   def __init__(self, configFile):

      self.value = {}
      configFileHandle = open( configFile, "r" )
      for line in configFileHandle:
         if "=" in line:
            key = re.split('=| ', line.replace("\r", ""))[0]
            val = re.split('=| ', line.replace("\r", ""))[1]
            if val is '': val=0
            self.value[key] = val
            #print configFile, key, val
      configFileHandle.close()

"""
Line class is used for all lines of text as they are read from the XML input files.
Functions and variable names are self explanatory.
"""

class Line:
   'Common base class for all lines'

   def __init__(self, blockIdx):

      self.words = []
      self.blockIdx = blockIdx 
      self.fontSize = 0
      self.bold = 0

   def getFontSize(self):
      #return average fontsize
      fs=0
      for w in self.words:
         fs+=int(w.fontSize)
      self.fontSize = fs / len(self.words)
      return fs / len(self.words)


   def string(self):

      s=''
      for w in self.words:
         s+=w.text
      return s 
   
   

"""
From the list of broadcasters loaded find if a broadcaster name is mentioned in the currently examined line.
"""
   def getBroadcaster(self,bblist):

      broadcasterList=bblist

	  broadcasterList=bblist
      for bb in broadcasterList:
         b = re.search('([\(|\s]'+bb+')|^'+bb+'', self.string().lower(), re.I)
         if b is not None:
            return bb.upper()

"""
From the list of networks loaded find if a network name is mentioned in the currently examined line.
"""
   def getNet(self,netlist):

      
      netList=netlist
      for nn in netList:
         n = re.search('([\(|\s]'+nn+')|^'+nn+'', self.string().lower(), re.I)
         if n is not None:
            return nn.upper()
"""
Check if a temporal element is found in the current line. Temporal elements can have '.' or ':' as
delimiter between hours and minutes. Acceptable format is hh:mm of hh.mm where hh<24 and mm<60
"""
   def getTime(self):
      #try to find valid time in current line
      if self.getFontSize() is int(config.value['time_fs']) or int(config.value['time_fs']) is 0:
         t = re.findall('([0-9]{1,2}[.|:]{1}[0-9]{2})(?!\d)', self.string(), re.I)
         if len(t) is 1:
            if int(re.split('[.|:]', t[0])[0]) < 24 and int(re.split('[.|:]', t[0])[1]) < 60:
               return t
         elif len(t) is 2:
            if int(re.split('[.|:]', t[0])[0]) < 24 and int(re.split('[.|:]', t[0])[1]) < 60 and int(re.split('[.|:]', t[1])[0]) < 24 and int(re.split('[.|:]', t[1])[1]) < 60:
               return t

"""
Based on the read value for the expected font size of the date text we check if the current line holds date information
"""
   def getDate(self):
      date_fs_upper=int(config.value['date_fs']) + round(int(config.value['date_fs'])*0.15)
      date_fs_lower=int(config.value['date_fs']) - round(int(config.value['date_fs'])*0.15)
      #print date_fs_upper, date_fs_lower
      if self.getFontSize() <= date_fs_upper and self.getFontSize() >= date_fs_lower or int(config.value['date_fs']) is 0: 
         tags = ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag', 'zondag', 'ma', 'di', 'wo', 'do', 'vr', 'zat', 'zon', 'jan', 'feb', 'mrt', 'apr', 'mei', 'jun', 'jul', 'aug', 'sep', 'oct', 'okt', 'nov', 'dec', 'januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'october', 'oktober', 'november', 'december']
         for tag in tags:
            t = re.findall('([\s]'+tag+'[\.]?$)', self.string().lower(), re.I)
            if len(t) > 0:
               if len(self.words) < 4:
                  #print self.string()
                  #week.getFormattedDate(self.string())
                  return self.string()
               



"""
For each line actual page limits are stored.
"""        

   def getBounds(self):
      #return boundaries for this line
      
      self.l = None
      self.t = None
      self.r = None
      self.b = None

      for word in self.words:

         if word.l < self.l or self.l is None: self.l = word.l
         if word.t < self.t or self.t is None: self.t = word.t
         if word.r > self.r or self.r is None: self.r = word.r
         if word.b > self.b or self.b is None: self.b = word.b
      
         w = int(self.r) - int(self.l)
         h = int(self.b) - int(self.t)
         x = int(self.l) 
         y = int(self.t) 
      return x, y, w, h

"""
For each word text, fontsize, confidence and limits are stored.
"""    

class Word:
   'Common base class for all words'

   def __init__(self, text, fontSize, confidence, l, t, r, b):
      self.text = text
      self.confidence = confidence
      self.fontSize = fontSize
      self.l = l
      self.t = t
      self.r = r
      self.b = b
      
   def getConfidence(self):
      return self.confidence / len(self.text)

"""
The programm class contains all attributes of a TV programme record. 
Again functions are self-explained by their names
"""    

class Program:
   'Common base class for all programs'

   def __init__(self):
      self.startTime = ''
      self.stopTime = ''
      self.startTimeFormatted = ''
      self.stopTimeFormatted = ''
      self.net = ''
      self.broadcaster = ''
      self.description = []
      self.title = ''
      self.src = ''
      self.date = ''
      self.dateFormatted = ''
      self.l = None
      self.t = None
      self.r = None
      self.b = None
   
   def string(self):
      s=''
      for wl in self.description:
         s+=" "
         for w in wl:
            s+=w.text
      return s 

   def getBounds(self):
    
      for wl in self.description:
         for w in wl:

            if w.l < self.l or self.l is None: self.l = w.l
            if w.t < self.t or self.t is None: self.t = w.t
            if w.r > self.r or self.r is None: self.r = w.r
            if w.b > self.b or self.b is None: self.b = w.b
      
      w = int(self.r) - int(self.l)
      h = int(self.b) - int(self.t)
      x = int(self.l) 
      y = int(self.t) 
      
      return x, y, w, h


   def getFormattedTime(self, unFormattedTime):
      h = re.split('\.|\:', unFormattedTime)[0]
      m = re.split('\.|\:', unFormattedTime)[1]
      t = datetime.time(int(h), int(m))
      return t.strftime("%H:%M:%S")

"""
This function gets the page bounds of the programm records
"""    
def sortIndex( block ):
   l=block.get('l')
   t=block.get('t')
   r=block.get('r')
   b=block.get('b')
   w = int(r) - int(l)
   h = int(b) - int(t)
   x= int(l) + w/2 
   y= int(t) + h/2

   return (x)+(y*99)
   
"""
This function gets a list of the active broadcasters on a given date
""" 
 
def getBBlist(date):

   broadcastersL=[]
   data=open('./broadcasterList.tsv','rU') 
   tsvin = csv.reader(data, delimiter='\t')
   for row in tsvin:
      
      checkD=datetime.datetime.strptime(row[2], "%d-%m-%Y").date()
      
      if (date>=checkD):
         broadcastersL.append(row[0])
         broadcastersL.append(row[1])
   data.close()
   return broadcastersL

import os, sys
import getopt
#import xml.etree.cElementTree as ET
from lxml import etree as ET
from xml.etree.ElementTree import QName
import re
import datetime
from xml.dom import minidom
import json
import csv

"""
The input directory containing the XML output of the scanned guides is given as an argument when calling the script
""" 

print 'ARGV      :', sys.argv[1:]

options, remainder = getopt.getopt(sys.argv[1:], 'i:v', ['inputdir=' 
                                 
                                                         ])
print 'OPTIONS   :', options

for opt, arg in options:
    if opt in ('-i', '--inputdir'):
        inputdir = arg

"""
The list of network channels is loaded from an external file
"""    
networks=[]
data=open('./networksList.tsv','rU') 
tsvin = csv.reader(data, delimiter='\t')
for row in tsvin:
   networks.append(row[0])
data.close()


"""
Method for CSV output of the segmented programme information
""" 
def writeCsv( programList ):
   for p in programList:
      file = open(bn+".csv", "a")
      json.dump(p,sys.stdout)
      if len(p.string()) < 2000:
         file.write(p.startTime)
         file.write(";")
         file.write(p.stopTime)
         file.write(";")
         file.write(p.net)
         file.write(";")
         file.write(p.broadcaster)
         file.write(";")
         file.write(p.string().encode("utf8"))
         file.write("\n")
         file.close()           

"""
Method for XML output of the segmented programme information
""" 
def writeXml( p ):
   for p in programList:
      if len(p.string()) < 2000:
         program = ET.SubElement(root, 'program')
         program.set('x', str(p.getBounds()[0]))
         program.set('y', str(p.getBounds()[1]))
         program.set('w', str(p.getBounds()[2]))
         program.set('h', str(p.getBounds()[3]))
         
         os.path.basename(inputdir)
   
         src = ET.SubElement(program, 'source')
         src.text = p.src
   
         date = ET.SubElement(program, 'date')
         date.text = p.date
      
         dateFormatted = ET.SubElement(program, 'dateFormatted')
         dateFormatted.text = p.dateFormatted

         startTime = ET.SubElement(program, 'startTime')
         startTime.text = p.startTime

         startTimeFormatted = ET.SubElement(program, 'startTimeFormatted')
         startTimeFormatted.text = p.startTimeFormatted
         
         stopTime = ET.SubElement(program, 'stopTime')
         stopTime.text = p.stopTime

         stopTimeFormatted = ET.SubElement(program, 'stopTimeFormatted')
         stopTimeFormatted.text = p.stopTimeFormatted
      
         net = ET.SubElement(program, 'net')
         net.text = p.net
      
         broadcaster = ET.SubElement(program, 'broadcaster')
         broadcaster.text = p.broadcaster
      
         description = ET.SubElement(program, 'desc')
         towrite=p.string().encode('ascii', 'ignore').replace(startTime.text,"")
         towrite=towrite.replace(stopTime.text, "")
         description.text = towrite
         
root = ET.Element('programs')
root.set('version', '1.0')

d=''

"""
Concordance file has a list of the corresponcence between guide barcode and assigned configuration file
""" 
#concordance = Concordance("../Config files per barcode - CoMeRDa gidsen 2012 - Gidsniveau.tsv")
concordance = Concordance("../Test_Descriptive1.txt")


for fsroot, dirs, filenames in os.walk(inputdir):   #loop all xml's (feed the script with one dir where all XMLs are found)
   filenames.sort()
   root = ET.Element('programs')
   root.set('version', '1.0')
   bn=bn_before=""
   broads=[]
   
"""
For every file in the directory the part before '_' in the filename is considered to be the file barcode.
Based on this barcode the start-date and end-date of the programmes described in the guide are read and parsed
from the additional files.

"""

   for f in filenames:
      if str(f) != ".DS_Store" :
         bn_before=bn

         bn=str(f).split("_")[0]
         if bn_before=="":
            broads=getBBlist(datetime.datetime.strptime(str(concordance.startDate[bn]),"%d/%m/%Y").date())
         else:
            if (bn_before!=bn):
               broads=getBBlist(datetime.datetime.strptime(str(concordance.startDate[bn]),"%d/%m/%Y").date())
               root.clear()
               d=""
               
         root.set('startDate', concordance.startDate[bn]) 
         root.set('endDate', concordance.endDate[bn]) 
         check1=datetime.datetime.strptime(str(concordance.startDate[bn]),"%d/%m/%Y")
         check2=datetime.datetime.strptime(concordance.endDate[bn],"%d/%m/%Y")
         check1= check1.date()
         check2= check2.date()
         
         week = Week(concordance.startDate[bn])
         
"""
For the active guide being segmented a configuration file is loaded. If there is no configuration file
then a generic configuration file is used.

"""
         if os.path.exists("../configs/"+concordance.configFilename[bn]+".txt"):
            config = Config("../configs/"+concordance.configFilename[bn]+".txt") #load configfile    
         else:
            config = Config("../configs/empty_config_file.txt") #load configfile
         


         dir(config)        
         ff = str(inputdir + "/" + str(f))
         tree = ET.parse(ff)
         doc = tree.getroot()
         
         namespace = 'http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml'
         
         lineList = []
         wordList = []
         
         word = ''
         confidence=word_l=word_t=word_r=word_b=None
         
"""
The XML output file is loaded in a tree form list. 
This tree form is made up of blocks,that are made up of lines, that are made up of words, 
that are made up of characters. 

""" 

         for block in doc.iter(str( QName( namespace, 'block' ) )):
            for line in block.iter(str( QName( namespace, 'line' ) )):
               lineobj = Line(sortIndex(block))
               for formatting in line.iter(str( QName( namespace, 'formatting' ) )):
                  for c in formatting.iter(str( QName( namespace, 'charParams' ) )):  #loop throug all characters
                     
"""
First step is making up words out of the characters.

"""         
                     if c.get('wordStart') == '1':       #make a wordobject and add it to the lineobject
                        if word is not '': lineobj.words.append(Word(word, formatting.get('fs'), confidence, word_l, word_t, word_r, word_b))
                        if c.get('charConfidence') is not None: confidence=int(c.get('charConfidence'))
                        word_l=int(c.get('l'))
                        word_t=int(c.get('t'))
                        word_r=int(c.get('r'))
                        word_b=int(c.get('b'))
                        word=xstr(c.text)
                     else:
                        if c.get('charConfidence') is not None: confidence+=int(c.get('charConfidence'))
                        if c.get('l') < word_l: word_l=int(c.get('l'))
                        if c.get('t') < word_t: word_t=int(c.get('t'))
                        if c.get('r') > word_r: word_r=int(c.get('r'))
                        if c.get('b') > word_b: word_b=int(c.get('b'))
                        word+=xstr(c.text)
               
               if word is not '': lineobj.words.append(Word(word, formatting.get('fs'), confidence, word_l, word_t, word_r, word_b))
               word=''
"""
The words make up a line which is then added to a linelist (a list of line objects)

"""               
               lineList.append(lineobj)   
         
         programList = []

         b=n=t=''
         
"""
Each line object is checked for date elements, network names, broadcaster names, and time elements
All the words remaining are considered to be the description of a programme.
"""          
         for l in lineList: 
            if l.getDate() is not None: d=l.getDate() 

         for l in lineList: 

            if l.getNet(networks) is not None: n=l.getNet(networks)
            if l.getBroadcaster(broads) is not None: b=l.getBroadcaster(broads)
            
            if l.getTime() > 0:
               try:
                  programList.append(programobj) 
               except:
                  foo = 'bar'
               programobj = Program()
               programobj.src = os.path.basename(ff)

               if len(l.getTime()) is 1:
                  programobj.startTime = l.getTime()[0]
                  programobj.startTimeFormatted = programobj.getFormattedTime(l.getTime()[0])
               elif len(l.getTime()) is 2:
                  programobj.startTime = l.getTime()[0]
                  programobj.startTimeFormatted = programobj.getFormattedTime(l.getTime()[0])
                  programobj.stopTime = l.getTime()[1]
                  programobj.stopTimeFormatted = programobj.getFormattedTime(l.getTime()[1])

               programobj.net = n
               programobj.broadcaster = b
               programobj.date = d
               programobj.dateFormatted = week.getFormattedDate(d)
               programobj.description.append(l.words)

            else:
               try:
                  programobj.description.append(l.words)
               except:
                  programobj = Program()
                  programobj.description.append(l.words)

         try:
            programList.append(programobj)
            writeXml(programList)
         except:
            foo='bar'
            
"""
The found segmented programmes are written to an XML file.
"""  
            
         xml = ET.tostring(root,encoding='utf8', pretty_print=True)
         fp = open("./results/"+bn+".xml", "w")
         fp.write(xml)
         fp.close()
 
