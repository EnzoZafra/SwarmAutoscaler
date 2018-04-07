from flask import Flask, request
import sys
from multiprocessing import Queue

app = Flask(__name__)

global timequeue

timequeue = Queue()

@app.route('/metric', methods=['GET', 'POST'])
def addmetric():
  if request.method == 'POST':
    time = request.form.get('time')
    timequeue.put(time)
    return 'OK'
  else:
    return 'You did a get post on /metric'
