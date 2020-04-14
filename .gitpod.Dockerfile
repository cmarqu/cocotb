FROM gitpod/workspace-full-vnc

USER gitpod

# Install custom tools, runtime, etc. using apt-get
# For example, the command below would install "bastet" - a command line tetris clone:
#
# RUN sudo apt-get -q update && #     sudo apt-get install -yq bastet && #     sudo rm -rf /var/lib/apt/lists/*
#
# More information: https://www.gitpod.io/docs/config-docker/

# Install custom tools, runtime, etc.
RUN sudo apt-get update \
    && sudo apt-get install -y \
        swig \
    && rm -rf /var/lib/apt/lists/*


# Simulation
ARG ICARUS_VERILOG_VERSION=10_2

RUN sudo apt-get -q update && sudo apt-get install -yq \
       python3-dev \
       python3 \
    && sudo rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip \
    && g++ --version

ARG PYTHON_VERSION=3.7.7
RUN PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install ${PYTHON_VERSION}

# Icarus Verilog
ENV ICARUS_VERILOG_VERSION=${ICARUS_VERILOG_VERSION}
WORKDIR /usr/src/iverilog
RUN git clone https://github.com/steveicarus/iverilog.git --depth=1 --branch v${ICARUS_VERILOG_VERSION} . \
    && cd iverilog \
    && sh autoconf.sh \
    && ./configure --prefix ${HOME} \
    && make -s ${MAKE_JOBS} \
    && make -s install \
    && cd ..

# make sources available in docker image - one copy per python version
COPY . /src

USER gitpod