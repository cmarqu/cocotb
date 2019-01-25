# Override this variable to use a VHDL toplevel instead of (System)Verilog
TOPLEVEL_LANG ?= verilog

SIM?=ius

TOPLEVEL = mixed_signal

PWD=$(shell pwd)
COCOTB=$(PWD)/../../..

ifeq ($(OS),Msys)
    WPWD=$(shell sh -c 'pwd -W')
else
    WPWD=$(shell pwd)
endif

VERILOG_SOURCES += $(WPWD)/../hdl/resistor.vams
VERILOG_SOURCES += $(WPWD)/../hdl/capacitor.vams

ifeq ($(SIM),$(filter $(SIM),ius xcelium))
    VERILOG_SOURCES += $(WPWD)/../hdl/analog_probe_cadence.sv
#FIXME    VERILOG_SOURCES += $(WPWD)/../hdl/mixed_signal_resistor_cadence.sv
    VERILOG_SOURCES += $(WPWD)/../hdl/mixed_signal_rescap_cadence.sv
    SIM_ARGS += -timescale 1ns/1ps
    SIM_ARGS += -reflib ${AMSHOME}/tools/affirma_ams/etc/connect_lib/connectLib
    SIM_ARGS += -discipline logic
    #SIM_ARGS += -dresolution
    SIM_ARGS += -amsconnrules CR_full_fast
    SIM_ARGS += -ieinfo
    SIM_ARGS += run.scs
    SIM_ARGS += $(EXTRA_SIM_ARGS)
else
    $(error "This example does not have support for for SIM=$(SIM)")
endif

ifeq ($(TOPLEVEL_LANG),verilog)
else ifeq ($(TOPLEVEL_LANG),vhdl)
    $(error "VHDL toplevel not yet implemented")
    VHDL_SOURCES += $(WPWD)/../hdl/mixed_signal.vhdl
else
    $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif


MODULE=test_mixed_signal

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim

