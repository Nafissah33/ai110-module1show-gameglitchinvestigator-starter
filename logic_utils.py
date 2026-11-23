"""Pure game logic for the Glitchy Guesser number-guessing game.

Everything in this module is free of Streamlit and global state so it can be
unit tested directly. ``app.py`` handles the UI and calls these functions.
"""

import json

HIGH_SCORE_FILE = "high_scores.json"


def get_range_for_difficulty(difficulty: str):
    """Return the inclusive guessing range for a difficulty level.

    Args:
        difficulty: One of ``"Easy"``, ``"Normal"`` or ``"Hard"``. Any other
            value falls back to the Normal range.

    Returns:
        tuple[int, int]: ``(low, high)``, both inclusive.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 50)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low: int = None, high: int = None):
    """Validate raw text input and convert it to an integer guess.

    Surrounding whitespace is ignored. Whole decimals such as ``"5.0"`` are
    accepted, but fractional decimals are rejected rather than silently
    truncated. ``inf``, ``nan`` and numbers too large for a float are
    rejected without raising.

    Args:
        raw: The text typed by the player. May be ``None`` or empty.
        low: Optional inclusive lower bound of the playable range.
        high: Optional inclusive upper bound of the playable range. The
            range check only runs when both bounds are given.

    Returns:
        tuple[bool, int | None, str | None]: ``(ok, guess, error)``. On
        success ``guess`` is the integer and ``error`` is ``None``; on
        failure ``guess`` is ``None`` and ``error`` explains why.

    Examples:
        >>> parse_guess(" 42 ")
        (True, 42, None)
        >>> parse_guess("3.9")
        (False, None, 'Enter a whole number, not a decimal.')
        >>> parse_guess("500", 1, 100)
        (False, None, 'Enter a number between 1 and 100.')
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    raw = raw.strip()

    try:
        if "." in raw:
            number = float(raw)
            if not number.is_integer():  # also False for inf and nan
                return False, None, "Enter a whole number, not a decimal."
            value = int(number)
        else:
            value = int(raw)
    except (ValueError, OverflowError):
        return False, None, "That is not a number."

    if low is not None and high is not None and not low <= value <= high:
        return False, None, f"Enter a number between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int):
    """Compare a guess with the secret number.

    Args:
        guess: The player's guess.
        secret: The number the player is trying to find.

    Returns:
        str: ``"Win"`` if they match, ``"Too High"`` if the guess is above
        the secret, otherwise ``"Too Low"``.

    Examples:
        >>> check_guess(60, 50)
        'Too High'
        >>> check_guess(40, 50)
        'Too Low'
        >>> check_guess(50, 50)
        'Win'
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Return the new score after a guess.

    A win earns ``100 - 10 * (attempt_number + 1)`` points, never fewer than
    10. Every wrong guess, high or low, costs 5 points. Unknown outcomes
    leave the score unchanged.

    Args:
        current_score: The score before this guess.
        outcome: The result from :func:`check_guess`.
        attempt_number: How many guesses the player has made, including
            this one.

    Returns:
        int: The updated score.

    Examples:
        >>> update_score(0, "Win", 1)
        80
        >>> update_score(100, "Too High", 3)
        95
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score


def proximity_label(guess: int, secret: int, low: int, high: int):
    """Describe how close a guess is as a hot/cold label.

    Distance is measured as a fraction of the whole range, so the same
    thresholds work for every difficulty.

    Args:
        guess: The player's guess.
        secret: The secret number.
        low: Inclusive lower bound of the range.
        high: Inclusive upper bound of the range.

    Returns:
        str: One of ``"🎯 Exact"``, ``"🔥 Burning hot"`` (within 5% of the
        range), ``"♨️ Warm"`` (15%), ``"🌤️ Cool"`` (35%) or ``"🧊 Cold"``.

    Examples:
        >>> proximity_label(50, 50, 1, 100)
        '🎯 Exact'
        >>> proximity_label(1, 100, 1, 100)
        '🧊 Cold'
    """
    span = max(high - low, 1)
    ratio = abs(guess - secret) / span
    if ratio == 0:
        return "🎯 Exact"
    if ratio <= 0.05:
        return "🔥 Burning hot"
    if ratio <= 0.15:
        return "♨️ Warm"
    if ratio <= 0.35:
        return "🌤️ Cool"
    return "🧊 Cold"


def load_high_scores(path: str = HIGH_SCORE_FILE):
    """Load the saved best scores from a JSON file.

    Args:
        path: Location of the high score file.

    Returns:
        dict[str, int]: Best score per difficulty. A missing, unreadable or
        malformed file yields ``{}``; entries that are not integer scores
        are dropped.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {
        key: value
        for key, value in data.items()
        if isinstance(key, str)
        and isinstance(value, int)
        and not isinstance(value, bool)
    }


