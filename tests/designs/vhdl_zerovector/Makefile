# Simulator configuration
# -----------------------
# simulator (modelsim is still 32-bit only)
SIM ?= modelsim
ARCH ?= i686
# language of toplevel module
TOPLEVEL_LANG = vhdl
# VHDL language version
VCOM_ARGS += -2008
# simulation time precision
SIM_ARGS += -t ns

PWD=$(shell pwd)
COCOTB?=$(PWD)/../../..

ifneq ($(filter $(SIM),ius xcelium),)
    SIM_ARGS += -v93
endif


# Preparations
# ------------
TOPLEVEL := vhdl_zerovector
MODULE = test_vhdl_zerovector
VHDL_SOURCES = $(COCOTB)/tests/designs/vhdl_zerovector/vhdl_zerovector.vhdl



# Cocotb inclusions
# -----------------
include $(shell cocotb-config --makefiles)/Makefile.sim
