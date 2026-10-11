# Design decisions

## Shared contracts

- The ticket list is stored as a Python list of dictionaries in memory and saved to JSON as a list of records.
- Validation raises `ValueError` with a clear message so the CLI can show a user-friendly error without mutating the record set.
- Creation and status updates return the updated ticket dictionary so the caller can replace the object in the collection.
- JSON loading and saving is owned in `campusflow/storage.py` and called by the CLI and tests.
- Business logic is isolated from CLI prompts so it can be unit-tested directly with plain Python data.

## Developer B ownership

- `campusflow/workflow.py`: ticket assignment and status transitions.
- `campusflow/reports.py`: totals and priority/status breakdowns.
- `campusflow/storage.py`: save/load JSON with validation and duplicate-ID checks.

## Lifecycle rules

- Unassigned tickets cannot move to `in_progress`.
- `resolved` tickets cannot be modified until an explicit `reopen` sets them back to `open`.
- The work queue shows unresolved tickets ordered by priority and then by ascending numeric ticket ID.
