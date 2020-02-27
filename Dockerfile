

FROM python:3.8.1-buster as build

RUN apt-get update --quiet \
 && apt-get install -y --quiet --no-install-recommends \
        python3-pip \
        python3-setuptools \
 && python3 -m pip install --upgrade pip pip-tools

RUN python3 --version
RUN mkdir ./implied_vol_prediction


COPY . /implied_vol_prediction/
WORKDIR /implied_vol_prediction/

RUN pip-compile requirements.in \
 && pip-sync


