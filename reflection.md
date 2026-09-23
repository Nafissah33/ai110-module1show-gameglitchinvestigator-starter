# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
It did look like a console, didn't have many options, ut i was still working and gave many failed attempts befor the game is over.
- List at least two concrete bugs you noticed at the start  
When i clicked on the return button from my computer, it didn't work. I had to hit submit. when I found the answer that was 2, it didn't let me do new game.
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.
-Game never resets.
-the code doesn't look like it has a break, out of the loop.
-it misfires, when an even-numbered attempt with a two-digit secret. 

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Won a round, then clicked "New Game 🔁" | Game resets to "playing" so I can enter a new guess | Page kept showing "You already won. Start a new game to play again." — clicking New Game had no visible effect | None — silent bug (`st.session_state.status` was never reset) |
| Loaded the app fresh on Normal difficulty (8 attempts allowed), before submitting any guess | "Attempts left: 8" | "Attempts left: 7" shown immediately, and the game ended after only 7 real guesses instead of 8 | None — `st.session_state.attempts` starts at 1 instead of 0 |
| Checked Debug Info (Secret: 50), then submitted 9 as my first guess | "Too Low" hint (9 < 50) | "Too High" hint shown instead | None shown in browser, but comparing an int guess to a str secret raises `TypeError` internally, caught silently and mishandled |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project .
Claude AI
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
My terminal said command not found for python/pip. The AI explained macOS didn't have those names — I needed python3/pip3 instead.I ran which python3, confirmed it existed, then ran python3 -m streamlit run app.py and the app launched successfully.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
Offered to just fill in the whole bug table for me, and recommended guiding me step-by-step as the alternative. I wanted code explained directly,perhaps showing some examples.Ran the app myself and confirmed the explained bugs actually showed up when I played.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I re-ran the exact scenario that triggered the bug and checked the behavior changed. For the "New Game never resets" bug, I won a round, clicked New Game, and confirmed I could play again instead of getting stuck on "Game over."


- Describe at least one test you ran (manual or using pytest)
I ran pytest tests/ and got 3 failures, all NotImplementedError, because logic_utils.py still had stub functions — the logic hadn't been refactored out of app.py yet. This told me the refactor step (README #4) was still outstanding, not just the bug fixes.  
  and what it showed you about your code.

- Did AI help you design or understand any tests? How?
Yes — while looking at the pytest failures, the AI pointed out that tests/test_game_logic.py expects check_guess to return a plain string like "Win", but the current check_guess in app.py returns a tuple (outcome, message). I wouldn't have caught that mismatch just by reading the error message alone.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Every button click reruns the whole script from top to bottom. Normal variables reset each time — st.session_state is the only thing that survives. That's why the New Game bug happened: it reset secret/attempts but forgot status, so the stale value carried over. Every click makes Streamlit re-read the whole script from scratch, like closing and reopening a book. session_state is a sticky note that survives the reread — forget to update one, and the old value sticks around.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
Before trusting that a fix worked, reproduce the exact broken scenario again and watch it behave differently , don't just assume the code change fixed it. Running pytest and manually replaying the bug (e.g., clicking New Game after winning) caught things a quick glance at the code wouldn't have.

  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?

I would make sure only one Streamlit server is running at a time; I ended up with two instances on different ports (8501 and 8502) and confused myself about which one I was testing.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

I think AI is great tool for novices like me. I didn't understand the code but it helped breaking it down and fixing bugs.