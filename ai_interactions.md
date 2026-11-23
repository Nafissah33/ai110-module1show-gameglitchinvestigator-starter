# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

"Use your AI coding assistant agentically to plan and implement a meaningful new feature" (Challenge 2). I asked for a persistent **High Score tracker** (best score saved to a file) and a **Guess History sidebar** that visualizes how close each previous guess was.

**What did the agent do?**

Files modified or added:

- `logic_utils.py`: added `load_high_scores`, `record_high_score` (JSON file, best score per difficulty, tolerant of missing/corrupt/unwritable files) and `closeness_percent`.
- `app.py`: sidebar "🏆 High score" metric for the current difficulty; saves a new record on a win; "Guess history" sidebar with a closeness progress bar per guess.
- `tests/test_high_score.py` (new): 8 tests using `tmp_path`, so they never touch the real score file.
- `.gitignore`: ignores the generated `high_scores.json`.
- `README.md`: documents the feature.

Steps: read `app.py`/`logic_utils.py`, planned the feature, put the logic in `logic_utils.py` (testable) with the UI in `app.py`, wrote tests (41 pass), then drove the real app with Streamlit's `AppTest` (miss, then win, then rerun) to confirm the high score file is written and the sidebar renders without exceptions.

**What did you have to verify or fix manually?**

- My first version rendered the history at the bottom of `app.py`. After a win or loss, `st.stop()` runs first on the next rerun, so the history disappeared. I moved the rendering into `render_history()` using sidebar/main containers and call it before `st.stop()` as well.
- Known limitation: the sidebar high-score metric is drawn before the guess is processed, so on the exact run where you set a new record it still shows the old best (the success banner shows the new one, and the next rerun shows the updated metric).
- I did not open the app in a real browser; verification was through `AppTest` and unit tests only.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative numbers / zero (`-5`, `0`) | "Identify three edge-case inputs that might still break my guessing game's `parse_guess` and generate pytest cases that verify they are handled gracefully (negative numbers, decimals, extremely large values)." | `test_negative_and_zero_are_rejected` (parametrized) | Old code accepted `-5` and `0` (checked by hand-running the old `parse_guess`); passes after adding range validation | Players can type anything; an out-of-range number is never a legitimate guess and shouldn't cost an attempt. |
| Decimals (`3.9`, `-3.9`, `1.5e3`) | Same prompt as above | `test_fractional_decimals_are_rejected`, `test_whole_decimal_is_accepted_as_integer` | Old code turned `3.9` into `3` (checked by hand); passes after rejecting fractional values | Silent truncation makes the game judge a different number than the player typed. |
| Extremely large / non-finite (`99999999999999999999999`, `1e400`, `inf`, `nan`) | Same prompt as above | `test_huge_or_malformed_input_is_rejected_gracefully` | Old code accepted huge ints (checked by hand) but already rejected inf/nan/overflow; all pass now | Huge and non-finite values are classic crash/overflow inputs; the game must never raise an exception. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
1. "Add professional-grade docstrings to every function in logic_utils.py."
2. "Review my code for PEP 8 style compliance and apply your suggestions to
   resolve any formatting or naming issues you identify."
