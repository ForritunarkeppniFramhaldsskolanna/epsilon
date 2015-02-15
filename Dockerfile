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

# Build isolate
WORKDIR /epsilon/judge/isolate
RUN make && sudo ./fix_mod.sh
WORKDIR /epsilon

ENTRYPOINT ["/epsilon/docker/entrypoint.sh"]
