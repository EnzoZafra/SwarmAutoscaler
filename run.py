import yaml
from multiprocessing import Process, Value, Queue
from api import app
from .autoscaler import AutoScaler

if __name__ == '__main__':
  with open("config.yml", r) as ymlfile:
    cfg = yaml.load(ymlfile)

  timequeue = Queue()
  autoscaler = AutoScaler(cfg, True)
  p = Process(
              target = AutoScaler.autoscaler_loop,
              args = (timequeue, )
              )
  p.start()
  app.run(host="0.0.0.0", port=1337, debug=True)
  p.join()
