import cocotb
from cocotb.clock import Clock
from cocotb.regression import TestFactory
from cocotb.triggers import Timer, NextTimeStep
from cocotb.utils import get_sim_time

import logging
import itertools

import matplotlib
import matplotlib.pyplot as plt

class MixedSignal_TB(object):

    def __init__(self, dut):
        self.dut = dut
        self.probenode = dut.i_analog_probe
        self.togglestream = itertools.cycle(range(2))  # toggle between 0 and 1
    
    def probe_values(self):
        """Collect data from *probenode* of class."""
        voltage = self.probenode.voltage.value
        current = self.probenode.current.value
        return (get_sim_time(units='ns'), voltage, current)  # FIXME: make this a NamedTuple
    

@cocotb.coroutine
def run_test(dut):
    """Run test for mixed signal simulation."""
    
    tb = MixedSignal_TB(dut)

    hierarchies_to_probe = [
        # "mixed_signal_regulator.node1",  # FIXME: doesn't work in cocotb 1.0.1, because of nettype probably
        "mixed_signal_regulator.i_regulator.vout",
    ]
     
    @cocotb.coroutine
    def get_single_sample():
        toggle = next(tb.togglestream)
        tb.probenode.probe_voltage_toggle <= toggle
        tb.probenode.probe_current_toggle <= toggle
        yield Timer(5, units='ps')  # NOTE: needs some time for some reason
        dataset = tb.probe_values()
        tb.dut._log.debug("{}={} V, {} A".format(tb.probenode, dataset[1], dataset[2]))
        return dataset
        
    @cocotb.coroutine
    def get_sample_data(steps=1, delay_ns=1, hierarchy_list=[]):
        data = []
        for idx in range(steps):
            for hierarchy in hierarchy_list:
                tb.dut.i_analog_probe.hierarchy_to_probe <= hierarchy
                dataset = yield get_single_sample()
                yield Timer(delay_ns, units='ns')
                data.append(dataset)
        return data
        
    probedata = []

    dummy = yield get_single_sample()  # FIXME: why is this needed? Because of $cds_get_analog_value?

    tb.dut._log.setLevel(logging.DEBUG)
    
    tb.dut.vdd_val <= 7.77
    tb.dut.vss_val <= 0.0
    tb.dut.trim_val <= 0
    yield Timer(5, units='ns')
    tb.dut._log.info("vdd={} V, trim_val={}".format(tb.dut.vdd_val.value, tb.dut.trim_val.value.signed_integer))
    
    data = yield get_sample_data(hierarchy_list=hierarchies_to_probe)
    probedata.extend(data)
    
    tb.dut.trim_val <= 3
    yield Timer(7, units='ns')
    tb.dut._log.info("vdd={} V, trim_val={}".format(tb.dut.vdd_val.value, tb.dut.trim_val.value.signed_integer))
    data = yield get_sample_data(hierarchy_list=hierarchies_to_probe)
    probedata.extend(data)
    
    tb.dut.trim_val <= -5
    yield Timer(7, units='ns')
    tb.dut._log.info("vdd={} V, trim_val={}".format(tb.dut.vdd_val.value, tb.dut.trim_val.value.signed_integer))
    data = yield get_sample_data(hierarchy_list=hierarchies_to_probe)
    probedata.extend(data)
        
    mpl_plot_data(dut=tb.dut, data=probedata, nodename=tb.probenode, graphfile="mixed_signal_regulator.png")
    # TODO: add trim value to matplotlib, make 3D-plot


# register the test
factory = TestFactory(run_test)
factory.generate_tests()


def mpl_plot_data(dut, data, nodename, graphfile="mixed_signal.png"):
    """Plot and save a graph with voltage and current over time."""
    
    time, voltage, current = zip(*data)
    
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_title('Node {}'.format(nodename))
    ax1.set_xlabel('Time (ns)')
    ax1.set_ylabel('Voltage (V)', color=color)
    ax1.plot(time, voltage, color=color, marker='.', markerfacecolor='black', linewidth=1)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.axhline(linestyle=':', color='gray')
    
    ax2 = ax1.twinx()  # instantiate a second axis that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('Current (A)', color=color)  # we already handled the x-label with ax1
    ax2.plot(time, current, color=color, marker='.', markerfacecolor='black', linewidth=1)
    ax2.tick_params(axis='y', labelcolor=color)
    
    # FIXME mpl_align_yaxis(ax1, 0, ax2, 0)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(14, 8)
    
    dut._log.info("Writing file {}".format(graphfile))
    fig.savefig(graphfile)

    
def mpl_align_yaxis(ax1, v1, ax2, v2):
    """Adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    mpl_adjust_yaxis(ax2,(y1-y2)/2,v2)
    mpl_adjust_yaxis(ax1,(y2-y1)/2,v1)

    
def mpl_adjust_yaxis(ax,ydif,v):
    """Shift axis ax by ydiff, maintaining point v at the same location"""
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
