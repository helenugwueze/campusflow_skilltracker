"""Reporting helpers for CampusFlow."""

from __future__ import annotations


def generate_report(tickets: list[dict]) -> dict:
    """Summarize totals by status and priority."""
    status_breakdown = {"open": 0, "in_progress": 0, "resolved": 0}
    priority_breakdown = {"critical": 0, "high": 0, "medium": 0, "low": 0}

    for ticket in tickets:
        status = str(ticket.get("status", "open")).strip().lower()
        if status in status_breakdown:
            status_breakdown[status] += 1

        priority = str(ticket.get("priority", "low")).strip().lower()
        if priority in priority_breakdown:
            priority_breakdown[priority] += 1

    return {
        "total_tickets": len(tickets),
        "status_breakdown": status_breakdown,
        "priority_breakdown": priority_breakdown,
    }
