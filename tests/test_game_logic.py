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
    even_attempt_score = update_score(current_score=100, outcome="Too High", attempt_number=2)
    odd_attempt_score = update_score(current_score=100, outcome="Too High", attempt_number=3)

    assert even_attempt_score == 95
    assert odd_attempt_score == 95
