import pytest

from file_storage.controller import Controller


@pytest.mark.parametrize(
    'a, b, res',
    [
        (0, 0, 0),
        (0, 1, 1),
        (1, 0, 1),
        (15, 82, 97),
        (-5, -2, -7),
        (-5, 2, -3),
    ],
)
def test_calc_sum_normal(controller: Controller, a: int, b: int, res: int):
    assert controller.calc_sum(a, b) == res
