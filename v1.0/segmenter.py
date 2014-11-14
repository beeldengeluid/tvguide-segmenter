#!/usr/bin/python
def xstr(s):
  if s is None:
     return ''
  return s

class Week:

   def __init__(self, startDate):
      
      self.dow = []
      startDateFormatted = datetime.datetime.strptime(startDate, "%d-%m-%Y")
      #self.endDateFormatted = startDateFormatted + datetime.timedelta(days=6)

      self.dow.append(startDateFormatted)
      for x in xrange(1,7):
         self.dow.append(startDateFormatted + datetime.timedelta(days=x))

   def getFormattedDate(self, unFormattedDate):

      unFormattedDateNumber = re.findall('([0-9]{1,2})', unFormattedDate, re.I)

      if len(unFormattedDateNumber) > 0:
         for d in self.dow:
            if int(d.day) == int(unFormattedDateNumber[0]):
               #print d
               return d.strftime("%Y-%m-%d")
               #print unFormattedDateNumber[0]
      
      #for d in self.dow:
      #   print d

class Concordance:

   def __init__(self, concordanceFile):
      
      self.configFilename = {}
      self.startDate = {}
      self.endDate = {}

      concordanceFileHandle = open( concordanceFile, "r" )
      
      for line in concordanceFileHandle:
         barcode=re.split('\t', line)[20]
         self.configFilename[barcode] = re.split('\t', line)[25]
         self.startDate[barcode] = re.split('\t', line)[32]
         self.endDate[barcode] = re.split('\t', line)[33]
      concordanceFileHandle.close()

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
            print configFile, key, val
      configFileHandle.close()
      

class Line:
   'Common base class for all lines'

   def __init__(self, blockIdx):
      #self.baseline = baseline
      self.words = []
      #self.fontSize = fontSize 
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

#  def getBold(self):
#     #return wether line contains bold
#     bold=0
#     for w in self.words:
#        if int(w.bold) == 1
#           bold=1            
#     return bold


   def string(self):
      #return the whole line.
      s=''
      for w in self.words:
         s+=w.text
      return s 

   def getBroadcaster(self):
      #try to get broadcaster from a list. TODO: load the list via cmdline arguments.

      broadcasterList = ['NOS','AVRO','VARA','NCRV','KRO','VPRO','KRO/RKK','NOS/NOT','ROF','TELEAC','HV']
      #score = process.extractOne(self.string(), broadcasterList)
      #print "%", b, score
      #if score[1] > 89: 
      #      return score[0]
       #  score = fuzz.token_set_ratio(self.string(), b)
         #if score > 80:
         #print '# ',self.string(), b, score
        # return b

      for bb in broadcasterList:
         b = re.search('([\(|\s]'+bb+')|^'+bb+'', self.string(), re.I)
         if b is not None:
            return bb

   def getNet(self):
      #try to find net in current line

      netList = ['NEDERLAND 1','NEDERLAND 2','NEDERLAND 3','HILVERSUM 1']

      for nn in netList:
         n = re.search('([\(|\s]'+nn+')|^'+nn+'', self.string(), re.I)
         if n is not None:
            return nn

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
               

      #   if self.getFontSize() is int(config.value['date_bold']) or int(config.value['date_bold']) is 0: 

      #   months = ['jan', 'feb', 'mrt', 'apr', 'mei', 'jun', 'jul', 'aug', 'sep', 'okt', 'oct', 'nov', 'dec']
      #   for month in months:
      #      mu = month.upper()
      #      ml = month.lower()
      #      d = re.findall('([0-9]{1,2}[\s]'+mu+'[.])', self.string(), re.I)
      #      #d = re.findall('([0-9]{1,2}[\s]'+ml+'[.])', self.string(), re.I)
      #      if len(d) > 0:
      #         print d[0]
      #         return d[0]



        

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
 


import os, sys
import getopt
#import xml.etree.cElementTree as ET
from lxml import etree as ET
from xml.etree.ElementTree import QName
import re
import datetime
from xml.dom import minidom
import json

print 'ARGV      :', sys.argv[1:]

options, remainder = getopt.getopt(sys.argv[1:], 'i:v', ['inputdir=' 
                                 
                                                         ])
print 'OPTIONS   :', options

for opt, arg in options:
    if opt in ('-i', '--inputdir'):
        inputdir = arg
   


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
         #description.text = p.string()
         
root = ET.Element('programs')
root.set('version', '1.0') 

d=''

concordance = Concordance("../Config files per barcode - CoMeRDa gidsen 2012 - Gidsniveau.tsv")

for fsroot, dirs, filenames in os.walk(inputdir):   #loop all xml's (feed the script with one dir=one edition)
   filenames.sort()
   for f in filenames:
      if str(f) != ".xml" :
         bn = os.path.basename(inputdir)
         root.set('startDate', concordance.startDate[bn]) 
         root.set('endDate', concordance.endDate[bn]) 


         week = Week(concordance.startDate[bn])
         
         if os.path.exists("../configs/"+concordance.configFilename[bn]+".txt"):
            config = Config("../configs/"+concordance.configFilename[bn]+".txt") #load configfile    
         else:
            config = Config("../configs/empty_config_file.txt") #load configfile
         


         dir(config)
         print bn
         
         ff = str(inputdir + "/" + str(f))
         print ff
         tree = ET.parse(ff)
         doc = tree.getroot()
         namespace = 'http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml'
         
         lineList = []
         wordList = []
         
         word = ''
         confidence=word_l=word_t=word_r=word_b=None
         
     

         for block in doc.iter(str( QName( namespace, 'block' ) )):
            for line in block.iter(str( QName( namespace, 'line' ) )):
               lineobj = Line(sortIndex(block))
               for formatting in line.iter(str( QName( namespace, 'formatting' ) )):
                  for c in formatting.iter(str( QName( namespace, 'charParams' ) )):  #loop throug all characters
                     
         
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
               
               lineList.append(lineobj)   
         
         programList = []
         
         b=n=t=''
         
         for l in lineList: 
            if l.getDate() is not None: d=l.getDate() 

         for l in lineList: 

            if l.getNet() is not None: n=l.getNet()   
            if l.getBroadcaster() is not None: b=l.getBroadcaster()
            
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
            #print "SFSKHGLRSGLKREHJGILJHRLGKHLERGLERHGLETRUH" 

xml = ET.tostring(root,encoding='utf8', pretty_print=True)      
fp = open(bn+".xml", "w")
fp.write(xml)
fp.close()
 
