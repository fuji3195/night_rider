override SIM := verilator
PYTHON := $(shell which python3)
COCOTB := $(shell cocotb-config --makefiles)/Makefile.sim
include $(COCOTB)

EXTRA_ARGS += --trace --trace-fst --trace-structs

MODULE = test

TOPLEVEL = test

VERILOG_SOURCES = $(abspath src/test.v)

export PYTHONPATH := $(PWD)/tb:$(PYTHONPATH)

.PHONY: all

all: sim