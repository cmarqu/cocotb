####################################
Creating your first cocotb Testbench
####################################

A typical cocotb testbench requires no additional HDL code (though nothing prevents you from adding testbench helper code).
The Design Under Test (DUT) is instantiated as the toplevel in the simulator
without any wrapper code.
Cocotb drives stimulus onto the inputs to the DUT and monitors the outputs
directly from Python.


*******************
Creating a Makefile
*******************

To create a cocotb test we typically have to create a Makefile.  Cocotb provides
rules which make it easy to get started.  We simply inform cocotb of the
source files we need compiling, the toplevel entity to instantiate and the
Python test script to load.

.. code-block:: makefile

    VERILOG_SOURCES = $(PWD)/submodule.sv $(PWD)/my_design.sv
    TOPLEVEL = my_design  # the module name in your Verilog or VHDL file
    MODULE = test_my_design  # the name of the Python test file
    include $(shell cocotb-config --makefiles)/Makefile.inc
    include $(shell cocotb-config --makefiles)/Makefile.sim

We would then create a file called ``test_my_design.py`` containing our tests.


***************
Creating a test
***************

The test is written in Python. Cocotb wraps your top level with the handle you
pass it. In this documentation, and most of the examples in the project, that
handle is ``dut``, but you can pass your own preferred name in instead. The
handle is used in all Python files referencing your RTL project. Assuming we
have a toplevel port called ``clk`` we could create a test file containing the
following:

.. code-block:: python3

    import cocotb
    from cocotb.triggers import Timer

    @cocotb.test()
    def my_first_test(dut):
        """Try accessing the design."""

        dut._log.info("Running test!")
        for cycle in range(10):
            dut.clk = 0
            yield Timer(1000)
            dut.clk = 1
            yield Timer(1000)
        dut._log.info("Running test!")

This will drive a square wave clock onto the ``clk`` port of the toplevel.


********************
Accessing the design
********************

When cocotb initialises it finds the top-level instantiation in the simulator
and creates a handle called ``dut``. Top-level signals can be accessed using the
"dot" notation used for accessing object attributes in Python. The same mechanism
can be used to access signals inside the design.

.. code-block:: python3

    # Get a reference to the "clk" signal on the top-level
    clk = dut.clk

    # Get a reference to a register "count"
    # in a sub-block "inst_sub_block"
    count = dut.inst_sub_block.count


***************************
Assigning values to signals
***************************

Values can be assigned to signals using either the
:attr:`~cocotb.handle.NonHierarchyObject.value` property of a handle object
or using direct assignment while traversing the hierarchy.

.. code-block:: python3

    # Get a reference to the "clk" signal and assign a value
    clk = dut.clk
    clk.value = 1

    # Direct assignment through the hierarchy
    dut.input_signal <= 12

    # Assign a value to a memory deep in the hierarchy
    dut.sub_block.memory.array[4] <= 2


The syntax ``sig <= new_value`` is a short form of ``sig.value = new_value``.
It not only resembles HDL-syntax, but also has the same semantics:
writes are not applied immediately, but delayed until the next write cycle.
Use ``sig.setimmediatevalue(new_val)`` to set a new value immediately
(see :meth:`~cocotb.handle.ModifiableObject.setimmediatevalue`).



***************************
Reading values from signals
***************************

Accessing the :attr:`~cocotb.handle.NonHierarchyObject.value` property of a handle object will return a :any:`BinaryValue` object.
Any unresolved bits are preserved and can be accessed using the :attr:`~cocotb.binary.BinaryValue.binstr` attribute,
or a resolved integer value can be accessed using the :attr:`~cocotb.binary.BinaryValue.integer` attribute.

.. code-block:: python3

    >>> # Read a value back from the DUT
    >>> count = dut.counter.value
    >>>
    >>> print(count.binstr)
    1X1010
    >>> # Resolve the value to an integer (X or Z treated as 0)
    >>> print(count.integer)
    42
    >>> # Show number of bits in a value
    >>> print(count.n_bits)
    6

We can also cast the signal handle directly to an integer:

.. code-block:: python3

    >>> print(int(dut.counter))
    42



***********************************************
Parallel and sequential execution of coroutines
***********************************************

.. code-block:: python3

    @cocotb.coroutine
    def reset_dut(reset_n, duration):
        reset_n <= 0
        yield Timer(duration)
        reset_n <= 1
        reset_n._log.debug("Reset complete")

    @cocotb.test()
    def parallel_example(dut):
        reset_n = dut.reset

        # This will call reset_dut sequentially
        # Execution will block until reset_dut has completed
        yield reset_dut(reset_n, 500)
        dut._log.debug("After reset")

        # Call reset_dut in parallel with this coroutine
        reset_thread = cocotb.fork(reset_dut(reset_n, 500)

        yield Timer(250)
        dut._log.debug("During reset (reset_n = %s)" % reset_n.value)

        # Wait for the other thread to complete
        yield reset_thread.join()
        dut._log.debug("After reset")

