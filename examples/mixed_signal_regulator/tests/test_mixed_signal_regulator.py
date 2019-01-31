import cocotb
from cocotb.clock import Clock
from cocotb.regression import TestFactory
from cocotb.triggers import Timer, NextTimeStep
from cocotb.utils import get_sim_time

from collections import namedtuple

import datetime
import itertools
import logging
import matplotlib
import matplotlib.pyplot as plt


PlotDataset = namedtuple('PlotDataset', 'time, trim, voltage, current')

class MixedSignal_TB(object):

    def __init__(self, dut):
        self.dut = dut
        self.analog_probe = dut.i_analog_probe
        self.bittogglestream = itertools.cycle(range(2))  # toggle between 0 and 1
    
    def probe_values(self):
        """Collect data from *analog_probe* of class."""
        voltage = self.analog_probe.voltage.value
        current = self.analog_probe.current.value
        return PlotDataset(time=get_sim_time(units='ns'),
                           trim=self.dut.trim_val.value.signed_integer,
                           voltage=voltage,
                           current=current)
    

@cocotb.coroutine
def run_test(dut):
    """Run test for mixed signal simulation."""
    
    tb = MixedSignal_TB(dut)

    node = "mixed_signal_regulator.i_regulator.vout"
    
    nodes_to_probe = [
        # "mixed_signal_regulator.node1",  # NOTE: doesn't work in cocotb 1.0.1, because of nettype probably
        "mixed_signal_regulator.i_regulator.vout",
    ]  #; list of hierarchical nodes to probe
     
    @cocotb.coroutine
    def get_single_sample(node):
        """Measure a single voltage/current pair on *node*."""
        toggle = next(tb.bittogglestream)
        tb.dut.i_analog_probe.node_to_probe <= node
        tb.analog_probe.probe_voltage_toggle <= toggle
        tb.analog_probe.probe_current_toggle <= toggle
        yield Timer(5, units='ps')  # NOTE: needs some time for some reason
        dataset = tb.probe_values()
        tb.dut._log.debug(f"trim value={tb.dut.trim_val.value.signed_integer}: {tb.analog_probe.node_to_probe}={dataset.voltage} V, {dataset.current} A")
        return dataset
        
    @cocotb.coroutine
    def get_sample_data(nodes, num=1, delay_ns=1):
        """For all *nodes*, get *num* samples, spaced *delay_ns* apart."""
        if not isinstance(nodes, list):  # single element? make it a list
            _nodes = [nodes]
        else:
            _nodes = nodes
        datasets = []
        for idx in range(num):
            for node in _nodes:
                dataset = yield get_single_sample(node)
                datasets.append(dataset)
                if num > 1:
                    yield Timer(delay_ns, units='ns')
        return datasets

    @cocotb.coroutine
    def do_trimming(node, target_volt, trim_min, trim_max):
        """Calculate best trimming for *target_volt* within range [*trim_min*..*trim_max*].
        Assumes a linear behaviour.
        """
        tb.dut.trim_val <= trim_min
        yield Timer(7, units='ns')
        sample = yield get_single_sample(node)
        val_min = sample.voltage
        tb.dut.trim_val <= trim_max
        yield Timer(7, units='ns')
        sample = yield get_single_sample(node)
        val_max = sample.voltage
        if target_volt > val_max:
            tb.dut._log.debug(f"target_volt={target_volt} > val_max={val_max}, returning trim_max={trim_max}")
            return trim_max
        if target_volt < val_min:
            tb.dut._log.debug(f"target_volt={target_volt} < val_min={val_min}, returning trim_min={trim_min}")
            return trim_min
        trim_diff = trim_max - trim_min
        val_diff = val_max - val_min
        ratio = trim_diff/val_diff
        target_trim = (target_volt-val_min)*ratio + trim_min
        return target_trim
        
    probedata = []

    dummy = yield get_single_sample(node)  # FIXME: why is this dummy read needed? Because of $cds_get_analog_value?

    tb.dut._log.setLevel(logging.DEBUG)

    # show manual trimming
    tb.dut.vdd_val <= 7.77
    tb.dut.vss_val <= 0.0
    tb.dut.trim_val <= 0
    yield Timer(7, units='ns')
    tb.dut._log.info(f"trim_val={tb.dut.trim_val.value.signed_integer}, vdd={tb.dut.vdd_val.value} V")
    
    datasets = yield get_sample_data(node)
    probedata.extend(datasets)
    
    tb.dut.trim_val <= 3
    yield Timer(7, units='ns')
    tb.dut._log.info(f"trim_val={tb.dut.trim_val.value.signed_integer}, vdd={tb.dut.vdd_val.value} V")
    datasets = yield get_sample_data(node)
    probedata.extend(datasets)
    
    tb.dut.trim_val <= -5
    yield Timer(7, units='ns')
    tb.dut._log.info(f"trim_val={tb.dut.trim_val.value.signed_integer}, vdd={tb.dut.vdd_val.value} V")
    datasets = yield get_sample_data(node)
    probedata.extend(datasets)

    # show automatic trimming
    target_volt = 3.013
    print(f"test_mixed_signal_regulator.py ({now_utc()}): Running trimming algorithm for target voltage {target_volt:.3} V")
    best_trim_float = yield do_trimming(node, target_volt, trim_min=-4, trim_max=4)
    best_trim_rounded = round(best_trim_float)
    tb.dut.trim_val <= best_trim_rounded
    yield Timer(7, units='ns')    
    trimmed_data = yield get_single_sample(node)
    trimmed_volt = trimmed_data.voltage
    print((f"test_mixed_signal_regulator.py ({now_utc()}): Determined best trimming value to be {best_trim_rounded} "
           f"which gives a trimmed voltage of {trimmed_volt:.3} V (difference to target={trimmed_volt-target_volt:.3} V)"))
    
    mpl_plot_data(dut=tb.dut, datasets=probedata, analog_probe=tb.analog_probe, graphfile="mixed_signal_regulator.png")

    
