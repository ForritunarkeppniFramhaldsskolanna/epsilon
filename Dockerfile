FROM ubuntu:trusty

ENV TERM xterm
ENV DEBIAN_FRONTEND noninteractive
ENV SHELL /bin/bash


RUN locale-gen en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
# Install add-apt-repository
RUN sed -i 's/archive.ubuntu.com/is.archive.ubuntu.com/' /etc/apt/sources.list
RUN apt-get update -qq && apt-get install -y software-properties-common

# Insert the app
RUN mkdir /epsilon
WORKDIR /epsilon
ADD . /epsilon/
RUN ./scripts/ubuntu/setup-all.sh
RUN pip3 install -r requirements.txt

# Build safeexec
WORKDIR /epsilon/judge/SafeExec
RUN make && make install && make clean
WORKDIR /epsilon

ENV EPSILON_JAIL /epsilon_jail
RUN ./judge/jail-setup.sh

ENTRYPOINT ["/epsilon/docker/entrypoint.sh"]
