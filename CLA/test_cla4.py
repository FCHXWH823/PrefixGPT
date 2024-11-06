import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_cla4(dut):
    """Test the 4-bit CLA"""

    # Set a number of random test cases
    max_val = 0xF  # 4-bit maximum value

    for a in range(1<<4):
        for b in range(1<<4):
            
            # Assign inputs
            dut.a.value = a
            dut.b.value = b

            # Wait for a simulated clock cycle or a wait cycle if asynchronous

            # await RisingEdge(dut.clk)  # Replace with an async wait if no clock
            await Timer(10, units="ns")
            # Calculate expected results
            expected_sum = (a + b) & max_val  # 4-bit sum
            expected_cout = (a + b) >> 4      # Carry out

            # Check if the results match the expected values
            assert dut.sum.value == expected_sum, f"Test failed with a={a}, b={b}: sum={dut.sum.value}, expected={expected_sum}"
            assert dut.cout.value == expected_cout, f"Test failed with a={a}, b={b}: cout={dut.cout.value}, expected={expected_cout}"

            # Print the test result (optional)
            print(f"PASS: a={a}, b={b} -> sum={dut.sum.value}, cout={dut.cout.value}")
