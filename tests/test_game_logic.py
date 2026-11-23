from logic_utils import check_guess, update_score


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_too_high_score_is_consistent_regardless_of_attempt_number():
    # Bug: "Too High" used to award +5 on even attempts but -5 on odd
    # attempts for the same mistake. It should always deduct 5 points.
    even_attempt_score = update_score(
        current_score=100, outcome="Too High", attempt_number=2
    )
    odd_attempt_score = update_score(
        current_score=100, outcome="Too High", attempt_number=3
    )

    assert even_attempt_score == 95
    assert odd_attempt_score == 95


def test_proximity_label_scales_with_range():
    from logic_utils import proximity_label
    assert proximity_label(50, 50, 1, 100) == "🎯 Exact"
    assert proximity_label(52, 50, 1, 100) == "🔥 Burning hot"
    assert proximity_label(60, 50, 1, 100) == "♨️ Warm"
    assert proximity_label(75, 50, 1, 100) == "🌤️ Cool"
    assert proximity_label(1, 100, 1, 100) == "🧊 Cold"
    # same absolute distance is "colder" on a smaller range
    assert proximity_label(10, 15, 1, 20) == "🌤️ Cool"


def test_hint_level_color_coding():
    from logic_utils import hint_level
    assert hint_level("🎯 Exact") == "success"
    assert hint_level("🔥 Burning hot") == "error"
    assert hint_level("♨️ Warm") == "warning"
    assert hint_level("🌤️ Cool") == "info"
    assert hint_level("🧊 Cold") == "info"
    assert hint_level("something else") == "info"


def test_summarize_session_rows():
    from logic_utils import summarize_session
    log = [{"Guess": 10}, {"Guess": 45}, {"Guess": 90}]
    rows = {r["Stat"]: r["Value"] for r in
            summarize_session(log, 50, "lost", -15)}
    assert rows["Outcome"] == "💀 Lost"
    assert rows["Guesses used"] == "3"
    assert rows["Closest guess"] == "45"
    assert rows["Final score"] == "-15"


def test_summarize_session_with_no_guesses():
    from logic_utils import summarize_session
    rows = {r["Stat"]: r["Value"] for r in
            summarize_session([], 50, "playing", 0)}
    assert rows["Closest guess"] == "—"
    assert rows["Outcome"] == "In progress"
