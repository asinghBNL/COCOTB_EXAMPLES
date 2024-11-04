SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl

VHDL_SOURCES = ./vhdl/*

SIM_ARGS += --wave=./output/dump.ghw --vcd=./output/dump.vcd

TOPLEVEL := adder
MODULE := main

include $(shell cocotb-config --makefiles)/Makefile.sim
