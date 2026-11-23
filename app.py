"""Streamlit UI for the Glitchy Guesser number-guessing game."""

import random
import streamlit as st

# FIX: Refactored game logic into logic_utils.py with AI help, so it could
# be unit tested; app.py now imports the pure functions instead of defining
# them inline.
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    proximity_label,
    closeness_percent,
    hint_level,
    summarize_session,
    load_high_scores,
    record_high_score,
)

# FIX: AI suggested check_guess return only the outcome string (to match
# tests/test_game_logic.py), so this dict rebuilds the hint text for the UI
# instead of getting it back from check_guess directly.
HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Too high — go LOWER!",
    "Too Low": "📈 Too low — go HIGHER!",
}

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Challenge 2: high score tracker (persisted in high_scores.json).
best_scores = load_high_scores()
st.sidebar.metric(
    f"🏆 High score ({difficulty})",
    best_scores.get(difficulty, "—"),
)

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIX: AI traced the "Attempts left" off-by-one to this starting at 1
# instead of 0, which also ended games one guess early.
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "guess_log" not in st.session_state:
    st.session_state.guess_log = []

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

# Enhanced UI: live scoreboard + attempts progress bar.
m1, m2, m3 = st.columns(3)
m1.metric("Score", st.session_state.score)
m2.metric("Attempts used", f"{st.session_state.attempts}/{attempt_limit}")
m3.metric("Range", f"{low}–{high}")
st.progress(min(st.session_state.attempts / attempt_limit, 1.0))

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

history_sidebar = st.sidebar.container()
history_main = st.container()


def render_history():
    """Fill the guess-history sidebar and table (also after game over)."""
    with history_sidebar:
        st.divider()
        st.subheader("Guess history")
        if st.session_state.guess_log:
            for entry in st.session_state.guess_log:
                pct = closeness_percent(
                    entry["Guess"], st.session_state.secret, low, high
                )
                st.caption(
                    f"#{entry['Attempt']}: {entry['Guess']} — "
                    f"{entry['Proximity']}"
                )
                st.progress(pct / 100)
        else:
            st.caption("No guesses yet.")
    with history_main:
        if st.session_state.status != "playing":
            st.subheader("Session summary")
            st.table(
                summarize_session(
                    st.session_state.guess_log,
                    st.session_state.secret,
                    st.session_state.status,
                    st.session_state.score,
                )
            )
        if st.session_state.guess_log:
            st.subheader("Your guesses")
            st.table(st.session_state.guess_log)


raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: AI found that New Game never reset status, so after a win/loss the
# "Game over" screen below would trigger st.stop() forever. Now resets
# status/score/history too, and uses low/high so the secret respects the
# selected difficulty instead of always being 1-100.
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.guess_log = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    render_history()
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        # Invalid input (negative, decimal, out of range...) is rejected
        # without costing the player an attempt.
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX: AI removed code here that converted secret to a string on
        # every other attempt, which made check_guess compare int vs str
        # and produce backwards "Too High"/"Too Low" hints.
        outcome = check_guess(guess_int, st.session_state.secret)

        heat = proximity_label(guess_int, st.session_state.secret, low, high)
        st.session_state.guess_log.append(
            {"Attempt": st.session_state.attempts, "Guess": guess_int,
             "Result": outcome, "Proximity": heat}
        )

        if show_hint:
            # Color-coded by proximity: green exact, red hot, orange warm,
            # blue cool/cold (see logic_utils.hint_level).
            getattr(st, hint_level(heat))(
                f"{HINT_MESSAGES[outcome]}  ({heat})"
            )

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            is_record, best = record_high_score(
                difficulty, st.session_state.score
            )
            if is_record:
                st.success(f"🏆 New high score for {difficulty}: {best}!")
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

render_history()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
