import pytest

from wristheat import ectemp


def test_step_golden_165():
    ct, v = ectemp.step(37.1, 0.02, 165)
    assert ct == pytest.approx(37.290475, abs=0.0005)
    assert v == pytest.approx(0.018330, abs=0.00001)


def test_step_golden_80_zero_var():
    ct, v = ectemp.step(37.1, 0.0, 80)
    assert ct == pytest.approx(37.099811, abs=0.0005)
    assert v == pytest.approx(0.000483, abs=0.00001)


def test_run_sequence_A():
    out = ectemp.run([75] * 2 + [165] * 20 + [100] * 10)
    for minute, expected in [(2, 37.0656), (12, 38.0408), (22, 38.4650), (32, 38.1118)]:
        assert out[minute - 1][0] == pytest.approx(expected, abs=0.0005), minute


def test_run_published_params_crosses_38_at_34():
    out = ectemp.run([80] * 10 + [150] * 30 + [100] * 20, v=0.0)
    first = next(i + 1 for i, (ct, _) in enumerate(out) if ct >= 38.0)
    assert first == 34
    assert max(ct for ct, _ in out) == pytest.approx(38.1827, abs=0.0005)
