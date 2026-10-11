"""Assignment and ticket lifecycle logic for CampusFlow."""

from __future__ import annotations

PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def _numeric_ticket_id(ticket_id: str) -> int:
    suffix = str(ticket_id or "").strip().upper()
    if suffix.startswith("T") and suffix[1:].isdigit():
        return int(suffix[1:])
    return 0


def assign_ticket(ticket: dict, assignee: str) -> dict:
    """Assign a ticket to a non-empty staff member."""
    if assignee is None or not str(assignee).strip():
        raise ValueError("Assignee name cannot be empty.")

    updated = dict(ticket)
    updated["assigned_to"] = str(assignee).strip()
    return updated


def update_status(ticket: dict, next_status: str) -> dict:
    """Transition a ticket through the valid lifecycle stages."""
    current = str(ticket.get("status", "open")).strip().lower()
    requested = str(next_status).strip().lower()

    if requested == "reopen":
        if current != "resolved":
            raise ValueError("Only a resolved ticket can be reopened.")
        updated = dict(ticket)
        updated["status"] = "open"
        return updated

    if requested == "open":
        if current == "resolved":
            raise ValueError("A resolved ticket must be explicitly reopened before it can be modified.")
        updated = dict(ticket)
        updated["status"] = "open"
        return updated

    if requested == "in_progress":
        if current == "resolved":
            raise ValueError("A resolved ticket may only be modified after an explicit reopen.")
        if not ticket.get("assigned_to") or not str(ticket.get("assigned_to")).strip():
            raise ValueError("An unassigned ticket cannot move to in_progress.")
        updated = dict(ticket)
        updated["status"] = "in_progress"
        return updated

    if requested == "resolved":
        if current == "open":
            raise ValueError("A ticket must move through in_progress before it can be resolved.")
        if current == "resolved":
            return dict(ticket)
        if not ticket.get("assigned_to") or not str(ticket.get("assigned_to")).strip():
            raise ValueError("A ticket must be assigned before it can be resolved.")
        updated = dict(ticket)
        updated["status"] = "resolved"
        return updated

    raise ValueError(f"Invalid status: {next_status}")


def get_queue(tickets: list[dict]) -> list[dict]:
    """Return unresolved tickets ordered by priority and ticket number."""
    unresolved = [
        ticket for ticket in tickets
        if str(ticket.get("status", "open")).strip().lower() != "resolved"
    ]
    return sorted(
        unresolved,
        key=lambda ticket: (
            PRIORITY_ORDER.get(str(ticket.get("priority", "low")).strip().lower(), 99),
            _numeric_ticket_id(ticket.get("id")),
        ),
    )
