
FROM python:3.8.1-buster as build

RUN apt-get update --quiet \
 && apt-get install -y --quiet --no-install-recommends \
        python3-pip \
        python3-setuptools \
 && python3 -m pip install --no-cache-dir --upgrade pip pipenv


RUN mkdir /reka


COPY ./implied_vol_prediction/ /reka/
WORKDIR /reka/implied_vol_prediction
RUN pipenv install --dev --deploy \
 && pipenv run pip install -e .



