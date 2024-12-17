#Lotto Drawing program using a class
#from sys import stdout
import SpellChecker
import sys
sys.path.append('/home/richard/.local/lib/python3.10/site-packages/')
from flask import Flask, request, render_template, Response, redirect,jsonify
import pandas as pd
import json
import random
import os
import requests
import subprocess
import sys
sys.path.append('/home/richard/Projects/Python')
import LottoPicker
 
#os.system('clear')

global drawnumbers
drawnumbers = []

global data

global lotto

global count

lottochoice = "None"

#print("""1 = Lotto 6/49
#2 = LottoMax
#3 = Grande Vie
#4 = Tout Ou Rien""")
#print()

global table
table = []

def LottoMax():
 with open('/home/richard/Projects/www/Home/Documents/LottoMax.json', 'r') as f:
    content = f.read()
    content = content.rstrip(",")
    table = json.loads(content)
 return table   

tasks = table

def choose(i):
    switcher = {
        1: 'Lotto649.json',
        2: 'LottoMax.json',
        3: 'Grande_Vie.json',
        4: 'ToutouRien.json'
    }
    return switcher.get(i, 'Invalid Number')
    
url = "https://richard-perreault.com/Documents/countries.json"

response = requests.get(url)
data = json.loads(response.text)
df = pd.DataFrame(data)

app = Flask('app')

@app.route('/getservices/', methods=["GET", "POST"])
def getservices():
    tasks=LottoMax()
    return jsonify(tasks)

@app.route('/countries', methods=["GET", "POST"])
def index2():
   return render_template('countries.html', data=df,len=len(df))

def convert(text):
  x=text.replace("\r\n"," <br/> ")
  return x

@app.route('/spellcheck', methods=["GET", "POST"])   
def index3():
    errors=[]
    global s
    s=""
    txt=""
    text=""
    if request.method == "POST":
        if request.form.get("Submit"):
             #try:
                 text = request.form['misspelled']
                 a=subprocess.Popen(["./SpellChecker.py",text],stdout = subprocess.PIPE)
                 txt=a.stdout.read().strip()
                 s=txt.decode()
                 #s=txt.replace("b''","")
                 print(str(s))
             #except:                               
                 errors.append(		    
"Unable to get URL. Please make sure it's valid and try again."
)
                 #print(errors)
    return render_template('spellcheck.html', title='Spell Checker',misspelled=convert(text),corrected=str(s))

@app.route('/', methods=["GET", "POST"])
def index():
    errors = []
    global pr
    pr = ""
    global data
    global lotto
    global count
    global drawnumbers
    lottochoice=request.args.get('lotto')
    global lotto
    lottochoice=request.args.get('lotto')
    if str(lottochoice) != "None":
           lotto = int(lottochoice)
    else:   
        if request.method == "POST":
            if request.form.get("Submit"):
                choice = request.form['choice']
                lotto = int(choice)
    try:
      jsonfile = choose(lotto)
      url = "https://richard-perreault.com/Documents/" + jsonfile
      response = requests.get(url)
      data = json.loads(response.text)
      count = len(data)
      
      #Lotto 6/49 Drawings global drawnumbers
      if lotto == 1:
        lottonumbers = LottoDrawings(7, 49, -5, drawnumbers)
        pr = "<p>The winning 6/49 numbers are<br>" + str(
        lottonumbers.drawnumbers) + "<br>in a total of " + str(
        count) + " drawings</p>"

      #Lotto Max Drawings
      if lotto == 2:
        lottonumbers = LottoDrawings(8, 50, -6, drawnumbers)
        pr = "<p>The Lotto Max winning numbers are<br>" + str(
        lottonumbers.drawnumbers) + "<br>in a total of " + str(
        count) + " drawings</p>"

        #Grande Vie Drawings
      if lotto == 3:
        lottonumbers = LottoDrawings(6, 49, -4, drawnumbers)
        pr = "<p>The winning Grande Vie numbers are<br>" + str(
        lottonumbers.drawnumbers) + "<br>in a total of " + str(
        count) + " drawings</p>"

          #Tout ou rien Drawings
      if lotto == 4:
        lottonumbers = LottoDrawings(13, 24, -11, drawnumbers)
        pr = "<p>The winning Tout ou rien numbers are<br>" + str(
        lottonumbers.drawnumbers) + "<br>in a total of " + str(
        count) + " drawings</p>"
                         
    except Exception as e:
        errors.append(
        "Unable to get URL. Please make sure it's valid and try again."
        )
        print(e.args[0])
    print(pr)
    return render_template('index.html', result=pr, title="Lotto Drawings")


