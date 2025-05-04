override SIM := verilator
export LD_LIBRARY_PATH := $(shell cocotb-config --prefix)/cocotb/libs:$(LD_LIBRARY_PATH)
PYTHON := $(shell which python3)
COCOTB := $(shell cocotb-config --makefiles)/Makefile.sim
include $(COCOTB)

EXTRA_ARGS += --trace --trace-fst --trace-structs -DSIM

MODULE = tb_night_rider

TOPLEVEL = top

VERILOG_SOURCES = $(abspath $(wildcard src/*.v))

export PYTHONPATH := $(PWD)/tb:$(PYTHONPATH)

.PHONY: all

all: sim