#!/usr/bin/python

Test

class Line:
   'Common base class for all lines'

   def __init__(self, blockIdx):
      #self.baseline = baseline
      self.words = []
      #self.fontSize = fontSize 
      self.blockIdx = blockIdx 

   def string(self):
      s=''
      for w in self.words:
         s+=w.text
      return s 

   def getBroadcaster(self):
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
      netList = ['NEDERLAND 1','NEDERLAND 2','NEDERLAND 3','HILVERSUM 1']
      #return process.extractOne(self.string(), netList)

      for nn in netList:
         n = re.search('([\(|\s]'+nn+')|^'+nn+'', self.string(), re.I)
         if n is not None:
            return nn

   def getTime(self):
      t = re.findall('([0-23]{1,2}[.|:|,]{1}[0-59]{2})(?!\d)', l.string(), re.I)
      
      #if len(t) is 1:
      #   print "whegfjwybrf", t[0].split('.', 1);
      #elif len(t) is 2:
      #   return t[0]+' tot en met '+t[1]
      return t

   def getBounds(self):
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
         #print word.text, x, y, w, h
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
      
   #@property
   def getConfidence(self):
      return self.confidence / len(self.text)

class Program:
   'Common base class for all programs'

   def __init__(self):
      self.startTime = ''
      self.stopTime = ''
      self.net = ''
      self.broadcaster = ''
      self.description = []
      self.title = ''
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
from pprint import pprint
import re
import json
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import fuzzy
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


for root, dirs, filenames in os.walk(inputdir):
   filenames.sort()
   for f in filenames:
      if str(f) != ".xml" :
         bn = os.path.basename(inputdir)
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
                  for c in formatting.iter(str( QName( namespace, 'charParams' ) )):
                     
         
                     if c.get('wordStart') == '1': 
                        if word is not '': lineobj.words.append(Word(word, formatting.get('fs'), confidence, word_l, word_t, word_r, word_b))
                        if c.get('charConfidence') is not None: confidence=int(c.get('charConfidence'))
                        word_l=int(c.get('l'))
                        word_t=int(c.get('t'))
                        word_r=int(c.get('r'))
                        word_b=int(c.get('b'))
                        word=c.text
                     else:
                        if c.get('charConfidence') is not None: confidence+=int(c.get('charConfidence'))
                        if c.get('l') < word_l: word_l=int(c.get('l'))
                        if c.get('t') < word_t: word_t=int(c.get('t'))
                        if c.get('r') > word_r: word_r=int(c.get('r'))
                        if c.get('b') > word_b: word_b=int(c.get('b'))
                        word+=c.text
         
               if word is not '': lineobj.words.append(Word(word, formatting.get('fs'), confidence, word_l, word_t, word_r, word_b))
               word=''
               #confidence=word_l=word_t=word_r=word_b=None
               lineList.append(lineobj)   
         
         #lineList.sort(key=lambda x: x.blockIdx, reverse=False)
         
         programList = []
         
         b=n=t=''
         
         for l in lineList: 
            #print l.string(), l.getBounds()
            if l.getNet() is not None: n=l.getNet()   
            if l.getBroadcaster() is not None: b=l.getBroadcaster()
            if len(l.getTime()) > 0:
               try:
                  programList.append(programobj) 
               except:
                  foo = 'bar'
               programobj = Program()
               if len(l.getTime()) is 1:
                  programobj.startTime = l.getTime()[0]
               elif len(l.getTime()) is 2:
                  programobj.startTime = l.getTime()[0]
                  programobj.stopTime = l.getTime()[1]
               programobj.net = n
               programobj.broadcaster = b
               programobj.description.append(l.words)
         
               #if l.l < programobj.l: programobj.l=l.l
               #if l.l < programobj.l: programobj.l=l.l
               #if l.l < programobj.l: programobj.l=l.l
               #if l.l < programobj.l: programobj.l=l.l
         
            else:
               try:
                  programobj.description.append(l.words)
               except:
                  programobj = Program()
                  programobj.description.append(l.words)

         
         programList.append(programobj)
         
         root = ET.Element('programs')
         root.set('version', '1.0')
         


         file = open(bn+".csv", "a")
         
         #file.write("<html>\n")
         #file.write("<head>\n")
         #file.write("<link rel=\"stylesheet\" href=\"style.css\">\n")
         #file.write("<script type=\"text/javascript\" src=\"http://code.jquery.com/jquery-1.10.2.js\"></script>\n")        
         #file.write("</head>\n")
         #file.write("<body>\n")
         #file.write("<div class=\"menu\">\n")
         #file.write("<div class=\"menuBox\" id=\"toggleBox\">\n")
         #file.write("<span>Toggle Layers</span><br />\n")
         #file.write("<button id=\"strings\" >Strings</button><br />\n")
         #file.write("</div>\n")
         #file.write("</div>\n")
         #file.write("<div id=\"image\">\n")
         #file.write("<img src=\"file:///Users/picturae/Desktop/GDS002000056_JPG/"+bn+".jpg\" />\n")
     
         
         
         

         #for p in programList:
         #   if len(p.string()) < 2000:
         #      
         #      program = ET.SubElement(root, 'program')
         #      program.set('x', str(p.getBounds()[0]))
         #      program.set('y', str(p.getBounds()[1]))
         #      program.set('w', str(p.getBounds()[2]))
         #      program.set('h', str(p.getBounds()[3]))
         #
         #      if p.getBounds()[2] < 1000:
         #         
         #         file.write("<div class=\"highlighter\" id=\"highlight-string\" style=\" left: "+str(p.getBounds()[0])+"px; top: "+str(p.getBounds()[1])+"px; width: "+str(p.getBounds()[2])+"px; height: "+str(p.getBounds()[3])+"px; filter: alpha(opacity=50)\" ></div>\n")
         #         startTime = ET.SubElement(program, 'startTime')
         #         startTime.text = p.startTime
         #      
         #         stopTime = ET.SubElement(program, 'stopTime')
         #         stopTime.text = p.stopTime
         #      
         #         net = ET.SubElement(program, 'net')
         #         net.text = p.net
         #      
         #         broadcaster = ET.SubElement(program, 'broadcaster')
         #         broadcaster.text = p.broadcaster
         #      
         #         description = ET.SubElement(program, 'desc')
         #         description.text = p.string()
         #
         #file.write("<script>\n")
         #file.write("$(\"button[id*=strings]\").click(function () {\n")
         #file.write("$(\"div[id*=highlight-string]\").toggle();\n")
         #file.write("});\n")    
         #file.write("</script>\n")
         #file.write("</div>\n")
         #file.write("</body>\n")
         #file.write("</html>\n")  
         #file.close()        
         #print ET.tostring(root,encoding='unicode', pretty_print=True)






         










