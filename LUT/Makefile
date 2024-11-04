SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl

VHDL_SOURCES = ./vhdl/sincos_lut.vhd

SIM_ARGS += --wave=dump.ghw --vcd=dump.vcd

TOPLEVEL := sincos_lut
MODULE := lut_tb

include $(shell cocotb-config --makefiles)/Makefile.sim
