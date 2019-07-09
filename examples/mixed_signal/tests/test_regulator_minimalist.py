import cocotb
from cocotb.triggers import Timer

bittoggle = 0

@cocotb.test()
def test_trim(hdl_tb):
    probed_node = "tb_regulator.i_regulator.i_regulator_block.vout"
    target_volt = 3.03
    hdl_tb.vdd_val <= 7.7  # "signal assignment"
    hdl_tb.vss_val <= 0.0
    print(f"Running automatic trimming algorithm for target voltage {target_volt} V")
    best_trim = yield find_trim_val(hdl_tb, probed_node, target_volt, trim_val_node=hdl_tb.trim_val)
    print(f"Best trimming value is {best_trim}")
    # measure back
    hdl_tb.trim_val <= best_trim
    yield Timer(1, units='ns')
    trimmed_volt = yield get_single_sample(hdl_tb, probed_node)
    print(f"Trimmed voltage is {trimmed_volt} V (difference to target is {trimmed_volt-target_volt} V)")

# --------------------------------------------------------------------------------

@cocotb.coroutine
def get_single_sample(hdl_tb, node):
    """Measure voltage on *node*."""
    yield Timer(1, units='ns')  # let trim_val take effect
    hdl_tb.i_analog_probe.node_to_probe <= node
    global bittoggle
    bittoggle = ~bittoggle
    hdl_tb.i_analog_probe.probe_voltage_toggle <= bittoggle
    yield Timer(5, units='ps')  # measuring needs some time too
    hdl_tb._log.info(hdl_tb.i_analog_probe.voltage.value)
    return hdl_tb.i_analog_probe.voltage.value

@cocotb.coroutine
def find_trim_val(hdl_tb, probed_node, target_volt, trim_val_node):
    """Calculate best trimming value. Assumes a linear behaviour."""
    trim_min = -2**(trim_val_node.value.n_bits-1)  # two's complement
    trim_max =  2**(trim_val_node.value.n_bits-1)-1
    trim_val_node <= trim_min
    volt_min = yield get_single_sample(hdl_tb, probed_node)
    trim_val_node <= trim_max
    volt_max = yield get_single_sample(hdl_tb, probed_node)
    slope = (trim_max-trim_min)/(volt_max-volt_min)
    target_trim = round((target_volt-volt_min)*slope + trim_min)
    target_trim_clamped = min(trim_max, max(trim_min, target_trim))
    return target_trim_clamped
