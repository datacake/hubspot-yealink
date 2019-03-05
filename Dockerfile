FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update -y && apt-get install -y libmemcached-dev zlib1g-dev
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
