"""Advanced edge-case tests for guess parsing (Challenge 1)."""
import pytest

from logic_utils import parse_guess, check_guess, update_score

LOW, HIGH = 1, 100


# Edge case 1: negative numbers and zero (out of the playable range)
@pytest.mark.parametrize("raw", ["-5", "-1", "0", "-0", "  -42  "])
def test_negative_and_zero_are_rejected(raw):
    ok, value, err = parse_guess(raw, LOW, HIGH)
    assert ok is False and value is None
    assert "between 1 and 100" in err


# Edge case 2: decimals must not be silently truncated
@pytest.mark.parametrize("raw", ["3.9", "-3.9", "0.5", "50.0001", "1.5e3"])
def test_fractional_decimals_are_rejected(raw):
    ok, value, err = parse_guess(raw, LOW, HIGH)
    assert ok is False and value is None
    assert err


def test_whole_decimal_is_accepted_as_integer():
    assert parse_guess("42.0", LOW, HIGH) == (True, 42, None)


# Edge case 3: extremely large / non-finite / malformed values
@pytest.mark.parametrize(
    "raw",
    [
        "99999999999999999999999",
        pytest.param("1" + "0" * 400, id="400-digit-int"),
        "1e400", "inf", "-inf", "nan",
        "abc", "12abc", "1,000", "", "   ", None,
    ],
)
def test_huge_or_malformed_input_is_rejected_gracefully(raw):
    ok, value, err = parse_guess(raw, LOW, HIGH)  # must not raise
    assert ok is False and value is None
    assert isinstance(err, str) and err


# Sanity: valid boundary values still work, and range is optional
@pytest.mark.parametrize(
    "raw,expected", [("1", 1), ("100", 100), (" 50 ", 50)]
)
def test_valid_inputs_still_accepted(raw, expected):
    assert parse_guess(raw, LOW, HIGH) == (True, expected, None)


def test_range_check_is_skipped_when_no_range_given():
    assert parse_guess("-5") == (True, -5, None)


def test_boundary_guesses_score_and_compare_sanely():
    assert check_guess(1, 1) == "Win"
    assert update_score(0, "Win", 50) == 10  # score floor holds on late wins
