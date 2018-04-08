from flask import Flask, request, send_file,render_template
import pygal
import sys
from StringIO import StringIO
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
    times = [x for x in timeArray]
    x_title = 'Elapsed time (sec)'

    title = 'Average Response Time vs Elapsed Time'
    y_title = 'Response Time (sec)'
    line_chart = pygal.Line(width=1200, height=200,explicit_size=True,
                            title=title, x_title=x_title, y_title=y_title
                            style=DarkSolarizedStyle,disable_xml_declaration=True)
    line_chart.x_labels = times
    avg_response_arr = [x for x in avg_response]
    line_chart.add('response time', avg_response_arr)

    title2 = 'Requests per second vs Elapsed Time'
    y_title2 = 'Requests per second'
    line_chart2 = pygal.Line(width=1200, height=200,explicit_size=True,
                             title=title2, x_title=x_title, y_title=y_title2
                             style=DarkSolarizedStyle,disable_xml_declaration=True)
    line_chart2.x_labels = times
    workload_arr = [x for x in workload]
    line_chart2.add('workload', workload_arr)

    title3 = 'Number of Replications vs Elapsed Time'
    y_title3 = 'Number of Replicas'
    line_chart3 = pygal.Line(width=1200, height=200,explicit_size=True,
                             title=title3, x_title=x_title, y_title=y_title3
                             style=DarkSolarizedStyle,disable_xml_declaration=True)
    line_chart3.x_labels = times
    replications_arr = [x for x in replications]
    line_chart3.add('replication', replications_arr)

    return render_template("plot.html", line_chart=line_chart,line_chart2=line_chart2,line_chart3 = line_chart3)
