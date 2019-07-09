import cocotb
from cocotb.regression import TestFactory
from cocotb.triggers import Timer
from cocotb.utils import get_sim_time

from collections import namedtuple

import datetime
import itertools
import logging
import matplotlib
import matplotlib.pyplot as plt


Dataset = namedtuple('Dataset', 'time, trim, voltage, current')

class MixedSignal_TB(object):
    """Class for collecting testbench objects.

    Args:
        dut: The toplevel of the design-under-test.
            In this mixed cocotb/HDL testbench environment, it is the HDL testbench.
        settling_time_ns (int): Time in nanoseconds to wait before sample is taken.
    """

    def __init__(self, dut, settling_time_ns=1):
        self.dut = dut
        self.settling_time_ns = settling_time_ns
        self.analog_probe = dut.i_analog_probe  #: The instance name of the analog probe module.
        self._bittogglestream = itertools.cycle(range(2))  #: Produce stream that toggles between ``0`` and ``1``.
    
    def probe_values(self):
        """Collect data from instance pointed to by :attr:`analog_probe`."""
        voltage = self.analog_probe.voltage.value
        current = self.analog_probe.current.value
        return Dataset(time=get_sim_time(units='ns'),
                       trim=self.dut.trim_val.value.signed_integer,
                       voltage=voltage,
                       current=current)
    
    @cocotb.coroutine
    def _get_single_sample(self, node):
        """Measure a single voltage/current pair on *node*."""
        toggle = next(self._bittogglestream)
        self.dut.i_analog_probe.node_to_probe <= node
        self.analog_probe.probe_voltage_toggle <= toggle
        self.analog_probe.probe_current_toggle <= toggle
        yield Timer(5, units='ps')  # NOTE: needs some time for some reason
        dataset = self.probe_values()
        self.dut._log.debug(f"trim value={self.dut.trim_val.value.signed_integer}: {self.analog_probe.node_to_probe}={dataset.voltage} V, {dataset.current} A")
        return dataset
        
    @cocotb.coroutine
    def get_sample_data(self, nodes, num=1, delay_ns=1):
        """For all *nodes*, get *num* samples, spaced *delay_ns* apart.

        Yields:
            list: List (*num* samples long) of :any:`Dataset` for all *nodes*.
        """
        if not isinstance(nodes, list):  # single element? make it a list
            _nodes = [nodes]
        else:
            _nodes = nodes
        datasets = []
        for idx in range(num):
            for node in _nodes:
                dataset = yield self._get_single_sample(node)
                datasets.append(dataset)
                if num > 1 and idx < num:
                    yield Timer(delay_ns, units='ns')
        return datasets

    @cocotb.coroutine
    def find_trim_val(self, probed_node, target_volt, trim_val_node, trim_val_repr='TWOS_COMPLEMENT'):
        """Calculate best trimming value for *target_volt*.
        Assumes a linear behaviour.

        Args:
            probed_node: The node to probe for the trimmed voltage.
            target_volt (float): The target voltage at *probed_node*.
            trim_val_node: The node to apply the trim value to.
            trim_val_repr (str, optional): String indicating whether the *trim_val_node* has an
                'UNSIGNED' or 'TWOS_COMPLEMENT' representation.

        Yields:
            float: The calculated best value for *trim_val_node*.
        """
        # find trim_val_min/trim_val_max based on bit length:
        assert trim_val_repr in ('UNSIGNED', 'TWOS_COMPLEMENT')
        trim_val_min = min_val(trim_val_node, trim_val_repr)
        trim_val_max = max_val(trim_val_node, trim_val_repr)
        # the actual trimming procedure:
        trim_val_node <= trim_val_min
        yield Timer(self.settling_time_ns, units='ns')
        sample = yield self.get_sample_data(probed_node)
        volt_min = sample[0].voltage
        trim_val_node <= trim_val_max
        yield Timer(self.settling_time_ns, units='ns')
        sample = yield self.get_sample_data(probed_node)
        volt_max = sample[0].voltage
        if target_volt > volt_max:
            self.dut._log.debug(f"target_volt={target_volt} > volt_max={volt_max}, returning minimum trim value {trim_val_max}")
            return trim_val_max
        if target_volt < volt_min:
            self.dut._log.debug(f"target_volt={target_volt} < volt_min={volt_min}, returning maximum trim value {trim_val_min}")
            return trim_val_min
        slope = (trim_val_max - trim_val_min)/(volt_max - volt_min)
        target_trim = (target_volt-volt_min)*slope + trim_val_min
        return target_trim
        
    def plot_data(self, datasets, graphfile="cocotb_plot.png"):
        """Plot and save a graph to file *graphfile* with voltage and current over trim value (contained in *datasets*)."""
        
        time, trim, voltage, current = zip(*datasets)
        
        fig, ax1 = plt.subplots()
        color = 'tab:red'
        ax1.set_title(f"Probed node: {self.analog_probe.node_to_probe}")
        ax1.set_xlabel("trim")
        ax1.set_ylabel("Voltage (V)", color=color)
        ax1.plot(trim, voltage, color=color, marker='.', markerfacecolor='black', linewidth=1)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.axhline(linestyle=':', color='tab:gray')  # horizontal line at zero of ax1
        
        ax2 = ax1.twinx()  # instantiate a second axis that shares the same x-axis
        color = 'tab:blue'
        ax2.set_ylabel("Current (A)", color=color)  # we already handled the x-label with ax1
        ax2.plot(trim, current, color=color, marker='.', markerfacecolor='black', linewidth=1)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.axhline(linestyle=':', color='tab:gray')  # horizontal line at zero of ax2
        
        _mpl_align_yaxis(ax1, 0, ax2, 0)
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        fig.set_size_inches(14, 8)
        
        self.dut._log.info(f"Writing file {graphfile}")
        fig.savefig(graphfile)
    
    
