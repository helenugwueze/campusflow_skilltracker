# CampusFlow

CampusFlow is a Python command-line helpdesk application for tracking campus support tickets. It validates ticket inputs, calculates priority, assigns staff, manages the lifecycle, displays the work queue, and persists records to JSON.

## Team and roles

- Developer A: ticket creation, validation, and priority engine.
- Developer B: assignment, workflow, queue, reports, and storage.

## Requirements and setup

- Python 3.11+
- Clone the repo and run from the project root.

## Run the CLI

```bash
python main.py
```

Available menu options:

1. Create ticket
2. List all tickets
3. View one ticket
4. Assign a ticket
5. Update ticket status
6. Show the work queue
7. Show report summary
8. Exit

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Priority rules

Priority is calculated in this exact order:

1. high urgency and 10+ affected users -> critical
2. high urgency or 10+ affected users -> high
3. medium urgency or 3+ affected users -> medium
4. otherwise -> low

## Storage

Ticket records are stored in `data/tickets.json`. If the file is missing, the app starts with an empty list. If the file contains malformed JSON, the app raises a clear error instead of silently deleting data.

## Known limitations

- The interface is text-based and intentionally uses the standard library only.
- The app is designed for local CLI work and does not include a web UI.
- Ticket IDs are generated sequentially in the current runtime session and reload from the saved records.
