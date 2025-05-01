override SIM := verilator
export LD_LIBRARY_PATH := $(shell cocotb-config --prefix)/cocotb/libs:$(LD_LIBRARY_PATH)
PYTHON := $(shell which python3)
COCOTB := $(shell cocotb-config --makefiles)/Makefile.sim
include $(COCOTB)

EXTRA_ARGS += --trace --trace-fst --trace-structs

MODULE = tb_night_rider

TOPLEVEL = night_rider_fsm

VERILOG_SOURCES = $(abspath src/top.v)

export PYTHONPATH := $(PWD)/tb:$(PYTHONPATH)

.PHONY: all

all: sim