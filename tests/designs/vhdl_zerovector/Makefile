# Copyright cocotb contributors
# Licensed under the Revised BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-3-Clause
#
# Simulator (modelsim is still 32-bit only)
SIM ?= modelsim
ifneq ($(filter $(SIM), modelsim),)
    ARCH ?= i686
endif

# Language of toplevel module
TOPLEVEL_LANG = vhdl

ifneq ($(filter $(SIM), questa modelsim),)
    # VHDL language version
    VCOM_ARGS += -2008
    # simulation time precision
    SIM_ARGS += -t ns
endif

ifneq ($(filter $(SIM),ius xcelium),)
    SIM_ARGS += -v93
endif

PWD=$(shell pwd)
COCOTB?=$(PWD)/../../..


# Preparations
TOPLEVEL := vhdl_zerovector
MODULE = test_vhdl_zerovector
VHDL_SOURCES = $(COCOTB)/tests/designs/vhdl_zerovector/vhdl_zerovector.vhdl


# Cocotb inclusions
include $(shell cocotb-config --makefiles)/Makefile.sim