@cocotb.coroutine
def run_test(dut):
    """Run test for mixed signal simulation."""
    
    tb = MixedSignal_TB(dut)

    node = "mixed_signal_regulator.i_regulator.vout"
    
    nodes_to_probe = [
        # "mixed_signal_regulator.node1",  # NOTE: doesn't work in cocotb 1.0.1, because of nettype probably
        "mixed_signal_regulator.i_regulator.vout",
    ]  #: list of hierarchical nodes to probe

    probedata = []

    dummy = yield tb.get_sample_data(node)  # NOTE: dummy read apparently needed because of $cds_get_analog_value

    tb.dut._log.setLevel(logging.DEBUG)

    # show manual trimming
    tb.dut.vdd_val <= 7.77
    tb.dut.vss_val <= 0.0
    
    tb.dut.trim_val <= 0
    yield Timer(tb.settling_time_ns, units='ns')
    tb.dut._log.info(f"trim_val={tb.dut.trim_val.value.signed_integer}, vdd={tb.dut.vdd_val.value} V")
    
    datasets = yield tb.get_sample_data(node)
    probedata.extend(datasets)
    
    tb.dut.trim_val <= 3
    yield Timer(tb.settling_time_ns, units='ns')
    tb.dut._log.info(f"trim_val={tb.dut.trim_val.value.signed_integer}, vdd={tb.dut.vdd_val.value} V")
    datasets = yield tb.get_sample_data(node)
    probedata.extend(datasets)
    
    tb.dut.trim_val <= -5
    yield Timer(tb.settling_time_ns, units='ns')
    tb.dut._log.info(f"trim_val={tb.dut.trim_val.value.signed_integer}, vdd={tb.dut.vdd_val.value} V")
    datasets = yield tb.get_sample_data(node)
    probedata.extend(datasets)

    tb.plot_data(datasets=probedata, graphfile="mixed_signal_regulator.png")

    # show automatic trimming
    target_volt = 3.013
    print(f"test_mixed_signal_regulator.py ({now_utc()}): Running trimming algorithm for target voltage {target_volt:.3} V")
    best_trim_float = yield tb.find_trim_val(probed_node=node, target_volt=target_volt, trim_val_node=tb.dut.trim_val)
    best_trim_rounded = round(best_trim_float)
    tb.dut.trim_val <= best_trim_rounded
    yield Timer(tb.settling_time_ns, units='ns')    
    datasets = yield tb.get_sample_data(node)
    trimmed_volt = datasets[0].voltage
    print((f"test_mixed_signal_regulator.py ({now_utc()}): Determined best trimming value to be {best_trim_rounded} "
           f"which gives a trimmed voltage of {trimmed_volt:.3} V (difference to target {trimmed_volt-target_volt:.3} V)"))
    
    
# register the test
factory = TestFactory(run_test)
factory.generate_tests()


# TODO: move to some utils package
def _mpl_align_yaxis(ax1, v1, ax2, v2):
    """Adjust *ax2* ylimit so that *v2* in *ax2* is aligned to *v1* in *ax1*."""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    _mpl_adjust_yaxis(ax2, (y1-y2)/2, v2)
    _mpl_adjust_yaxis(ax1, (y2-y1)/2, v1)

    
def _mpl_adjust_yaxis(ax, ydiff, v):
    """Shift axis *ax* by *ydiff*, maintaining point *v* at the same location."""
    inv = ax.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, ydiff))
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
    """Return current ISO8601 date and time in the UTC timezone."""
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0).isoformat().replace("+00:00", "Z")


# FIXME: use cocotb.binary.BinaryRepresentation?
def min_val(vector, representation='UNSIGNED'):
    """Return minimum value that can be stored in *vector* given its *representation*."""
    assert representation in ('UNSIGNED', 'TWOS_COMPLEMENT')
    if representation == 'TWOS_COMPLEMENT':
        return -2**(vector.value.n_bits-1)
    else:
        return 0


def max_val(vector, representation='UNSIGNED'):
    """Return maximum value that can be stored in *vector* given its *representation*."""
    assert representation in ('UNSIGNED', 'TWOS_COMPLEMENT')
    if representation == 'TWOS_COMPLEMENT':
        return 2**(vector.value.n_bits-1)-1
    else:
        return 2**(vector.value.n_bits-1)
