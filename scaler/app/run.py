import yaml
import argparse
import time
import ctypes
import requests
from multiprocessing import Process, Value, Queue
from api import app, timequeue, avg_response, workload, replications, timeArray, toggle
from mydocker.dockerapi import DockerAPIWrapper
from requests.exceptions import ConnectionError, RequestException

dockerapi = DockerAPIWrapper()
startTime = 0

def autoscaler_loop(timequeue, config, avg_response
                    , replications, workload, timeArray, toggle):

  with open(config.value, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

  scale_up_threshold = cfg['scale_up_threshold']
  scale_down_threshold = cfg['scale_down_threshold']
  scale_step = cfg['scale_step']
  max_replica = cfg['max_replica']
  min_replica = cfg['min_replica']
  poll_interval = cfg['poll_interval']
  servicename = cfg['servicename']
  servicehost = cfg['servicehost']

  on = True;
  while True:
    if not toggle.empty():
      on = toggle.get()

    len = 0
    sum = 0

    interval_start = time.time();
    t1 = 0;
    while poll_interval > t1 - interval_start:
      try:
        t0 = time.time()
        r = requests.get("http://" + servicehost + "/", timeout=2*scale_up_threshold)
        # r = requests.get("http://10.1.0.138:8000/")
        t1 = time.time()
        len = len + 1
        sum += t1-t0
      except ConnectionError as e:
        print('Service is autoscaling. Please try again')
      except RequestException:
        t1 = time.time()
        len = len + 1
        sum += t1-t0

    avg = sum/len if len else 0
    if avg != 0:
      while not timequeue.empty():
        timequeue.get()
        len = len + 1

      if len != 0:
        req_per_sec = len / (t1 - interval_start)

      workload.append(req_per_sec)
      curr_repcount = dockerapi.getReplicaCount(servicename)

      avg_response.append(avg)
      replications.append(curr_repcount)
      elapsedTime = time.time() - startTime
      timeArray.append(elapsedTime)

      if on:
        if avg > scale_up_threshold:
          repcount = curr_repcount + scale_step
          if repcount <= max_replica:
            dockerapi.scaleService(servicename, repcount)
            print("Scaling up")
        if avg < scale_down_threshold:
          repcount = curr_repcount - scale_step
          if repcount >= min_replica:
            dockerapi.scaleService(servicename, repcount)
            print("Scaling down")

if __name__ == '__main__':
  startTime = time.time()
  parser = argparse.ArgumentParser(description="An autoscaler for your swarm cluster")
  parser.add_argument('configfile',
                      help='include a path to a configuration file')
  args = parser.parse_args()

  if args.configfile is not None:
    config = Value(ctypes.c_char_p, args.configfile)
  else:
    config = Value(ctypes.c_char_p, "/opt/swarmautoscaler/autoscaler.yml")

  p = Process(
    target = autoscaler_loop,
    args = (timequeue, config, avg_response, replications, workload, timeArray, toggle)
  )

  p.start()
  app.run(host="0.0.0.0", port=1337)
  p.join()
