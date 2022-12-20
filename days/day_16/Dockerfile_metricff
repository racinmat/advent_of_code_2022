FROM ubuntu:20.04

COPY ./Metric-FF-v2.1 /root/Metric-FF-v2.1

WORKDIR /root/Metric-FF-v2.1

RUN apt-get update

RUN apt-get install -y \
    make gcc

RUN apt-get install -y \
    flex bison dos2unix

RUN make
