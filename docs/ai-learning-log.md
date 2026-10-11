# AI learning log

## Fellow: Developer B

### Interaction #1 — JSON persistence and error handling

Problem: I needed to understand how to save and reload ticket data without silently deleting valid information when the file was malformed.

My initial understanding: JSON should be serialised in a predictable structure, and missing data should not crash the program if the file is absent.

Prompt to AI: "Explain how json.load() behaves with a missing file and malformed JSON, and show a tiny example of handling errors cleanly in Python."

Useful AI guidance: The AI explained that `json.load()` raises `FileNotFoundError` for a missing file and `JSONDecodeError` for broken JSON. It also suggested validating the top-level type before handling the records.

My independent experiment/test: I wrote a tiny script that attempted to open a file that did not exist and another file with invalid JSON, then checked the exact exception types.

Verification source or result: Python raised `FileNotFoundError` and `JSONDecodeError`, which matched the guidance.

Decision: I accepted this approach and added explicit checks in `campusflow/storage.py` so the CLI shows a clear message and does not erase stored tickets.

Related file/commit: `campusflow/storage.py`, `tests/test_campusflow.py`

What I can now explain without AI: JSON storage is easiest when the file is treated as a list of dictionaries, and each load should validate the payload before data is used.

### Interaction #2 — Status workflow rules

Problem: I wanted to be sure about what a valid ticket lifecycle should allow and what should be rejected.

My initial understanding: A ticket should move `open -> in_progress -> resolved`, and only a reopened ticket should return to `open`.

Prompt to AI: "Describe a safe way to model a finite status workflow in Python, and show a small example of rejecting invalid transitions without hiding the reason."

Useful AI guidance: The AI suggested keeping status checks explicit and validating both the current state and the assignee before allowing a transition.

My independent experiment/test: I manually tested `update_status()` with valid and invalid combinations such as `open -> resolved`, `unassigned -> in_progress`, and `resolved -> reopen`.

Verification source or result: The function raised `ValueError` for invalid transitions and returned the updated ticket for valid ones.

Decision: I improved the implementation by validating both assignment and state before the transition.

Related file/commit: `campusflow/workflow.py`

What I can now explain without AI: A workflow should reject invalid movement early and keep the business rule in one place so every caller sees the same behaviour.

### Interaction #3 — Review and corrective debugging

Problem: A failing test showed that a resolved ticket was being accepted without going through `in_progress`, which contradicted the project specification.

My initial understanding: A direct `open -> resolved` transition should be rejected to follow the required lifecycle.

Prompt to AI: "Here is the failing status test and traceback. Help me isolate whether the bug is in the rule order or the state validation, and give experiments rather than a rewrite."

Useful AI guidance: The AI advised checking the exact transition guard for `resolved` and confirming whether the code allowed the wrong state to progress.

My independent experiment/test: I ran the focused unittest output and inspected the transition branch in `campusflow/workflow.py` before changing it.

Verification source or result: The test confirmed `open -> resolved` was incorrectly allowed; I corrected the guard and reran the suite.

Decision: I rejected the shortcut and restored the required sequence. This illustrated the importance of verifying AI suggestions against the written requirements.

Related file/commit: `campusflow/workflow.py`, `tests/test_campusflow.py`

What I can now explain without AI: AI can suggest a quick fix, but I still need to check the requirement text and the failing test to verify the real rule before committing to the change.
