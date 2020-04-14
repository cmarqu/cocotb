# FROM gitpod/workspace-full-vnc
FROM ubuntu:16.04

#USER gitpod

# Install custom tools, runtime, etc. using apt-get
# For example, the command below would install "bastet" - a command line tetris clone:
#
# RUN sudo apt-get -q update && #     sudo apt-get install -yq bastet && #     sudo rm -rf /var/lib/apt/lists/*
#
# More information: https://www.gitpod.io/docs/config-docker/




# travis-ci only provides 2
ARG MAKE_JOBS=-j2

# Simulation
ARG ICARUS_VERILOG_VERSION=10_2

RUN sudo apt-get -qq update && apt-get -qq install -y --no-install-recommends \
       wget \
       git \
       gperf \
       make \
       autoconf \
       g++ \
       flex \
       bison \
       python3-dev\
       python3-pip \
       python3-setuptools \
       python3 \
       virtualenv \
       python3-venv \
       swig \
    && sudo rm -rf /var/lib/apt/lists/* \
    && sudo apt-get clean \
    && sudo pip3 install --upgrade pip \
    && sudo g++ --version

# Icarus Verilog
ENV ICARUS_VERILOG_VERSION=${ICARUS_VERILOG_VERSION}
WORKDIR /usr/src/iverilog
RUN git clone https://github.com/steveicarus/iverilog.git --depth=1 --branch v${ICARUS_VERILOG_VERSION} . \
    && sh autoconf.sh \
    && ./configure \
    && make -s ${MAKE_JOBS} \
    && make -s install \
    && rm -r /usr/src/iverilog

# make sources available in docker image - one copy per python version
COPY . /src