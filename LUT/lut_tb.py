import random

import matplotlib.pyplot as plt

import cocotb
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock

from python.functions.conversion import binary_to_float
from python.functions.conversion import float_to_binary

@cocotb.test()
async def lut_tb(dut):
    #simulation values
    r = 0.001

    #stimulus
    t = []
    for i in range(4096):
        t.append(i)

    #initialize clock : 0.05us=20MHz
    clock = Clock(dut.clk, 0.05, units="us")
    cocotb.start_soon(clock.start(start_high=False))

    #reset
    dut.reset.value = 1
    await Timer(1,units="us")
    dut.reset.value = 0
    dut.clk_en.value = 1
    await Timer(1,units="us")

    #data array
    y = []
    n = []

    it = 0
    for i in range(len(t)):
        dut.theta.value = t[i]
        dut.clk_en.value = 1
        await RisingEdge(dut.clk)

        dout_value = dut.sin_data.value.signed_integer
        dout_value1 = dut.cos_data.value.signed_integer
        y.append(dout_value)
        n.append(dout_value1)

    #Plotting results
    plt.plot(t,y)
    plt.plot(t,n)
    plt.show()
