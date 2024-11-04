import random

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sps

import cocotb
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock
import cocotb.binary
import cocotb.utils

def float_to_binary(x, m, n):
    x_scaled = round(x * 2 ** n)
    return '{:0{}b}'.format(x_scaled, m + n)

def binary_to_float(bstr, m, n):
    return int(bstr, 2) / 2 ** n

def twos_binary_to_float(bstr):
    blen = len(bstr)
    if bstr[0] == '1':
        si = int(bstr,2) - (1<<blen)
    else:
        si = int(bstr,2)
    return si

def float_to_twos_binary(fl):
    return 0

@cocotb.test()
async def lut_tb(dut):
    #simulation values
    r = 0.001

    #stimulus
    t = []
    for i in range(4096):
        t.append(i)
    #for i in range(y.size):
    #    y[i] = y[i] - random.uniform(0,0.1)

    #params

    #initialize clock : 0.05us=20MHz
    clock = Clock(dut.clk, 0.05, units="us")
    cocotb.start_soon(clock.start(start_high=False))

    #vhdl inputs

    #reset
    dut.reset.value = 1
    await Timer(1,units="us")
    dut.reset.value = 0
    dut.clk_en.value = 1
    await Timer(1,units="us")

    #data array
    y = []
    n = []

    sim_time = 0
    it = 0
    for i in range(len(t)):
        #keep track of simulation time
        #sim_time = cocotb.utils.get_sim_time('sec')
        #print(f"Sim Time: {sim_time:.10f}")
        #print("--------------------------")

        #allow simulation stuff to happen

        #apply input to dut and wait for clk
        print(t[i])
        dut.theta.value = t[i]
        dut.clk_en.value = 1
        await RisingEdge(dut.clk)

        #obtain dut output, convert to fixed point, add to dut array
        dout_value = dut.sin_data.value.signed_integer
        dout_value1 = dut.cos_data.value.signed_integer
        #dout_bin = float_to_binary(dout_value,16,0)
        #dout_fix = (binary_to_float(dout_bin,2,14))
        #dout_fix = (binary_to_float(dout_bin,2,14))
        y.append(dout_value)
        n.append(dout_value1)

        #print relevant values
        #print(f"DUT OUT: {dut.dout.value}, FIXED: {dout_value}")
        #print("\n")
        if i % 10 == 0:
            print(i)

    #Plotting results
    plt.plot(t,y)
    plt.plot(t,n)
    plt.show()
