FROM daocloud.io/ubuntu:16.04

MAINTAINER Robin<robin.chen@b-uxin.com>

ENV LANG C.UTF-8


#创建并管理Python运行的环境
RUN pip install virtualenv
RUN virtualenv --no-site-packages smenv
#使用bash命令集

RUN ["/bin/bash","-c","source smenv/bin/activate"]

RUN apt-get update
RUN apt-get install -y python3 && \
     apt-get install -y python-pip

RUN  mkdir -p /app

WORKDIR /app

COPY /app /app
COPY base.txt /app
COPY requirements.txt /app

#安装Python程序运行的依赖库
RUN cd /app && pip install -r base.txt
RUN cd /app && pip install -r requirements.txt


EXPOSE 80


ENTRYPOINT ["python", "/app/main.py"]