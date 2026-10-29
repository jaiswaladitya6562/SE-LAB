import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


# ---------- credit_band: validation branches ----------
@pytest.mark.parametrize("score", [299, 200, 901, 950])
def test_credit_band_invalid_score(score):
    with pytest.raises(ValueError):
        credit_band(score)


@pytest.mark.parametrize("score", [300, 900])
def test_credit_band_valid_limits_do_not_raise(score):
    # Score exactly at the limits is valid (False side of both conditions)
    credit_band(score)


# ---------- credit_band: every band, including boundaries ----------
@pytest.mark.parametrize(
    "score, expected",
    [
        (900, "excellent"),
        (750, "excellent"),
        (749, "good"),
        (650, "good"),
        (649, "fair"),
        (550, "fair"),
        (549, "poor"),
        (300, "poor"),
    ],
)
def test_credit_band_boundaries(score, expected):
    assert credit_band(score) == expected


# ---------- is_eligible: each decision, both outcomes ----------
def test_unknown_employment_raises():
    with pytest.raises(ValueError):
        is_eligible(30, 50000, "student", 800)


def test_age_below_minimum():
    assert is_eligible(20, 50000, "salaried", 800) is False


def test_age_above_maximum():
    assert is_eligible(61, 50000, "salaried", 800) is False


@pytest.mark.parametrize("age", [21, 60])
def test_age_on_limits_is_eligible(age):
    assert is_eligible(age, 50000, "salaried", 800) is True


def test_salaried_income_too_low():
    assert is_eligible(30, 24999, "salaried", 800) is False


def test_salaried_income_exact_minimum():
    assert is_eligible(30, 25000, "salaried", 800) is True


def test_self_employed_income_too_low():
    assert is_eligible(30, 39999, "self_employed", 800) is False


def test_self_employed_income_exact_minimum():
    assert is_eligible(30, 40000, "self_employed", 800) is True


def test_salaried_income_not_enough_for_self_employed():
    # 30000 passes for salaried but fails for self_employed
    assert is_eligible(30, 30000, "salaried", 800) is True
    assert is_eligible(30, 30000, "self_employed", 800) is False


def test_poor_credit_rejected():
    assert is_eligible(30, 50000, "salaried", 400) is False


def test_fair_credit_accepted():
    assert is_eligible(30, 50000, "salaried", 600) is True


def test_invalid_score_propagates_from_is_eligible():
    with pytest.raises(ValueError):
        is_eligible(30, 50000, "salaried", 1000)


# ---------- interest_rate: band x employment x collateral ----------
@pytest.mark.parametrize(
    "score, employment, collateral, expected",
    [
        # excellent (base 8)
        (800, "salaried", False, 8),
        (800, "salaried", True, 6),
        (800, "self_employed", False, 9),
        (800, "self_employed", True, 7),
        # good (base 10)
        (700, "salaried", False, 10),
        (700, "salaried", True, 8),
        (700, "self_employed", False, 11),
        (700, "self_employed", True, 9),
        # fair (base 13)
        (600, "salaried", False, 13),
        (600, "salaried", True, 11),
        (600, "self_employed", False, 14),
        (600, "self_employed", True, 12),
        # poor falls into the else branch (base 13)
        (400, "salaried", False, 13),
        (400, "self_employed", True, 12),
    ],
)
def test_interest_rate_all_paths(score, employment, collateral, expected):
    assert interest_rate(score, employment, collateral) == expected


def test_interest_rate_invalid_score_raises():
    with pytest.raises(ValueError):
        interest_rate(100, "salaried", False)
