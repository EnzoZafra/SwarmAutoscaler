from flask import Flask, request

app = Flask(__name__)

@app.route('/metric', methods=['GET', 'POST'])
def addmetric():
  global timequeue
  if request.method == 'POST':
    time = request.form.get('time')
    timequeue.put(time)
    return 'OK'
  else:
    return 'You did a get post on /metric'
