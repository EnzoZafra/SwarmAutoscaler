import yaml
import time
from multiprocessing import Process, Value, Queue
from api import app, timequeue
from mydocker.dockerapi import DockerAPIWrapper

scale_up_threshold = 0
scale_down_threshold = 0
scale_step = 0
max_replica = 0
min_replica = 0
poll_interval = 0
servicename = ''

dockerapi = DockerAPIWrapper()

def autoscaler_loop(timequeue, on):
  with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

  scale_up_threshold = cfg['scale_up_threshold']
  scale_down_threshold = cfg['scale_down_threshold']
  scale_step = cfg['scale_step']
  max_replica = cfg['max_replica']
  min_replica = cfg['min_replica']
  poll_interval = cfg['poll_interval']
  servicename = cfg['servicename']
  target_url = cfg['target_url']

  while True:
    if on.value == True:
      len = 0
      sum = 0

      while not timequeue.empty():
        len = len + 1
        sum += float(timequeue.get())

      avg = sum/len if len else 0
      if avg != 0:
        print('The average elapsed time: {}'.format(avg))
        if avg > scale_up_threshold:
          repcount = dockerapi.getReplicaCount(servicename) + scalestep
          if repcount <= max_replica:
            dockerapi.scaleService(servicename, repcount)
            print("Scaling up")
        if avg < scale_down_threshold:
          repcount = dockerapi.getReplicaCount(servicename) - scalestep
          if repcount >= min_replica:
            dockerapi.scaleService(servicename, repcount)
            print("Scaling down")
      else:
        print("avg is 0")
      time.sleep(poll_interval)

if __name__ == '__main__':
  val = Value('b', True)
  p = Process(
              target = autoscaler_loop,
              args = (timequeue, val)
              )
  p.start()
  app.run(host="0.0.0.0", port=1337, debug=True)
  p.join()
