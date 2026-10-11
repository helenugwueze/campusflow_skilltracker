"""Ticket models and validation rules for CampusFlow."""

from __future__ import annotations

import re
from typing import Iterable

VALID_CATEGORIES = {"network", "hardware", "software", "other"}
VALID_URGENCIES = {"low", "medium", "high"}
PRIORITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1}
_NEXT_TICKET_NUMBER = 0


def _sync_next_ticket_number(existing_tickets: Iterable[dict] | None = None) -> int:
    global _NEXT_TICKET_NUMBER
    max_value = 0
    for ticket in existing_tickets or []:
        match = re.fullmatch(r"T(\d+)", str(ticket.get("id", "")).strip(), flags=re.IGNORECASE)
        if match:
            max_value = max(max_value, int(match.group(1)))
    if max_value > _NEXT_TICKET_NUMBER:
        _NEXT_TICKET_NUMBER = max_value
    return _NEXT_TICKET_NUMBER


def normalize_category(category: str) -> str:
    """Normalize category names to the accepted canonical labels."""
    if category is None:
        raise ValueError("Category is required.")
    cleaned = str(category).strip()
    normalized = cleaned.lower()
    if normalized not in VALID_CATEGORIES:
        raise ValueError("Invalid category. Allowed categories: Network, Hardware, Software, Other.")
    return cleaned.title() if cleaned.title() in {"Network", "Hardware", "Software", "Other"} else cleaned.title()


def normalize_urgency(urgency: str) -> str:
    """Normalize urgency values to lowercase and validate them."""
    if urgency is None:
        raise ValueError("Urgency is required.")
    cleaned = str(urgency).strip().lower()
    if cleaned not in VALID_URGENCIES:
        raise ValueError("Invalid urgency. Allowed values: low, medium, high.")
    return cleaned


def _ticket_number(ticket_id: str) -> int:
    match = re.fullmatch(r"T(\d+)", str(ticket_id or "").strip(), flags=re.IGNORECASE)
    if not match:
        return 0
    return int(match.group(1))


def reset_ticket_counter() -> None:
    """Reset the in-memory counter used for sequential ticket IDs."""
    global _NEXT_TICKET_NUMBER
    _NEXT_TICKET_NUMBER = 0


def sync_ticket_counter(existing_tickets: Iterable[dict] | None = None) -> None:
    """Align the in-memory counter with the highest ticket ID already present."""
    global _NEXT_TICKET_NUMBER
    _NEXT_TICKET_NUMBER = max(_NEXT_TICKET_NUMBER, _sync_next_ticket_number(existing_tickets))


def generate_ticket_id(existing_tickets: Iterable[dict] | None = None) -> str:
    """Generate the next ticket ID in the T001, T002 pattern."""
    global _NEXT_TICKET_NUMBER
    highest = _sync_next_ticket_number(existing_tickets)
    _NEXT_TICKET_NUMBER = highest + 1
    return f"T{highest + 1:03d}"


def calculate_priority(urgency: str, affected_users: int) -> str:
    """Apply the required business rules in their exact precedence order."""
    normalized_urgency = normalize_urgency(urgency)
    if normalized_urgency == "high" and affected_users >= 10:
        return "critical"
    if normalized_urgency == "high" or affected_users >= 10:
        return "high"
    if normalized_urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def create_ticket(title: str, category: str, urgency: str, affected_users: int, existing_tickets: Iterable[dict] | None = None) -> dict:
    """Create a valid ticket dictionary and calculate its priority."""
    if title is None or not str(title).strip():
        raise ValueError("Title must not be blank.")

    if not isinstance(affected_users, int) or isinstance(affected_users, bool):
        raise ValueError("affected_users must be a positive integer.")
    if affected_users <= 0:
        raise ValueError("affected_users must be a positive integer.")

    normalized_category = normalize_category(category)
    normalized_urgency = normalize_urgency(urgency)
    priority = calculate_priority(normalized_urgency, affected_users)

    ticket = {
        "id": generate_ticket_id(existing_tickets),
        "title": str(title).strip(),
        "category": normalized_category,
        "urgency": normalized_urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }
    return ticket
