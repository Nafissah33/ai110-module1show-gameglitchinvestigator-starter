# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User opens Debug Info and sees the secret is 55
2. User enters a guess of 40 → "Too Low"
3. User enters a guess of 70 → "Too High"
4. Score updates correctly after each guess (-5 per miss)
5. User enters a guess of 55 → "Correct!" and the game ends
6. User clicks New Game → secret, attempts, and score reset and the game is playable again

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest -v
tests/test_edge_cases.py::test_negative_and_zero_are_rejected[-5] PASSED
tests/test_edge_cases.py::test_negative_and_zero_are_rejected[-1] PASSED
tests/test_edge_cases.py::test_negative_and_zero_are_rejected[0] PASSED
tests/test_edge_cases.py::test_negative_and_zero_are_rejected[-0] PASSED
tests/test_edge_cases.py::test_negative_and_zero_are_rejected[  -42  ] PASSED
tests/test_edge_cases.py::test_fractional_decimals_are_rejected[3.9] PASSED
tests/test_edge_cases.py::test_fractional_decimals_are_rejected[-3.9] PASSED
tests/test_edge_cases.py::test_fractional_decimals_are_rejected[0.5] PASSED
tests/test_edge_cases.py::test_fractional_decimals_are_rejected[50.0001] PASSED
tests/test_edge_cases.py::test_fractional_decimals_are_rejected[1.5e3] PASSED
tests/test_edge_cases.py::test_whole_decimal_is_accepted_as_integer PASSED
tests/test_edge_cases.py::test_huge_or_malformed_input_is_rejected_gracefully[99999999999999999999999] PASSED
tests/test_edge_cases.py::test_huge_or_malformed_input_is_rejected_gracefully[400-digit-int] PASSED
tests/test_edge_cases.py::test_huge_or_malformed_input_is_rejected_gracefully[1e400] PASSED
tests/test_edge_cases.py::test_huge_or_malformed_input_is_rejected_gracefully[inf] PASSED
tests/test_edge_cases.py::test_huge_or_malformed_input_is_rejected_gracefully[-inf] PASSED
tests/test_edge_cases.py::test_huge_or_malformed_input_is_rejected_gracefully[nan] PASSED
tests/test_edge_cases.py::test_huge_or_malformed_input_is_rejected_gracefully[abc] PASSED
tests/test_edge_cases.py::test_huge_or_malformed_input_is_rejected_gracefully[12abc] PASSED
tests/test_edge_cases.py::test_huge_or_malformed_input_is_rejected_gracefully[1,000] PASSED
tests/test_edge_cases.py::test_huge_or_malformed_input_is_rejected_gracefully[] PASSED
tests/test_edge_cases.py::test_huge_or_malformed_input_is_rejected_gracefully[   ] PASSED
tests/test_edge_cases.py::test_huge_or_malformed_input_is_rejected_gracefully[None] PASSED
tests/test_edge_cases.py::test_valid_inputs_still_accepted[1-1] PASSED
tests/test_edge_cases.py::test_valid_inputs_still_accepted[100-100] PASSED
tests/test_edge_cases.py::test_valid_inputs_still_accepted[ 50 -50] PASSED
tests/test_edge_cases.py::test_range_check_is_skipped_when_no_range_given PASSED
tests/test_edge_cases.py::test_boundary_guesses_score_and_compare_sanely PASSED
tests/test_game_logic.py::test_winning_guess PASSED
tests/test_game_logic.py::test_guess_too_high PASSED
tests/test_game_logic.py::test_guess_too_low PASSED
tests/test_game_logic.py::test_too_high_score_is_consistent_regardless_of_attempt_number PASSED
tests/test_game_logic.py::test_proximity_label_scales_with_range PASSED
tests/test_game_logic.py::test_hint_level_color_coding PASSED
tests/test_game_logic.py::test_summarize_session_rows PASSED
tests/test_game_logic.py::test_summarize_session_with_no_guesses PASSED
tests/test_high_score.py::test_missing_file_returns_empty PASSED
tests/test_high_score.py::test_first_score_is_a_record_and_is_saved PASSED
tests/test_high_score.py::test_lower_or_equal_score_does_not_replace_best PASSED
tests/test_high_score.py::test_higher_score_replaces_best_and_difficulties_are_separate PASSED
tests/test_high_score.py::test_corrupt_or_wrong_shape_file_is_ignored PASSED
tests/test_high_score.py::test_negative_best_can_be_beaten PASSED
tests/test_high_score.py::test_unwritable_path_does_not_crash PASSED
tests/test_high_score.py::test_closeness_percent PASSED
============================== 44 passed in 0.02s ==============================
```

### Challenge 1: Advanced Edge-Case Testing

New suite: [tests/test_edge_cases.py](tests/test_edge_cases.py). Three edge-case families that used to slip through `parse_guess`:

1. **Negative numbers / zero** (`-5`, `0`): were accepted as valid guesses and burned an attempt. Now rejected with a range message.
2. **Decimals** (`3.9`, `-3.9`): were silently truncated to `3` / `-3`. Now rejected; whole decimals like `42.0` still work.
3. **Extremely large / non-finite values** (`99999999999999999999999`, a 400-digit int, `1e400`, `inf`, `nan`): huge ints were accepted as guesses. Now rejected without crashing.

Fix: `parse_guess(raw, low, high)` in `logic_utils.py` now validates range and decimals, and `app.py` no longer charges an attempt for invalid input.

## 🚀 Stretch Features

**Challenge 4 – Enhanced UI**

All of this is presentation only: the core rules (`check_guess`, `update_score`, `parse_guess`) are unchanged, and the new helpers are pure functions in `logic_utils.py` with unit tests.

| Enhancement | Where | What it outputs now |
|---|---|---|
| **Color-coded hints** | `hint_level()` in `logic_utils.py`, used in the `if show_hint:` block of `app.py` | Maps a proximity label to a Streamlit message level, so the hint banner is 🟩 green when exact, 🟥 red when burning hot, 🟧 orange when warm and 🟦 blue when cool/cold |
| **Hot/Cold emojis** | `proximity_label()` in `logic_utils.py` | `🎯 Exact`, `🔥 Burning hot`, `♨️ Warm`, `🌤️ Cool`, `🧊 Cold`, scaled to the difficulty's range and appended to the Higher/Lower hint, e.g. `Too low — go HIGHER!  (🔥 Burning hot)` |
| **Session summary table** | `summarize_session()` in `logic_utils.py`, rendered by `render_history()` in `app.py` | When a game ends, a "Session summary" table lists outcome (🏆 Won / 💀 Lost), secret number, guesses used, closest guess and final score |
| **Per-guess table** | `guess_log` in `st.session_state`, rendered by `render_history()` | "Your guesses" table: attempt number, guess, result and proximity |
| **Live scoreboard** | The `st.metric` / `st.progress` block above the debug expander in `app.py` | Score, attempts used out of the limit, the difficulty's range, and an attempts progress bar |
| **Guess history sidebar** | `render_history()` + `closeness_percent()` | A closeness progress bar for each guess (see Challenge 2) |

Other fixes made along the way: the hint text was backwards (`"Too High"` said "Go HIGHER!"), and the prompt always said 1–100 regardless of difficulty. Tests: `test_hint_level_color_coding`, `test_summarize_session_rows`, `test_summarize_session_with_no_guesses`, `test_proximity_label_scales_with_range`.

**Challenge 2 – Feature Expansion**

- **🏆 High Score tracker:** the best winning score per difficulty is saved to `high_scores.json` and shown in the sidebar, with a banner when you beat it. A missing, corrupt or read-only file never crashes the game.
- **Guess History sidebar:** each guess is listed with its hot/cold label and a progress bar showing how close it was; it stays visible after the game ends and clears on New Game.
- Tests: `tests/test_high_score.py`. See the Agent Workflow section of `ai_interactions.md`.
