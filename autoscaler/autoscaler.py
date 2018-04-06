import time

class AutoScaler(object):
  def __init__(self, config, on):
    self.config = config
    self.on = on

  def autoscaler_loop(timequeue):
    while True:
      if self.on is True:
        len = 0
        sum = 0

        while not timequeue.empty():
          len = len + 1
          sum += float(timequeue.get())

        avg = sum/len
        if avg not 0:
          print('The average elapsed time: {}'.format(avg))
          # process avg here

        time.sleep(config[poll_interval])
