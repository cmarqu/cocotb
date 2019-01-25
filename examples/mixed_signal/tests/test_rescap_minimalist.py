import cocotb
from cocotb.triggers import Timer


@cocotb.test()
def rescap_minimalist_test(dut):
    """Mixed signal resistor/capacitor simulation, minimalistic."""

    dut.vdd_val <= 7.7
    dut.vss_val <= 0.0

    dut.i_analog_probe.node_to_probe <= "tb_rescap.i_rescap.i_capacitor.p"

    yield Timer(50, units="ns")

    dut.i_analog_probe.probe_voltage_toggle <= 1
    dut.i_analog_probe.probe_current_toggle <= 1
    yield Timer(1, units="ns")
    dut._log.info(
        "dut.i_analog_probe={} V  {} A".format(
            dut.i_analog_probe.voltage.value, dut.i_analog_probe.current.value
        )
    )

    yield Timer(50, units="ns")

    dut.i_analog_probe.probe_voltage_toggle <= 0
    dut.i_analog_probe.probe_current_toggle <= 0
    yield Timer(1, units="ns")
    dut._log.info(
        "dut.i_analog_probe={} V  {} A".format(
            dut.i_analog_probe.voltage.value, dut.i_analog_probe.current.value
        )
    )

    yield Timer(50, units="ns")

    dut.i_analog_probe.probe_voltage_toggle <= 1
    dut.i_analog_probe.probe_current_toggle <= 1
    yield Timer(1, units="ns")
    dut._log.info(
        "dut.i_analog_probe={} V  {} A".format(
            dut.i_analog_probe.voltage.value, dut.i_analog_probe.current.value
        )
    )
