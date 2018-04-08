import numpy as np
import matplotlib.pyplot as plt
import time
import random

plt.axis([0,200,0,200])
fig = plt.figure()
ax = fig.add_subplot(111)
plt.ion()
fig.show()
fig.canvas.draw()
startTime = time.time()
emptyArray =[]
timeArray = []
oldElasped = 0
for i in range(0,400):
    elapsedTime = time.time() - startTime
    timeArray.append(elapsedTime)
    y = random.randint(1,100)
    emptyArray.append(y)
    timeCounter = elapsedTime
    check2Sec = elapsedTime - oldElasped
    if(check2Sec > 10):
      print("inside here")
      oldElasped = elapsedTime
      plt.axis([elapsedTime-1,elapsedTime+10,0,100])
    ax.plot(timeArray,emptyArray,'--r')
    fig.canvas.draw()