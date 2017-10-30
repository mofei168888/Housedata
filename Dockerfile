FROM python:3.6.2
MAINTAINER Robin <Robin.chen@b-uxin.com>


RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app
RUN cd /app && pip install  -r requirements.txt

COPY main.py /app

EXPOSE 80

ENTRYPOINT ["python3", "/app/main.py"]