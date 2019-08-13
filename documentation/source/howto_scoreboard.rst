############################################
Using a Scoreboard to Track Testbench Errors
############################################

The :class:`.Scoreboard` class is used to compare the actual outputs to
expected outputs. Monitors are added to the scoreboard for the actual outputs,
and the expected outputs can be either a simple list, or a function that
provides a transaction. Here is some code from the ``dff`` example, similar to
above with the scoreboard added.

.. code-block:: python3

    class DFF_TB(object):
        def __init__(self, dut, init_val):
            self.dut = dut

            # Create input driver and output monitor
            self.input_drv = BitDriver(dut.d, dut.c, input_gen())
            self.output_mon = BitMonitor("output", dut.q, dut.c)

            # Create a scoreboard on the outputs
            self.expected_output = [init_val]
            self.scoreboard = Scoreboard(dut)
            self.scoreboard.add_interface(self.output_mon, self.expected_output)

            # Reconstruct the input transactions from the pins
            # and send them to our 'model'
            self.input_mon = BitMonitor("input", dut.d, dut.c, callback=self.model)
