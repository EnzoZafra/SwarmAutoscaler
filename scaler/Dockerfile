FROM python:2.7-slim
ADD . /opt/swarmautoscaler
WORKDIR /opt/swarmautoscaler
RUN pip install -r requirements.txt
CMD ["python", "app/run.py", "swarmautoscaler.yml"]
