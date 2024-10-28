import random

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sps
import scipy as sp

import cocotb
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock
import cocotb.binary
import cocotb.utils

from python.conversion import float_to_binary
from python.conversion import binary_to_float

@cocotb.test()
async def combfilter_tb(dut):
    #simulation values
    Fs = 20 * 10**6
    Ts = 1/Fs
    freqs = [76923.08,77972.71,78125,78201.01]
    freq = 78125
    r = 0.001
    Fsr = int(Fs*r)

    #stimulus
    t = np.linspace(0,r,Fsr)
    #y = np.sin(freq*2*np.pi*t)
    y = sps.chirp(t,0,r,5000000)

    #params
    gain = 4
    delay = 257
    y_delay = np.zeros(y.size)
    y_fixed = np.zeros(y.size)

    #initialize clock
    clock = Clock(dut.clk, 0.05, units="us")
    cocotb.start_soon(clock.start(start_high=False))

    #vhdl inputs
    dut.din.value = 0
    dut.G.value = gain
    dut.Dfrac.value = int(0 * 65536)
    dut.rst.value = 1
    await Timer(1,units="us")
    dut.rst.value = 0
    await Timer(1,units="us")
    dut.vdel.value = 0

    #digital filter
    num = np.zeros(delay)
    den = np.zeros(delay)

    num[0] = 2**(-1*gain)
    den[0] = 1
    den[delay-1] = -(1-(2**(-1*gain)))

    #Applying filter
    z = sps.lfilter(num,den,y)

    sim_time = 0
    it = 0
    while sim_time < r-0.00001:
        #keep track of simulation time
        sim_time = cocotb.utils.get_sim_time('sec')
        print(f"Sim Time: {sim_time:.10f}")
        print("--------------------------")

        #allow simulation stuff to happen

        #apply input to dut and wait for clk
        input_fixed = int(binary_to_float(float_to_binary(y[it],2,14),16,0))
        dut.din.value = input_fixed
        await RisingEdge(dut.clk)

        #obtain dut output, convert to fixed point, add to dut array
        dout_value = dut.dout.value.signed_integer
        dout_bin = float_to_binary(dout_value,16,0)
        dout_fix = (binary_to_float(dout_bin,2,14))
        #dout_fix = (binary_to_float(dout_bin,2,14))
        y_fixed[it] = dout_fix

        #print relevant values
        print(f"DUT OUT: {dut.dout.value}, FIXED: {dout_fix}")
        print(f"SIM OUT: {z[it]}")
        print("\n")

        it += 1

    #Plotting results
    #plt.plot(t[0:it],y[0:it])
    #plt.plot(t[0:it],z[0:it])
    #plt.plot(t[0:it],y_fixed[0:it])
    N = len(y[0:it])
    yf = sp.fft.fft(y_fixed[0:it])
    xf = sp.fft.fftfreq(N,1/Fs)
    plt.plot(xf[:N//2],np.abs(yf)[:N//2])
    plt.show()
