from flask import Flask, request, send_file,render_template
import pygal
import sys
from StringIO import StringIO
import numpy as np
import matplotlib.pyplot as plt
import time
import random
from multiprocessing import Queue, Manager
from pygal.style import DarkSolarizedStyle

global timequeue
global avg_response
global workload
global replications
global timeArray

app = Flask(__name__)

timequeue = Queue()
avg_response = Manager().list()
workload = Manager().list()
replications = Manager().list()
timeArray = Manager().list()

@app.route('/metric', methods=['GET', 'POST'])
def addmetric():
  if request.method == 'POST':
    time = request.form.get('time')
    timequeue.put(time)
    return 'OK'
  else:
    return 'You did a get post on /metric'


@app.route('/graphs', methods=['GET'])
def plotstats():
  if request.method == 'GET':
    timeArray = []
    someArray = []
    title = 'reponse time vs elapsed time'
    line_chart = pygal.Line(width=1200, height=600,explicit_size=True, title=title,style=DarkSolarizedStyle,disable_xml_declaration=True)
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = [0,1,2,3,4,5,6,7,8,9,10]
    for i in range(0,10):
      y = random.randint(1,100)
      someArray.append(y)
      line_chart.add('Firefox', someArray)
      line_chart.render_to_png('chart.png')
      print("inside here")
  return send_file('chart.png', mimetype='image/png')
""" plt.axis([0,200,0,200])
    fig = plt.figure()
    ax = fig.add_subplot(111)
#   plt.ion()
#   fig.show()
    fig.canvas.draw()

    y = avg_response
    print(timeArray)
    for item in timeArray:
      print(item)
    ax.plot(timeArray, y, '-o')
    img = StringIO()
    fig.savefig(img)
    img.seek(0)"""

@app.route('/printgraph')
def images():
   return render_template("templates/plot.html")