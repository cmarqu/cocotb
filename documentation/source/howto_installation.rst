.. _installation:

#################
Installing cocotb
#################

**************
Pre-requisites
**************

Cocotb has the following requirements:

* Python 2.7, Python 3.5+ (recommended)
* Python-dev packages
* GCC and associated development packages
* GNU Make
* A Verilog or VHDL simulator, depending on your RTL source code

  
********************
Installation via PIP
********************

.. versionadded:: 1.2

Cocotb can be installed by running

.. code-block:: bash

    pip3 install cocotb

or

.. code-block:: bash

    pip install cocotb

For user local installation follow the
`pip User Guide <https://https://pip.pypa.io/en/stable/user_guide/#user-installs/>`_.

To install the development version of cocotb:

.. code-block:: bash

    git clone https://github.com/cocotb/cocotb
    pip install -e ./cocotb


*************************
Native Linux Installation
*************************

The following instructions will allow building of the cocotb libraries
for use with a 64-bit native simulator.

If a 32-bit simulator is being used then additional steps are needed, please see
`our Wiki <https://github.com/cocotb/cocotb/wiki/Tier-2-Setup-Instructions>`_.

Debian/Ubuntu-based

.. code-block:: bash

    sudo apt-get install git make gcc g++ swig python-dev

RedHat-based

.. code-block:: bash

    sudo yum install gcc gcc-c++ libstdc++-devel swig python-devel


********************
Windows Installation
********************

Download the MinGW installer from https://osdn.net/projects/mingw/releases/.

Run the GUI installer and specify a directory you would like the environment
installed in. The installer will retrieve a list of possible packages, when this
is done press "Continue". The MinGW Installation Manager is then launched.

The following packages need selecting by checking the tick box and selecting
"Mark for installation"

.. code-block:: bash

    Basic Installation
      -- mingw-developer-tools
      -- mingw32-base
      -- mingw32-gcc-g++
      -- msys-base

From the Installation menu then select "Apply Changes", in the next dialog
select "Apply".

When installed a shell can be opened using the "msys.bat" file located under
the <install_dir>/msys/1.0/

Python can be downloaded from https://www.python.org/downloads/windows/.
Run the installer and download to your chosen location.

It is beneficial to add the path to Python to the Windows system ``PATH`` variable
so it can be used easily from inside Msys.

Once inside the Msys shell commands as given here will work as expected.


**************
macOS Packages
**************

You need a few packages installed to get cocotb running on macOS.
Installing a package manager really helps things out here.

`Brew <https://brew.sh/>`_ seems to be the most popular, so we'll assume you have that installed.

.. code-block:: bash

    brew install python icarus-verilog gtkwave