# register the test
factory = TestFactory(run_test)
factory.generate_tests()


def mpl_plot_data(dut, datasets, analog_probe, graphfile="cocotb_plot.png"):
    """Plot and save a graph with voltage and current over trim value."""
    
    time, trim, voltage, current = zip(*datasets)
    
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_title(f"Probed node: {analog_probe.node_to_probe}")
    ax1.set_xlabel("trim")
    ax1.set_ylabel("Voltage (V)", color=color)
    ax1.plot(trim, voltage, color=color, marker='.', markerfacecolor='black', linewidth=1)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.axhline(linestyle=':', color='gray')
    
    ax2 = ax1.twinx()  # instantiate a second axis that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel("Current (A)", color=color)  # we already handled the x-label with ax1
    ax2.plot(trim, current, color=color, marker='.', markerfacecolor='black', linewidth=1)
    ax2.tick_params(axis='y', labelcolor=color)
    
    # FIXME mpl_align_yaxis(ax1, 0, ax2, 0)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 8)
    
    dut._log.info(f"Writing file {graphfile}")
    fig.savefig(graphfile)

    
def mpl_align_yaxis(ax1, v1, ax2, v2):
    """Adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1."""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    mpl_adjust_yaxis(ax2,(y1-y2)/2,v2)
    mpl_adjust_yaxis(ax1,(y2-y1)/2,v1)

    
def mpl_adjust_yaxis(ax,ydif,v):
    """Shift axis ax by ydiff, maintaining point v at the same location."""
    inv = ax.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, ydif))
    miny, maxy = ax.get_ylim()
    miny, maxy = miny - v, maxy - v
    if -miny>maxy or (-miny==maxy and dy > 0):
        nminy = miny
        nmaxy = miny*(maxy+dy)/(miny+dy)
    else:
        nmaxy = maxy
        nminy = maxy*(miny+dy)/(maxy+dy)
    ax.set_ylim(nminy+v, nmaxy+v)


def now_utc():
    """Return ISO8601 date in UTC."""
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0).isoformat().replace("+00:00", "Z")
