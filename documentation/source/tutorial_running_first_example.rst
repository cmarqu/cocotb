##########################
Running your first Example
##########################

Assuming you have installed cocotb as described in :doc:`/howto_installation`,
the following lines are all you need to run a first simulation with cocotb:

.. code-block:: bash

    git clone https://github.com/cocotb/cocotb
    cd cocotb/examples/endian_swapper/tests
    make

Selecting a different simulator is as easy as:

.. code-block:: bash

    make SIM=vcs


********************************
Running the same example as VHDL
********************************

The :doc:`/endian_swapper` example includes both a VHDL and a Verilog RTL implementation.
The cocotb testbench can execute against either implementation using VPI for
Verilog and VHPI/FLI for VHDL.  To run the test suite against the VHDL
implementation use the following command (a VHPI or FLI capable simulator must
be used):

.. code-block:: bash

    make SIM=ghdl TOPLEVEL_LANG=vhdl
