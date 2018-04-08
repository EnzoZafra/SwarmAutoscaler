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
    timeArray = [3,4,5,8,9,10]
    timeArray2 = [1,2,3,4,5,6,2]
    someArray = []
    y = avg_response
    y = [1,2,3,4,5,6,7,8]
    y2 = [1,2,4,5,7,8,9]
    
    title = 'reponse time vs elapsed time'
    line_chart = pygal.Line(width=1200, height=200,explicit_size=True, title=title,style=DarkSolarizedStyle,disable_xml_declaration=True)
    line_chart.x_labels = timeArray
    line_chart.add('chart1', y)

    line_chart2 = pygal.Line(width=1200, height=200,explicit_size=True, title=title,style=DarkSolarizedStyle,disable_xml_declaration=True)
    line_chart2.x_labels = timeArray2
    line_chart2.add('chart2', y2)


    line_chart3 = pygal.Line(width=1200, height=200,explicit_size=True, title=title,style=DarkSolarizedStyle,disable_xml_declaration=True)
    line_chart3.x_labels = timeArray2
    line_chart3.add('chart3', y2)






    return render_template("plot.html", line_chart=line_chart,line_chart2=line_chart2,line_chart3 = line_chart3)
#  return render_template('plot.html', title=title,line_chart=bar_chart)
#  return send_file('chart.png', mimetype='image/png')
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
   return render_template("plot.html")