The cocotb ``mixed_signal_regulator`` Testbench
===============================================

This is a `cocotb <https://cocotb.readthedocs.io>`_ testbench :mod:`test_mixed_signal_regulator`
for the design ``mixed_signal_regulator``.

The design consists of a regulator model written in SystemVerilog (instance name ``i_regulator``), and load resistor
(instance name ``i_resistor``).

The testbench has both an HDL part and a Python/cocotb part.

The HDL part contains a probe module for analog values (instance name ``i_analog_probe``) which can capture
the voltage and current of a node specified by ``node_to_probe`` (a string containing a hierarchical path).
The capturing occurs whenever there is an edge on logic signals ``probe_voltage_toggle`` or ``probe_current_toggle``.
The captured values can be read on real-value signals ``voltage`` and ``current`` in this module.

Here is the capture code for ``voltage`` with the "user-interface" highlighted:

.. literalinclude:: ../../hdl/analog_probe_cadence.sv
   :caption: analog_probe_cadence.sv
   :language: systemverilog
   :lines: 3-15
   :emphasize-lines: 1-4
   :dedent: 2


The cocotb part of the testbench provides functions to:

* do the sampling of voltage and current of a given node (:meth:`~.get_sample_data()`),
* trim the regulator as close as possible to a target voltage within a given trim value range ( :meth:`~.find_trim_val()`), and
* plot the sampled data to a file (:meth:`~.plot_data()`).

.. todo:: Expand


Reference Documentation
-----------------------

cocotb Testbench
~~~~~~~~~~~~~~~~

.. currentmodule:: test_mixed_signal_regulator

.. autoclass:: MixedSignal_TB
               
    .. automethod:: get_sample_data(nodes, num=1, delay_ns=1)
    .. automethod:: find_trim_val(probed_node, target_volt, trim_val_node, trim_val_signed=True, trim_val_min=None, trim_val_max=None)
    .. automethod:: plot_data(datasets, graphfile="cocotb_plot.png")

                    
.. autoclass:: PlotDataset
    :show-inheritance:
    :members:
    :member-order: bysource
               
                    
Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
