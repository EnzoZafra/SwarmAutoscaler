FROM python:2.7-slim
WORKDIR /temp
ADD . /temp
RUN pip install -r requirements.txt
CMD ["python", "app/run.py"]