def record_high_score(
    difficulty: str, score: int, path: str = HIGH_SCORE_FILE
):
    """Save ``score`` if it beats the stored best for ``difficulty``.

    Failure to write the file (for example a read-only disk) is ignored so
    it can never crash the game.

    Args:
        difficulty: The difficulty the score was earned on.
        score: The finished game's score.
        path: Location of the high score file.

    Returns:
        tuple[bool, int]: ``(is_new_record, best_score)``. A score equal to
        the existing best is not a new record.
    """
    scores = load_high_scores(path)
    best = scores.get(difficulty)
    if best is not None and score <= best:
        return False, best
    scores[difficulty] = score
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(scores, file, indent=2)
    except OSError:
        pass
    return True, score


def closeness_percent(guess: int, secret: int, low: int, high: int):
    """Return how close a guess is to the secret as a 0-100 percentage.

    Args:
        guess: The player's guess.
        secret: The secret number.
        low: Inclusive lower bound of the range.
        high: Inclusive upper bound of the range.

    Returns:
        int: ``100`` for an exact match, falling linearly to ``0`` at the
        far end of the range. Never below 0.

    Examples:
        >>> closeness_percent(50, 50, 1, 100)
        100
        >>> closeness_percent(1, 100, 1, 100)
        0
    """
    span = max(high - low, 1)
    return max(0, round(100 * (1 - abs(guess - secret) / span)))


def hint_level(heat: str):
    """Map a proximity label to a Streamlit message level for color coding.

    Args:
        heat: A label returned by :func:`proximity_label`.

    Returns:
        str: ``"success"`` (green) for an exact match, ``"error"`` (red)
        for hot guesses, ``"warning"`` (orange) for warm ones and ``"info"``
        (blue) for cool and cold ones. Unknown labels map to ``"info"``.

    Examples:
        >>> hint_level("🎯 Exact")
        'success'
        >>> hint_level("🧊 Cold")
        'info'
    """
    levels = {
        "🎯 Exact": "success",
        "🔥 Burning hot": "error",
        "♨️ Warm": "warning",
    }
    return levels.get(heat, "info")


def summarize_session(guess_log: list, secret: int, status: str, score: int):
    """Build the end-of-game summary shown as a table.

    Args:
        guess_log: One dict per valid guess with ``"Guess"`` keys, as built
            by ``app.py``.
        secret: The secret number.
        status: ``"won"``, ``"lost"`` or ``"playing"``.
        score: The final score.

    Returns:
        list[dict[str, str]]: ``{"Stat": ..., "Value": ...}`` rows covering
        outcome, secret, guesses used, closest guess and final score. The
        closest guess is ``"—"`` when no guesses were made.

    Examples:
        >>> rows = summarize_session([{"Guess": 40}, {"Guess": 55}], 50,
        ...                          "lost", -10)
        >>> rows[3]
        {'Stat': 'Closest guess', 'Value': '55'}
    """
    outcome = {"won": "🏆 Won", "lost": "💀 Lost"}.get(status, "In progress")
    guesses = [entry["Guess"] for entry in guess_log]
    closest = min(guesses, key=lambda g: abs(g - secret)) if guesses else "—"
    return [
        {"Stat": "Outcome", "Value": outcome},
        {"Stat": "Secret number", "Value": str(secret)},
        {"Stat": "Guesses used", "Value": str(len(guesses))},
        {"Stat": "Closest guess", "Value": str(closest)},
        {"Stat": "Final score", "Value": str(score)},
    ]
