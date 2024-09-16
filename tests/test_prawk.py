import subprocess
import pytest
from prawk import do_the_stuff


shell_test_params = [
    (["prawk -t 'print(F[1])' <(echo a b c)"], "a"),
    (["prawk -t 'print(F[-1])' <(echo a b c)"], "c"),
    (["echo x y z | prawk -t 'print(F[-2])' -"], "y"),
]
@pytest.mark.parametrize(["cmd", "expected_output"], shell_test_params)
def test_shell_tests(cmd, expected_output):
    result = subprocess.run(cmd, check=True, capture_output=True, text=True,
                            shell=True, executable="/bin/bash")
    assert result.stdout[:-1] == expected_output


tests = [
    (["prawk", "-t", "print(NR, F[0])", "examples/fruit_prices.txt"],
     """1 Banana 150
2 Apple 10
3 Citrus 200
4 Blueberries 30
5 Strawberries 30"""),
    (["prawk", "-f", "examples/total_sum.py", "examples/fruit_prices.txt"],
     "Total: 420"),
    (["prawk", "-f", "examples/total_order_cost.py",
      "examples/fruit_prices.txt", "examples/fruit_orders.txt"],
     "Total: {'David': 300, 'Monica': 600}"),
]
@pytest.mark.parametrize("cmd, expected_output", tests)
def test_prawk(cmd, expected_output):
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    assert result.stderr == ""
    assert result.stdout.strip() == expected_output


def test_unit_test() -> None:
    res = do_the_stuff("if NR == 1: NEXT\nS+=F[1]", [["2", "3", "4"]], {"S": 0})
    assert res["S"] == 7