```

(Paraphrased from the Challenge 3 instructions; replace with your exact wording if it differed.)

Tooling: `flake8` with the `pep8-naming` and `flake8-docstrings` plugins
(run from a throwaway virtualenv, not added to `requirements.txt`),
`flake8 --max-line-length=79 logic_utils.py app.py tests`.

**Linting output before:**

```
app.py:1:1: D100 Missing docstring in public module
app.py:115:80: E501 line too long (83 > 79 characters)
logic_utils.py:1:1: D100 Missing docstring in public module
logic_utils.py:111:80: E501 line too long (85 > 79 characters)
logic_utils.py:114:80: E501 line too long (80 > 79 characters)
tests/test_edge_cases.py:11:1: D103 Missing docstring in public function
tests/test_edge_cases.py:19:1: D103 Missing docstring in public function
tests/test_edge_cases.py:25:1: D103 Missing docstring in public function
tests/test_edge_cases.py:32:80: E501 line too long (113 > 79 characters)
tests/test_edge_cases.py:35:1: D103 Missing docstring in public function
tests/test_edge_cases.py:42:80: E501 line too long (80 > 79 characters)
tests/test_edge_cases.py:43:1: D103 Missing docstring in public function
tests/test_edge_cases.py:47:1: D103 Missing docstring in public function
tests/test_edge_cases.py:51:1: D103 Missing docstring in public function
tests/test_game_logic.py:1:1: D100 Missing docstring in public module
tests/test_game_logic.py:3:1: D103 Missing docstring in public function
tests/test_game_logic.py:3:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:8:1: D103 Missing docstring in public function
tests/test_game_logic.py:8:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:13:1: D103 Missing docstring in public function
tests/test_game_logic.py:13:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:18:1: D103 Missing docstring in public function
tests/test_game_logic.py:18:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:21:80: E501 line too long (94 > 79 characters)
tests/test_game_logic.py:22:80: E501 line too long (93 > 79 characters)
tests/test_game_logic.py:28:1: D103 Missing docstring in public function
tests/test_high_score.py:1:1: D100 Missing docstring in public module
tests/test_high_score.py:6:1: D103 Missing docstring in public function
tests/test_high_score.py:10:1: D103 Missing docstring in public function
tests/test_high_score.py:16:1: D103 Missing docstring in public function
tests/test_high_score.py:24:1: D103 Missing docstring in public function
tests/test_high_score.py:32:1: D103 Missing docstring in public function
tests/test_high_score.py:42:1: D103 Missing docstring in public function
tests/test_high_score.py:48:1: D103 Missing docstring in public function
tests/test_high_score.py:49:80: E501 line too long (89 > 79 characters)
tests/test_high_score.py:52:1: D103 Missing docstring in public function
```

**Linting output after** (`flake8 .` with the new `setup.cfg`):

```
$ flake8 .
$ echo $?
0
```

Also: `python -m doctest logic_utils.py` passes (the new docstring examples
are real, executable doctests) and `pytest` still shows 41 passed.

**Changes applied:**

Docstrings (`logic_utils.py`): every function now has a Google-style
docstring with a summary, `Args`, `Returns` and, where useful, runnable
`Examples`; the module has a docstring too. The previous one-liners did not
document the edge-case behaviour added in Challenges 1 and 2.

| AI suggestion | Applied? |
|---|---|
| D100: add module docstrings to `app.py` and `logic_utils.py` | Yes |
| E501: wrap lines over 79 characters (`logic_utils.py`, `app.py`, tests) | Yes, all of them |
| E302: two blank lines between functions in `tests/test_game_logic.py` | Yes |
| PEP 8 imports: move `import json` from inside two functions to the top of `logic_utils.py` | Yes |
| Add type hints to `check_guess` parameters | Yes (`guess: int, secret: int`) |
| D100/D103: add docstrings to every test function and test module | No. I set `per-file-ignores = tests/*:D100,D103` in `setup.cfg` instead; the descriptive test names already say what each does and 30+ one-line docstrings would be noise |
| Naming (`pep8-naming`) | Nothing flagged: function and variable names were already `snake_case`. I only renamed the local `f` file handle to `file` while rewriting |

Not changed: `.venv` is excluded from linting, and I did not add flake8 to
`requirements.txt`.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

The Phase 1 bug where hints were wrong on alternating guesses. In the original `app.py`, the submit handler did `secret = str(st.session_state.secret)` whenever `attempts % 2 == 0`, so `check_guess` compared an `int` with a `str`, hit a `TypeError`, and a `try/except` fallback silently compared the two as strings. Both models got the identical prompt, with the original `check_guess` and the submit-handler snippet pasted in: *"Players report the Higher/Lower hints are sometimes wrong, on alternating guesses. Please (1) give me a fixed version of the code, and (2) explain why the bug happens. Keep the whole answer under 300 words."* Neither model could read the repo or see my fix.

**Honest caveat:** I could not reach ChatGPT, Gemini or Copilot from this environment, so both models are from the Claude family: **Claude Opus** (larger) and **Claude Haiku** (smaller, faster). I did not make up answers for other vendors. If your instructor requires a different vendor, paste the same prompt into one and add a third column.

| | Model A | Model B |
|-|---------|---------|
| **Model name** | Claude Opus | Claude Haiku |
| **Response summary** | Found *two* bugs: the int/str mix-up with the `TypeError` fallback, and the swapped hint messages. Fix: removed the even/odd switch and the `try/except`, swapped the messages, and added `int(guess), int(secret)` at the top of `check_guess`. | Found the same two bugs. Fix: removed the `try/except`, swapped the messages, and in the handler used `secret = int(st.session_state.secret)` before calling `check_guess`. |
| **More Pythonic?** | Slightly less. The `int()` coercion inside `check_guess` is redundant and can hide a bad type, which contradicts its own closing advice ("convert once, when values come in"). | Slightly more. `check_guess` stays a tiny pure comparison and the conversion happens once in the caller. Its "make sure the secret is stored as an int" advice was vague, though. |
| **Clearer explanation?** | Yes. It walked through why only *alternating* guesses fail, gave two concrete string-comparison examples (`"9" > "50"`, `"100" < "20"`), and pointed out the two bugs sometimes cancelled each other out, which explains why the hint was occasionally right by accident. It ended with a general lesson about `try/except TypeError`. | Good but shorter. It explained odd vs even attempts and gave one example (`"5" > "10"`), and noted why the win check still worked. It did not mention that the two bugs can mask each other. |

**Which did you prefer and why?**

For the *code*, the two fixes are nearly the same, and I slightly prefer Haiku's because `check_guess` stays a plain comparison. For the *explanation* I prefer Opus: the "why" is what you need to avoid repeating the bug, and only Opus explained the masking between the two bugs and ended with a rule you can reuse. My own fix (in the current repo) removed the string conversion entirely and made `check_guess` return only the outcome string, so the message text lives in `HINT_MESSAGES` in `app.py`. That is closest to Haiku's structure, plus Opus's lesson.

Both models caught the swapped hint messages without being told to look for them, which I had to find separately by playing the game.

**Tests:** `check_guess` is covered by `tests/test_game_logic.py` (`test_guess_too_high`, `test_guess_too_low`, `test_winning_guess`).
