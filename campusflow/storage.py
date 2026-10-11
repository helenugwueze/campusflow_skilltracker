"""JSON persistence for CampusFlow ticket data."""

from __future__ import annotations

import json
import os
from typing import Iterable

from campusflow.tickets import sync_ticket_counter


def _validate_ticket(ticket: dict) -> dict:
    if not isinstance(ticket, dict):
        raise ValueError("Each stored record must be a dictionary.")
    required = {"id", "title", "category", "urgency", "affected_users", "priority", "status", "assigned_to"}
    missing = sorted(required - set(ticket.keys()))
    if missing:
        raise ValueError(f"Ticket record is missing required fields: {', '.join(missing)}")
    return ticket


def load_tickets(path: str) -> list[dict]:
    """Load tickets from disk. Missing files result in an empty list."""
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON in ticket storage: {path}") from exc

    if not isinstance(payload, list):
        raise ValueError("Ticket data must be stored as a JSON list.")

    validated = [_validate_ticket(ticket) for ticket in payload]
    seen_ids = set()
    for ticket in validated:
        ticket_id = str(ticket["id"])
        if ticket_id in seen_ids:
            raise ValueError(f"Duplicate ticket IDs are not allowed: {ticket_id}")
        seen_ids.add(ticket_id)
    sync_ticket_counter(validated)
    return validated


def save_tickets(path: str, tickets: Iterable[dict]) -> None:
    """Persist ticket data to disk in JSON format."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(path, "w", encoding="utf-8") as handle:
        json.dump(list(tickets), handle, indent=2)
        handle.write("\n")