class LottoDrawings():
    def __init__(self, rangenum, drawingnum, same, drawnumbers):
        self.rangenum = rangenum
        self.drawingnum = drawingnum
        self.same = same
        self.drawnumbers = drawnumbers

        def PrintStatus():
            print("|\r", end="")
            print("/\r", end="")
            print("|\r", end="")
            print("\\\r", end="")
            print("|\r", end="")
            print("/\r", end="")

        PickNumbers = True

        hits = 0

        while PickNumbers or hits > 0:

            numbers = []

            hits = 0

            for count in range(1, rangenum):
                rnd = random.randint(1, drawingnum)
                samenumber = 0
                numbers2 = LottoPicker.PickLottoNumbers(samenumber, drawingnum,numbers)
                numbers2[0].append(rnd)
                numbers2[0].sort()
                samenumber = 0
            while samenumber != same:
                numbers2 = LottoPicker.PickLottoNumbers(samenumber, drawingnum,numbers)
                samenumber = numbers2[1]
            numbers = numbers2[0]

            if same == -4:
                rnd = random.randint(1, 6)
                numbers.append(rnd)

            self.drawnumbers = numbers

            with open("LottoDrawings.txt", 'w+') as File:

                for pan in data:

                    PrintStatus()

                    hit = 0

                    #Lotto 6/49 Drawings
                    if lotto == 1:

                        for num in range(0, 6):
                            if numbers[num] == int(pan["P1"]) or numbers[num] == int(pan["P2"]) \
                            or numbers[num] == int(pan["P3"]) or numbers[num] == int(pan["P4"]) \
                            or numbers[num] == int(pan["P5"]) or numbers[num] == int(pan["P6"]) \
                            or numbers[num] == int(pan["P7"]):
                                hit += 1
                        if hit == 6:
                            PickNumbers = True
                            File.write(pan["Drawdate"] + ", ")
                            hits += 1
                        else:
                            PickNumbers = False

                    #LottoMax Drawings
                    if lotto == 2:

                        for num in range(0, 7):
                            if numbers[num] == int(pan["P1"]) or numbers[num] == int(pan["P2"]) \
                            or numbers[num] == int(pan["P3"]) or numbers[num] == int(pan["P4"]) \
                            or numbers[num] == int(pan["P5"]) or numbers[num] == int(pan["P6"] \
                            or numbers[num] == int(pan["P7"])):
                                hit += 1
                            if hit == 4 or hit == 7:
                                PickNumbers = True
                                File.write(pan["Drawdate"] + ", ")
                                hits += 1
                            else:
                                PickNumbers = False

                    #Grande Vie Drawings
                    elif lotto == 3:

                        if numbers[0] == int(pan["p1"]) and numbers[1] == int(pan["p2"]) \
                        and numbers[2] == int(pan["p3"]) and numbers[3] == int(pan["p4"])\
                        and numbers[4] == int(pan["p5"]):
                            PickNumbers = True
                            File.write(pan["Drawdate"] + ", ")
                            hits = +1
                        else:
                            PickNumbers = False

                        if numbers[0] == int(pan["p1"]) and numbers[1] == int(pan["p2"]) \
                        and numbers[2] == int(pan["p3"]) and numbers[3] == int(pan["p4"]) \
                        and numbers[4] == int(pan["p5"]) and numbers[5] == int(pan["gn"]):
                            PickNumbers = True
                            File.write(pan["Drawdate"] + ", ")
                            hits = +1
                        else:
                            PickNumbers = False

                        for num in range(0, 5):
                            if numbers[num] == int(pan["p1"]) or numbers[num] == int(pan["p2"]) \
                            or numbers[num] == int(pan["p3"]) or numbers[num] == int(pan["p4"]):
                                hit += 1
                            if hit == 5:
                                PickNumbers = True
                                File.write(pan["Drawdate"] + ", ")
                                hits += 1
                            else:
                                PickNumbers = False

                    #Tout ou Rien Drawings
                    if lotto == 4:
                        for num in range(0, 12):
                            if numbers[num] == int(pan["p1"]) or numbers[num] == int(pan["p2"]) \
                            or numbers[num] == int(pan["p3"]) or numbers[num] == int(pan["p4"]) \
                            or numbers[num] == int(pan["p5"]) or numbers[num] == int(pan["p6"]) \
                            or numbers[num] == int(pan["p7"]) or numbers[num] == int(pan["p8"]) \
                            or numbers[num] == int(pan["p9"]) or numbers[num] == int(pan["p10"]) \
                            or numbers[num] == int(pan["p11"]) or numbers[num] == int(pan["p12"]):
                                hit += 1
                            if hit == 12:
                                PickNumbers = True
                                File.write(pan["Drawdate"] + ", ")
                                hits += 1
                            else:
                                PickNumbers = False


#app.run(host='0.0.0.0')
if __name__ == "__main__":
    app.run()

