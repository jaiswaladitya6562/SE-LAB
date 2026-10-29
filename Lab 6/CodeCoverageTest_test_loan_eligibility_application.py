import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


# ---------- credit_band ----------
def test_excellent_band():
    assert credit_band(800) == "excellent"


def test_good_band():
    assert credit_band(700) == "good"


def test_fair_band():
    assert credit_band(600) == "fair"


def test_poor_band():
    assert credit_band(400) == "poor"


def test_invalid_score_raises():
    with pytest.raises(ValueError):
        credit_band(200)


# ---------- is_eligible ----------
def test_eligible():
    assert is_eligible(30, 50000, "salaried", 800) is True


def test_unknown_employment_raises():
    with pytest.raises(ValueError):
        is_eligible(30, 50000, "student", 800)


def test_too_young_not_eligible():
    assert is_eligible(18, 50000, "salaried", 800) is False


def test_low_income_not_eligible():
    assert is_eligible(30, 10000, "salaried", 800) is False


def test_poor_credit_not_eligible():
    assert is_eligible(30, 50000, "salaried", 400) is False


# ---------- interest_rate ----------
def test_rate_excellent():
    # 8 + 1 (self_employed) - 2 (collateral) = 7
    assert interest_rate(800, "self_employed", True) == 7


def test_rate_good():
    # 10 + 1 - 2 = 9
    assert interest_rate(700, "self_employed", True) == 9


def test_rate_fair():
    # 13 + 1 - 2 = 12
    assert interest_rate(600, "self_employed", True) == 12
