#######
Logging
#######

Cocotb extends the Python :any:`logging` library. Each DUT, monitor, driver, and
scoreboard (as well as any other function using the coroutine decorator)
implements its own logging object, and each can be set to its own
logging level. Within a DUT, each hierarchical object can also have individual
logging levels set.

When logging HDL objects, beware that ``_log`` is the preferred way to use
logging (FIXME: expand). This helps minimize the change of name collisions of an HDL log
component with the Python logging functionality.

Log printing levels can also be set on a per-object basis.

.. code-block:: python3

        class EndianSwapperTB(object):
            def __init__(self, dut, debug=False):
                self.dut = dut
                self.stream_in = AvalonSTDriver(dut, "stream_in", dut.clk)
                self.stream_in_recovered = AvalonSTMonitor(
                    dut, "stream_in", dut.clk, callback=self.model
                )

                # Set verbosity on our various interfaces
                level = logging.DEBUG if debug else logging.WARNING
                self.stream_in.log.setLevel(level)
                self.stream_in_recovered.log.setLevel(level)
                self.dut.reset_n._log.setLevel(logging.DEBUG)

And when the logging is actually called

.. code-block:: python3

        class AvalonSTPkts(BusMonitor):
            ...

            @coroutine
            def _monitor_recv(self):
                ...
                self.log.info("Received a packet of %d bytes" % len(pkt))


        class Scoreboard(object):
            ...

            def add_interface(self):
                ...
                self.log.info("Created with reorder_depth %d" % reorder_depth)


        class EndianSwapTB(object):
            ...

            @cocotb.coroutine
            def reset():
                self.dut._log.debug("Resetting DUT")


will display as something like

.. code-block:: bash

    0.00ns INFO                   cocotb.scoreboard.endian_swapper_sv       scoreboard.py:177  in add_interface                   Created with reorder_depth 0
    0.00ns DEBUG                  cocotb.endian_swapper_sv           .._endian_swapper.py:106  in reset                           Resetting DUT
    160000000000000.00ns INFO     cocotb.endian_swapper_sv.stream_out           avalon.py:151  in _monitor_recv                   Received a packet of 125 bytes
