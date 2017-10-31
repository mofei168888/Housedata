FROM daocloud.io/ubuntu:16.04


ENV LANG C.UTF-8

RUN apt-get update
RUN apt-get install -y python3 && \
     apt-get install -y python-pip

RUN  mkdir -p /app

WORKDIR /app


COPY / /app
COPY base.txt /app
COPY requirements.txt /app

RUN cd /app && pip install -r base.txt
RUN cd /app && pip install -r requirements.txt


EXPOSE 80


ENTRYPOINT ["python", "/app/main.py"]