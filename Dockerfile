FROM ubuntu:trusty

ENV TERM xterm
ENV DEBIAN_FRONTEND noninteractive
ENV SHELL /bin/bash
# Install add-apt-repository
RUN sed -i 's/archive.ubuntu.com/is.archive.ubuntu.com/' /etc/apt/sources.list
RUN apt-get update -qq && apt-get install -y software-properties-common
RUN apt-get install -y postgresql-client

# Insert the app
RUN mkdir /epsilon
WORKDIR /epsilon
ADD . /epsilon/
RUN ./scripts/ubuntu/setup-all.sh
RUN pip3 install -r requirements.txt
