import cocotb
from cocotb.clock import Clock
from cocotb.regression import TestFactory
from cocotb.triggers import Timer
from cocotb.utils import get_sim_time

from collections import namedtuple

from itertools import cycle

import matplotlib
import matplotlib.pyplot as plt

Dataset = namedtuple('Dataset', 'time, voltage, current')

class MixedSignal_TB(object):

    def __init__(self, dut):
        self.dut = dut
        self.analog_probe = dut.i_analog_probe  #: The instance name of the analog probe module.
        self.togglestream = cycle(range(2))  # toggle between 0 and 1
    
    def probe_values(self):
        """Collect data from instance pointed to by :attr:`analog_probe`."""
        voltage = self.analog_probe.voltage.value
        current = self.analog_probe.current.value
        self.dut._log.info("{}={} V  {} A".format(self.analog_probe, voltage, current))
        return Dataset(time=get_sim_time(units='ns'),
                       voltage=voltage,
                       current=current)
    
    @cocotb.coroutine
    def _get_single_sample(self, node):
        toggle = next(self.togglestream)
        self.dut.i_analog_probe.node_to_probe <= node
        self.analog_probe.probe_voltage_toggle <= toggle
        self.analog_probe.probe_current_toggle <= toggle
        yield Timer(5, units='ps')  # NOTE: needs some time for some reason
        dataset = self.probe_values()
        self.dut._log.debug(f"{self.analog_probe.node_to_probe}={dataset.voltage} V, {dataset.current} A")
        return dataset
        
    @cocotb.coroutine
    def get_sample_data(self, steps=50, delay_ns=5, nodes=[]):
        datasets = []
        for idx in range(steps):
            for node in nodes:
                dataset = yield self._get_single_sample(node)
                yield Timer(delay_ns, units='ns')
                datasets.append(dataset)
        return datasets
        
    def plot_data(self, datasets, nodes, graphfile="cocotb_plot.png"):
        """Plot and save a graph to file *graphfile* with voltage and current value (contained in *datasets*)."""
        
        time, voltage, current = zip(*datasets)
    
        fig, ax1 = plt.subplots()
        color = 'tab:red'
        ax1.set_title(f"Probed nodes: {nodes}")
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
        
        self.dut._log.info("Writing file {}".format(graphfile))
        fig.savefig(graphfile)
        

@cocotb.coroutine
def run_test(dut):
    """Run test for mixed signal simulation."""
    
    tb = MixedSignal_TB(dut)

    nodes_to_probe = [
        "mixed_signal.i_resistor.p",
        "mixed_signal.i_capacitor.p",
    ]
     
    probedata = []

    dummy = yield tb.get_sample_data(nodes=nodes_to_probe)  # NOTE: dummy read apparently needed because of $cds_get_analog_value

    yield Timer(5, units='ns')
    
    tb.dut.vdd_val <= 5.55
    tb.dut.gnd_val <= 0.0
    tb.dut._log.info("Setting vdd={} V".format(tb.dut.vdd_val.value))

    data = yield tb.get_sample_data(steps=80, delay_ns=5, nodes=nodes_to_probe)
    probedata.extend(data)
    
    tb.dut.vdd_val <= -3.33
    tb.dut.gnd_val <= 0.0
    tb.dut._log.info("Setting vdd={} V".format(tb.dut.vdd_val.value))

    data = yield tb.get_sample_data(steps=80, delay_ns=5, nodes=nodes_to_probe)
    probedata.extend(data)
    
    tb.plot_data(datasets=probedata, nodes=nodes_to_probe, graphfile="mixed_signal.png")



# register the test
factory = TestFactory(run_test)
factory.generate_tests()

    
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
