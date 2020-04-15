FROM gitpod/workspace-full-vnc

USER gitpod

# Install custom tools, runtime, etc. using apt-get
# For example, the command below would install "bastet" - a command line tetris clone:
#
# RUN sudo apt-get -q update && #     sudo apt-get install -yq bastet && #     sudo rm -rf /var/lib/apt/lists/*
#
# More information: https://www.gitpod.io/docs/config-docker/

# Install custom tools, runtime, etc.

ARG PYTHON_VERSION=3.8.2
RUN rm -rf ${HOME}.pyenv/versions/${PYTHON_VERSION}
RUN PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install ${PYTHON_VERSION}
RUN pyenv global ${PYTHON_VERSION}

RUN pip3 install --upgrade pip

RUN brew install gperf flex bison

ARG MAKE_JOBS=-j8

# Icarus Verilog
ARG ICARUS_VERILOG_BRANCH=v10_2
ENV ICARUS_VERILOG_BRANCH=${ICARUS_VERILOG_BRANCH}
WORKDIR /usr/src/iverilog
USER root
RUN git clone https://github.com/steveicarus/iverilog.git --depth=1 --branch ${ICARUS_VERILOG_BRANCH} . \
    && sh autoconf.sh \
    && ./configure --prefix ${HOME} \
    && make -s ${MAKE_JOBS} \
    && make -s install \
    && cd ..
USER gitpod

# Verilator 
ARG VERILATOR_BRANCH=master
ENV VERILATOR_BRANCH=${VERILATOR_BRANCH}
WORKDIR /usr/src/verilator
USER root
RUN git clone https://github.com/verilator/verilator.git --depth=1 --branch ${VERILATOR_BRANCH} . \
    && autoconf \
    && ./configure --prefix ${HOME} \
    && make -s ${MAKE_JOBS} \
    && make -s install \
    && cd ..
USER gitpod

# make sources available in docker image - one copy per Python version
COPY . /src
