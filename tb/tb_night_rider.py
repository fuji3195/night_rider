import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

N = 8

@cocotb.test()
async def test1(dut):
    cocotb.start_soon(Clock(dut.board_clk, 38, units="ns").start())

    dut.rst_n_btn.value = 0
    await Timer(25, units="ns")
    dut.rst_n_btn.value = 1
    await RisingEdge(dut.board_clk) # system clockでReset解除を同期
    await RisingEdge(dut.board_clk)
    await RisingEdge(dut.divide_to_10Hz.clk_out)    # reset flipflop bypass 1段目
    await RisingEdge(dut.divide_to_10Hz.clk_out)    # reset flipflop bypass 2段目
    assert dut.led.value == 0x01, f"Error initial led out is not correct"
    
    n = 0
    dir = 1
    i = 0
    while i < 100:
        await RisingEdge(dut.divide_to_10Hz.clk_out)
        if dir == 1:
            n+=1
            if n == N-1: dir = 0
        else:
            n-=1
            if n == 0: dir = 1
        curr = int(dut.led.value)
        #print(f"n = {n}, curr = {curr}")
        expected = 1<<n
        dut._log.info(f"cycle {i:3d}: curr {curr:02X}, expected {expected:02X}")
        assert curr == expected, f"cycle {i}: got {curr}, expected {expected}"
        i+=1