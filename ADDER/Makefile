SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl

VHDL_SOURCES = ./vhdl/*

SIM_ARGS += --wave=dump.ghw --vcd=dump.vcd

TOPLEVEL := adder
MODULE := main

include $(shell cocotb-config --makefiles)/Makefile.sim
