import random

import cocotb
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock

from python.modules.adder import adder #python implementation of adder to test against

@cocotb.test()
async def main(dut):
    #initialize clock
    clock = Clock(dut.clk, 0.05, units="us")
    cocotb.start_soon(clock.start(start_high=False))

    a = random.randint(0,255)
    b = random.randint(0,255)
    c = adder(a,b)

    dut.a.value = a
    dut.b.value = b
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    assert dut.c.value == c, f"INCORRECT: dut: {dut.c.value}, sim: {c}"
