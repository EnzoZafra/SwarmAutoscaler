import yaml
import argparse
import time
import ctypes
from multiprocessing import Process, Value, Queue
from api import app, timequeue, avg_response, workload, replications, timeArray
from mydocker.dockerapi import DockerAPIWrapper

dockerapi = DockerAPIWrapper()
startTime = 0

def autoscaler_loop(timequeue, on, config, avg_response
                    , workload, replications, timeArray):
  with open(config.value, 'r') as ymlfile:
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
        curr_repcount = dockerapi.getReplicaCount(servicename)
        req_per_sec = len / poll_interval

        avg_response.append(avg)
        replications.append(curr_repcount)
        workload.append(req_per_sec)
        elapsedTime = time.time() - startTime
        timeArray.append(elapsedTime)

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
      time.sleep(poll_interval)

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

  val = Value("b", True)
  p = Process(
              target = autoscaler_loop,
              args = (timequeue, val, config, avg_response, workload, replications, timeArray)
              )
  p.start()
  app.run(host="0.0.0.0", port=1337)
  p.join()
