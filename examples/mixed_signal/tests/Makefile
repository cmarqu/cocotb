# Override this variable to use a VHDL toplevel instead of (System)Verilog
TOPLEVEL_LANG ?= verilog

# FIXME
TOPLEVEL ?= mixed_signal_rescap
#TOPLEVEL ?= mixed_signal_regulator

MODULE ?= test_$(TOPLEVEL)
#MODULE ?= test_$(TOPLEVEL)_minimalist

PWD = $(shell pwd)
COCOTB = $(PWD)/../../..

ifeq ($(OS),Msys)
    WPWD=$(shell sh -c 'pwd -W')
else
    WPWD=$(shell pwd)
endif


# Files

VERILOG_SOURCES += $(WPWD)/../hdl/resistor.vams
VERILOG_SOURCES += $(WPWD)/../hdl/capacitor.vams
VERILOG_SOURCES += $(WPWD)/../hdl/regulator.vams

ifeq ($(SIM),$(filter $(SIM),ius xcelium))
    VERILOG_SOURCES += $(WPWD)/../hdl/analog_probe_cadence.sv
    ifeq ($(TOPLEVEL_LANG),verilog)
        VERILOG_SOURCES += $(WPWD)/../hdl/nettypes_pkg.sv
        VERILOG_SOURCES += $(WPWD)/../hdl/mixed_signal_rescap_cadence.sv
        VERILOG_SOURCES += $(WPWD)/../hdl/mixed_signal_regulator_cadence.sv
    else ifeq ($(TOPLEVEL_LANG),vhdl)
        $(error "VHDL toplevel not yet implemented")
        VHDL_SOURCES += $(WPWD)/../hdl/mixed_signal_rescap_cadence.vhdl
        VHDL_SOURCES += $(WPWD)/../hdl/mixed_signal_regulator_cadence.vhdl
    else
        $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
    endif
else ifeq ($(SIM),vcs)
    VERILOG_SOURCES += $(WPWD)/../hdl/analog_probe_synopsys.sv
    ifeq ($(TOPLEVEL_LANG),verilog)
        VERILOG_SOURCES += $(WPWD)/../hdl/mixed_signal_rescap_synopsys.sv
        VERILOG_SOURCES += $(WPWD)/../hdl/mixed_signal_regulator_synopsys.sv
    else ifeq ($(TOPLEVEL_LANG),vhdl)
        $(error "VHDL toplevel not yet implemented")
        VHDL_SOURCES += $(WPWD)/../hdl/mixed_signal_rescap_synopsys.vhdl
        VHDL_SOURCES += $(WPWD)/../hdl/mixed_signal_regulator_synopsys.vhdl
    else
        $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
    endif
else
    $(error "This example does not have support for for SIM=$(SIM)")
endif


# Options

ifeq ($(SIM),$(filter $(SIM),ius xcelium))
    SIM_ARGS += -timescale 1ns/1ps
    SIM_ARGS += -reflib ${AMSHOME}/tools/affirma_ams/etc/connect_lib/connectLib
    SIM_ARGS += -discipline logic
    #SIM_ARGS += -dresolution
    SIM_ARGS += -amsconnrules CR_full_fast
    SIM_ARGS += -ieinfo
    SIM_ARGS += -ieinfo_log $(SIM_BUILD)/ams_ieinfo.log
    SIM_ARGS += -spectre_args "+lqtimeout 7200"
    SIM_ARGS += run.scs
    SIM_ARGS += $(EXTRA_SIM_ARGS)
else ifeq ($(SIM),vcs)
    SIM_ARGS += -xlrm coerce_nettype
else
    $(error "This example does not have support for for SIM=$(SIM)")
endif



include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim
