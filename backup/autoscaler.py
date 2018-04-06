"""
TODO: documentation file
"""

import time
from flask import Flask, request
from multiprocessing import Process, Value, Queue

app = Flask(__name__)
timequeue = Queue()

@app.route('/metric', methods=['GET', 'POST'])
def addmetric():
  global timequeue

  if request.method == 'POST':
    time = request.form.get('time')
    timequeue.put(time)
    return 'OK'
  else:
    return 'You did a get post on /metric'

def autoscaler_loop(loop_on, timequeue):
  while True:
    if loop_on.value == True:
      len = 0
      sum = 0
      while not timequeue.empty():
        len = len + 1
        sum += float(timequeue.get());
      avg = sum/len if sum else '-'
      if avg is not '-':
        print('The average elapsed time: {}'.format(avg))
    time.sleep(10)

if __name__ == "__main__":
  autoscaler_on = Value('b', True)
  p = Process(target=autoscaler_loop, args=(autoscaler_on, timequeue))
  p.start()
  app.run(host="0.0.0.0", port=1337, debug=True)
  p.join()
