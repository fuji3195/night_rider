import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def test1(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    dut.rst_n.value = 0
    await Timer(25, units="ns")
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    
    prev = int(dut.count.value)
    for i in range(100):
        await RisingEdge(dut.clk)
        curr = int(dut.count.value)
        expected = (prev+1)&0xFF
        assert curr ==expected, f"cycle {i}: count was {curr}, expected {expected}"
        prev = curr