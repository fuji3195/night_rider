import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
import os, sys

# --- クロック管理 ---
_clock_task = None # シミュレーション全体でクロックタスクを保持する変数

async def start_clock_once(dut):
    """ クロックがまだ開始されていなければ開始する """
    global _clock_task
    if _clock_task is None or _clock_task.done():
        dut._log.info("Starting the clock.")
        clk = Clock(dut.board_clk, 38, units="ns")
        _clock_task = cocotb.start_soon(clk.start())
        # クロックが安定するのを待つ (オプション)
        await RisingEdge(dut.board_clk)
        await RisingEdge(dut.board_clk)
    else:
        dut._log.info("Clock is already running.")

# --- DUTリセット関数 ---
async def reset_dut(dut):
    """ DUTをリセットし、初期状態を確認する """
    dut._log.info("Resetting DUT...")
    dut.rst_n_btn.value = 0
    await Timer(50, units="ns") # 例: クロック周期より少し長く
    dut.rst_n_btn.value = 1
    # リセット解除が伝播するのを待つ
    await RisingEdge(dut.board_clk)
    await RisingEdge(dut.board_clk)
    dut._log.info("DUT reset sequence complete.")
    # リセット後の期待される初期状態まで待機・確認
    # (重要: この待機が不足すると、テスト開始時にDUTが期待状態でない可能性がある)
    try:
        # 10Hzクロックが2回トグルするのを待つ
        await RisingEdge(dut.divide_to_10Hz.clk_out)
        await RisingEdge(dut.divide_to_10Hz.clk_out)
        assert dut.led.value == 0x01, "Initial LED value after reset is incorrect"
        dut._log.info("Initial LED value confirmed after reset.")
    except Exception as e:
        dut._log.error(f"Error during initial state check after reset: {e}")
        raise

@cocotb.test()
async def test1(dut):
    """
    reset後、動作が想定通り動くかの確認
    """
    dut._log.info(">>> Starting test1")
    await start_clock_once(dut) # クロックを開始 (または確認)
    await reset_dut(dut)        # 各テストの開始時にDUTをリセット

    # --- test1 のロジック ---
    N = len(dut.led)
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
        expected = 1<<n
        dut._log.info(f"cycle {i:3d}: curr {curr:02X}, expected {expected:02X}")
        assert curr == expected, f"cycle {i}: got {curr}, expected {expected}"
        i+=1
    dut._log.info(">>> Finished test1")
    pass

@cocotb.test()
async def test_reset_during_scan(dut):
    """
    少し進めた後にResetしたときに正しくResetされるかの確認。
    """
    dut._log.info(">>> Starting test_reset_during_scan")
    await start_clock_once(dut) # クロックを開始 (または確認)
    await reset_dut(dut)        # 各テストの開始時にDUTをリセット

    # --- test_reset_during_scan のロジック ---
    N = len(dut.led)

    dut._log.info("Running a few cycles before second reset...")
    for i in range(3):
        await RisingEdge(dut.divide_to_10Hz.clk_out)
        dut._log.info(f"Cycle {i}, LED: {dut.led.value.integer:02X}")

    # 再度リセット
    dut._log.info("Resetting DUT again during scan...")
    dut.rst_n_btn.value = 0
    # リセット中にクロックエッジが発生するように少し待つ
    await Timer(50, units="ns") # 例: クロック周期より少し長く
    dut.rst_n_btn.value = 1
    await RisingEdge(dut.board_clk) # リセット解除を同期
    await RisingEdge(dut.board_clk)
    dut._log.info("DUT reset complete again.")

    # リセット後の状態を確認
    try:
        # 10Hzクロックが2回トグルするのを待つ
        await RisingEdge(dut.divide_to_10Hz.clk_out)
        await RisingEdge(dut.divide_to_10Hz.clk_out)
        # リセット直後は 1 になるはず
        assert int(dut.led.value) == 1, f"Error led value after second reset is not correct"
        dut._log.info("Initial LED value confirmed after second reset.")
    except Exception as e:
        dut._log.error(f"Error during state check after second reset: {e}")
        raise

    dut._log.info(">>> Finished test_reset_during_scan")
    pass