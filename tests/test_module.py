import os
import glob
import pytest
import cocotb_test.simulator as sim

@pytest.mark.parametrize("N", [4, 8, 16])
def test_top(N,tmp_path):
    print("test top start")
    # verilog_src = [os.path.join("src", "top.v")]
    verilog_src = glob.glob(os.path.join(os.getcwd(), "src", "*.v"))
    module_name     = "top"
    pythonmodule    = "tb.tb_night_rider"
    sim_dir         = tmp_path / f"sim_{module_name}_{N}"
    #wave_dir        = tmp_path.parent / "waveforms"
    #vcd_path        = wave_dir / f"{module_name}_{N}.vcd"
    #wave_dir.mkdir(exist_ok = True)
    sim.run(
        verilog_sources = verilog_src,
        toplevel        = module_name,
        module          = pythonmodule,
        simulator       = "verilator",
        compile_args    = ["+define+SIM"],
        verilator_compile_args  = ["--trace", "--trace-structs",
                                    #"--trace-fst", "--ldflags","-lverilated_fst"
                                ],
        parameters      = {"N" : N},
        sim_build       = sim_dir,
        waves           = True,
        #extra_env       = {"FST_FILE": str(vcd_path)},
        #extra_env       = {"VCD_FILE": str(vcd_path)},
        extra_env        = {"COCOTB_LOG_LEVEL": "INFO",
                            "MY_CUSTOM_VAR": "Hello from cocotb-test" # カスタム変数を追加
                            },
        #cocotb_args     = ["--log-level","INFO","--dump-level","DEBUG"],
        #extra_args      = ["--log-level", "DEBUG", "--traceback", "on"],
    )

    #assert vcd_path.exists()