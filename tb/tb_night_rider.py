import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

N = 8

@cocotb.test()
async def test1(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    dut.rst_n.value = 0
    await Timer(25, units="ns")
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    assert dut.led_out.value == 0x01, f"Error initial led out is not correct"
    
    n = 0
    dir = 1
    i = 0
    while i < 50:
        if dir == 1: n+=1
        else: n-=1
        if n == N-1: dir = 0
        if n == 0: dir = 1
        await RisingEdge(dut.clk)
        curr = int(dut.led_out.value)
        expected = 1<<n
        assert curr ==expected, f"cycle {i}: count was {curr}, expected {expected}"
        i+=1