#!/usr/bin/python3
import sys
sys.path.append('/home/richard/.local/lib/python3.10/site-packages/')
from spellchecker import SpellChecker
#pip install pyspellchecker
from flask import Flask, request, render_template
#from flask import escape
import sys
#For French
#spell = SpellChecker(language='fr')
#misspelled = ["resaissir", "matinnée", "plonbier", "tecnicien"]
spell = SpellChecker()

def convert(text):
  x=text.replace("\r\n"," <br/> ")
  return x

def CorectText(misspelled,corrected):
  global wordcount
  wordcount=0
  for mword in misspelled:
    firstchr=""
    space=False
    count=0
    period=False
    comma=False
    exclamation=False
    question=False
    semicolon=False
    colon=False
    Andsign=False
    DoubleQuotes=False
    SingleQuotes=False
    Hyphen=False
    SpecialCharacters = ["\"","'","-"]
    SpecialChar=False
    secondchr=""
    length=0
    mlst = list(mword)
    length = len(mword)
    for m in mlst:
       count+=1
       for sc in SpecialCharacters:
         if count==1 and m==sc:
           SpecialChar=True
       if count==1:
         firstchr=m
       else:
         if SpecialChar and count==2:
           secondchr=m           
         if m==" ":
           space=True
         if (m=="." and count==length) or (m=="." and count==length-1):
           period=True
           if (m=="." and count==length-1):
              space=False  
         if m==",":
           comma=True
         if m=="!":
           exclamation=True 
         if m=="?":
           question=True
         if m==";":
           semicolon=True
         if m==":":
           colon=True
         if m=="&":
           Andsign=True
         if m=="\"":
           DoubleQuotes=True
         if m=="'":
           SingleQuotes=True
         if m=="-":
           Hyphen=True 

    wordcount+=1
    DoWord(firstchr,secondchr,SpecialChar,space,period,comma,exclamation,question,semicolon,colon,Andsign,DoubleQuotes,SingleQuotes,Hyphen)
     
def DoWord(firstchr,secondchr,SpecialChar,space,period,comma,exclamation,question,semicolon,colon,Andsign,DoubleQuotes,SingleQuotes,Hyphen):      
  count=0 
  global correctedtxt
  c = list(corrected[wordcount-1])
  for clst in c:
          count+=1
          if count==1:
             correctedtxt+=firstchr
          else:
            if SpecialChar and count==2:
              correctedtxt+=secondchr+clst
            else:  
              correctedtxt+=clst
  if period:
    correctedtxt+="."
  if comma:
    correctedtxt+=","
  if exclamation:
    correctedtxt+="!"
  if question:
    correctedtxt+="?"
  if semicolon:
    correctedtxt+=";"
  if colon:
    correctedtxt+=":"
  if Andsign:
    correctedtxt+="&"
  if DoubleQuotes:
    correctedtxt+="\""
  if SingleQuotes:
    correctedtxt+="'"
  if Hyphen:
    correctedtxt+="-"
  if space:
    correctedtxt+=" "

def CheckText(text):
  textstr = list(convert(text))
  global txtstr
  txtstr=""
  for txt in textstr:
    txtstr += txt
    if(txt == " "):
     misspelled.append(txtstr)
     txtstr=""
     global Dotext
     Dotext=False
  misspelled.append(txtstr)
  return misspelled

def convertbr(text):
  x=text.replace(" <br/> ","<br>")
  return x

def clean(text):
  x=text.replace(",","")
  x=x.replace(".","")
  x=x.replace("!","")
  x=x.replace("?","")
  x=x.replace(";","")
  x=x.replace(":","")
  x=x.replace("&","")
  x=x.replace("\"","")
  x=x.replace("'","")
  x=x.replace("-","")
  return x  
  
def clrdatam():
  for m in range(0,len(misspelled)):
    misspelled.pop(m)

def clrdatac():
  for c in range(0,len(corrected)):
    corrected.pop(c) 

def delete(text):
    lst=list(text)
    count=0
    count2=0
    str=""
    Dobr=False
    for l in lst:
        count+=1
        if l=="\n":
            count2=count
            Dobr=True
        if count2!=count-1:
            str+=l
        elif not Dobr:
            str+=l
    return str

def checknumber(word):
    usemisspelled=False
    period=False
    for character in word:
        if character==".":
            period =True
        if period and character.isdigit():
            usemisspelled = True
    return usemisspelled  
             
global misspelled
misspelled = []
misspelled.clear()

global corrected
corrected = []
corrected.clear()

global txtstr
txtstr =""

global corectedtxt
correctedtxt=""

global count
count=0

global Dotext
Dotext=True

global wordcount
wordcount=0  
  
try:
    if sys.argv[1] !="":
        text=sys.argv[1]

    misspelled.clear()
    CheckText(text)
#misspelled = spell.unknown(misspelled)
#print(misspelled)
except:
    text="No text entered please try again"
    misspelled=list(text)
corrected.clear()
for word in misspelled:
             if not checknumber(word):
                word=clean(word)   
                correctedword = spell.correction(word)
             else:
                correctedword = word[:-1]    
             corrected.append(correctedword)
#print(corrected)
correctedtxt=""
CorectText(misspelled,corrected)
correctedtxt=convertbr(correctedtxt)
print(correctedtxt)
#x=list(correctedtxt)
#print(x)
