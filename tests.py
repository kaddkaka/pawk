import pytest
import subprocess

tests = [
    (["pawk", "-t", "print(NR, F[0])", "examples/fruit_prices.txt"],
     """1 Banana 150
2 Apple 10
3 Citrus 200
4 Blueberries 30
5 Strawberries 30"""),
    (["pawk", "-f", "examples/total_sum.py", "examples/fruit_prices.txt"],
     "Total: 420"),
    (["pawk", "-f", "examples/total_order_cost.py",
      "examples/fruit_prices.txt", "examples/fruit_orders.txt"],
     "Total: {'David': 300, 'Monica': 600}"),
]

@pytest.mark.parametrize("cmd, expected_output", tests)
def tests(cmd, expected_output):
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    assert result.stderr == ""
    assert result.stdout.strip() == expected_output