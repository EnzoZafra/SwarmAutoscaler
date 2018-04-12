# Swarm AutoScaler

Swarm AutoScaler is a service which gathers response time statistics for a cloud microservice application
and automatically scales the said cloud microservice depending on the gathered statistics. The auto-scaler scales
the application horizontally according to the workload. An acceptable range for response time is indicated by an
upper and lower threshold which can be configured by a configuration file.

## Authors

* **Lorenzo Zafra** - [enzozafra](https://github.com/enzozafra)
* **Alexander Nguyen** - [ahnguyen03](https://github.com/ahnguyen03)

## Getting Started


### Prerequisites
To install, you will need Python 2.7, and Pip

On Ubuntu, they can be installed with

```
sudo apt-get install python-pip python-dev build-essential 
```
then update
```
sudo pip install --upgrade pip 
```

### Installing Locally
When SwarmAutoScaler is ran locally, it is assumed that the Docker service you want
to auto-scale is up and running.

clone the project

```
git clone https://github.com/EnzoZafra/SwarmAutoScaler.git
```

go to the scaler's directory

```
cd SwarmAutoScaler/scaler
```

install packages

```
pip install -r requirements.txt
```

run autoscaler

```
python app/run.py  ../swarmautoscaler.yml
```

run the client which emulates load and sends a POST request to the autoscaler for statistics

```
cd ../client
python http_client [autoscaler's ip] [numthreads] [delay_per_request]
```


### Running in a Docker Swarm
Add this service to your docker-compose file
```
service:
   autoscaler:
     image: zafra/swarmautoscaler:ece422
     # command: "--configfile swarmautoscaler.yml"
     ports:
       - "1337:1337"
     volumes:
       - ${PWD}/swarmautoscaler.yml:/opt/swarmautoscaler/swarmautoscaler.yml
       - /var/run/docker.sock:/var/run/docker.sock
     deploy:
       placement:
         constraints:
           - node.role == manager
```

### Example in a Docker Swarm
get a copy of the configuration file
```
wget https://raw.githubusercontent.com/EnzoZafra/SwarmAutoscaler/master/swarmautoscaler.yml
```

get a copy of the docker-compose file
```
wget https://raw.githubusercontent.com/EnzoZafra/SwarmAutoscaler/master/docker-compose.yml
```

deploy the stack in your swarm
```
docker stack deploy --compose-file docker-compose.yml app_name
```

run the client which emulates load and sends a POST request to the autoscaler for statistics

```
wget https://raw.githubusercontent.com/EnzoZafra/SwarmAutoscaler/master/client/http_client.py
python http_client [autoscaler's ip] [numthreads] [delay_per_request]
```

### Example in a Docker Swarm
Graphs plotting request per second, workload and number of replicas for the service can be found at the link below
```
http://[autoscalerip]:1337/graphs
```
* Assumes that you have autoscaler running

## Built With

* [Python](https://www.python.org/) - Language used
* [Flask](http://flask.pocoo.org/) - API Framework
* [pyyaml](http://pyyaml.org/wiki/PyYAML) - YAML file parser
* [DockerApi](https://docker-py.readthedocs.io) - Docker Python API
* [PyGal](http://pygal.org/) - Graphing in Python


