

FROM python:3.8.1-buster as build

RUN apt-get update --quiet \
 && apt-get install -y --quiet --no-install-recommends \
        python3-pip \
        python3-setuptools \
 && python3 -m pip install --upgrade pip pip-tools

RUN python3 --version
RUN mkdir ./reka


COPY . /reka/
COPY src/ /src/
#RUN ls -la /src/*
WORKDIR /reka/implied_vol_prediction
COPY requirements.txt .

RUN pip install notebook \
 && pip install --no-cache-dir -r requirements.txt
 #&& pip-compile ./requirements.in > ./requirements.txt \
 #&& pip-sync
 #&&
#pipenv install --dev --deploy \
# && pipenv run pip install -e .
