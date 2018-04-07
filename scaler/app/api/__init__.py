from flask import Flask, request, send_file
import sys
from StringIO import StringIO
import numpy as np
import matplotlib.pyplot as plt
import time
import random
from multiprocessing import Queue, Manager

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
    plt.axis([0,200,0,200])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.ion()
    fig.show()
    fig.canvas.draw()

    y = avg_response
    print(timeArray)
    for item in timeArray:
      print(item)
    ax.plot(timeArray, y, '-o')
    img = StringIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/printgraph')
def images():
  return render_template("templates/plot.html", title=cropzonekey)
