import cocotb
from cocotb.result import TestFailure
from cocotb.triggers import Timer


@cocotb.test()
async def test_long_signal(dut):
    """ Write and read a normal signal (longer than 0)."""
    await Timer(1, "ns")
    dut.data_in <= 0x5
    await Timer(1, "ns")

    if dut.data_out != 0x5:
        raise TestFailure("Failed to readback dut.data_out")


@cocotb.test()
async def test_read_zero_signal(dut):
    """ Read a zero vector. It should always read 0."""
    await Timer(1, "ns")
    if dut.Cntrl_out != 0:
        raise TestFailure("Failed to readback dut.Cntrl_out")


@cocotb.test()
async def test_write_zero_signal_with_0(dut):
    """ Write a zero vector with 0."""
    await Timer(1, "ns")
    dut.Cntrl_out <= 0x0
    await Timer(1, "ns")
    if dut.Cntrl_out != 0:
        raise TestFailure("Failed to readback dut.Cntrl_out")


@cocotb.test()
async def test_write_zero_signal_with_1(dut):
    """ Write a zero vector with 1. Should catch a "out of range" exception."""
    await Timer(1, "ns")

    try:
        dut.Cntrl_out <= 0x1
    except OverflowError:
        pass
    else:
        assert False, "Exception did not occur"
