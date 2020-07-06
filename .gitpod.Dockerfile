FROM gitpod/workspace-full-vnc

USER gitpod

## Install Python with --enable-shared
ARG PYTHON_VERSION=3.8.2
RUN rm -rf ${HOME}/.pyenv/versions/${PYTHON_VERSION}
RUN PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install ${PYTHON_VERSION}
RUN pyenv global ${PYTHON_VERSION}

RUN pip3 install --upgrade pip

# Install linters
RUN pip3 install -U flake8 pylint

# Re-synchronize the package index
RUN sudo apt-get update

# Install needed packages
RUN sudo apt-get install -y flex gnat gtkwave swig gperf
RUN sudo rm -rf /var/lib/apt/lists/*

## Install Icarus latest
RUN git clone https://github.com/steveicarus/iverilog.git icarus \
    && cd icarus \
    && autoconf \
    && ./configure \
    && make -j4 -s \
    && sudo make -s install \
    && cd .. \
    && rm -rf icarus
