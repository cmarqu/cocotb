.. _internals:

*********
Internals
*********


.. _internals-miscellaneous:

Miscellaneous
=============

HDL names starting with an underscore
-------------------------------------

cocotb uses names starting with an underscore for internal purposes.
This means that if you have such names in your SystemVerilog code
(e.g. ``reg _underscore_name;``), you cannot directly access them.

Instead, you have to handle those signals specially like in the following example:

.. code-block:: python3

    # need to fill in _sub_handles
    _ = dir(dut)
    dut._sub_handles["_underscore_name"] <= 1
    yield Timer(1, 'ns')
    assert dut._sub_handles["_underscore_name"].value == 1
