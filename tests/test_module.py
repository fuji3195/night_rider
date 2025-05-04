import os
import glob
import pytest
import cocotb_test.simulator as sim

COMMON_SETUP = {
    "verilog_sources":glob.glob(os.path.join(os.getcwd(), "src","*.v")),
    "toplevel":"top",
    "module":"tb.tb_night_rider",
    "simulator":"verilator",
    "compile_args":["+define+SIM"],
    "verilator_compile_args":["--trace","--trace-structs",
                                    #"--trace-fst", "--ldflags","-lverilated_fst"
                                ],
    "waves":True,
}
@pytest.mark.parametrize("N", [4, 8, 16])
def test_top(N,tmp_path):
    # verilog_src = [os.path.join("src", "top.v")]
    verilog_src = glob.glob(os.path.join(os.getcwd(), "src", "*.v"))
    module_name     = "top"
    pythonmodule    = "tb.tb_night_rider"
    sim_dir         = tmp_path / f"sim_{module_name}_{N}"
    sim.run(
        verilog_sources = verilog_src,
        toplevel        = module_name,
        module          = pythonmodule,
        simulator       = "verilator",
        compile_args    = ["+define+SIM"],
        verilator_compile_args  = [
                                    #"--trace", "--trace-structs",
                                    #"--trace-fst", "--ldflags","-lverilated_fst"
                                ],
        parameters      = {"N" : N},
        sim_build       = sim_dir,
        waves           = False,
        #extra_env       = {"FST_FILE": str(vcd_path)},
        #extra_env       = {"VCD_FILE": str(vcd_path)},
        extra_env        = {"COCOTB_LOG_LEVEL": "DEBUG",
                            #"MY_CUSTOM_VAR": "Hello from cocotb-test" # カスタム変数を追加
                            },
    )