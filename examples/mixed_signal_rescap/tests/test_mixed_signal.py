import cocotb
from cocotb.clock import Clock
from cocotb.regression import TestFactory
from cocotb.triggers import Timer
from cocotb.utils import get_sim_time

from itertools import cycle

import matplotlib
import matplotlib.pyplot as plt

class MixedSignal_TB(object):

    def __init__(self, dut):
        self.dut = dut
        self.probenode = dut.i_analog_probe
        self.togglestream = cycle(range(2))  # toggle between 0 and 1
    
    def collect_data(self):
        """Collect data from *probenode* of class."""
        voltage = self.probenode.voltage.value
        current = self.probenode.current.value
        self.dut._log.info("{}={} V  {} A".format(self.probenode, voltage, current))
        return (get_sim_time(units='ns'), voltage, current)
    

@cocotb.coroutine
def run_test(dut):
    """Run test for mixed signal simulation."""
    
    tb = MixedSignal_TB(dut)

    hierarchies_to_probe = ["mixed_signal.i_capacitor.p",
                            "mixed_signal.i_resistor.p",
    ]
     
    def get_single_sample():
        toggle = next(tb.togglestream)
        tb.probenode.probe_voltage_toggle <= toggle
        tb.probenode.probe_current_toggle <= toggle
        dataset = tb.collect_data()
        return dataset
        
    @cocotb.coroutine
    def get_sample_data_multi(steps=50, delay_ns=5, hierarchy_list=[]):
        data = []
        for idx in range(steps):
            for hierarchy in hierarchy_list:
                tb.dut.i_analog_probe.hierarchy_to_probe <= hierarchy
                dataset = get_single_sample()
                yield Timer(delay_ns, units='ns')
                data.append(dataset)
        return data
        
    probedata = []

    yield Timer(5, units='ns')
    
    tb.dut.vdd_val <= 5.55
    tb.dut.gnd_val <= 0.0
    tb.dut._log.info("Setting vdd={} V".format(tb.dut.vdd_val.value))

    data = yield get_sample_data_multi(steps=80, delay_ns=5, hierarchy_list=hierarchies_to_probe)
    probedata.extend(data)
    
    tb.dut.vdd_val <= -3.33
    tb.dut.gnd_val <= 0.0
    tb.dut._log.info("Setting vdd={} V".format(tb.dut.vdd_val.value))

    data = yield get_sample_data_multi(steps=80, delay_ns=5, hierarchy_list=hierarchies_to_probe)
    probedata.extend(data)
    
        
    mpl_plot_data(dut=tb.dut, data=probedata, nodename=tb.probenode)


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
    
    mpl_align_yaxis(ax1, 0, ax2, 0)
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
