"""Command-line interface for CampusFlow."""

from __future__ import annotations

import os

from campusflow.reports import generate_report
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, get_queue, update_status

DATA_PATH = os.path.join("data", "tickets.json")


def load_ticket_store() -> list[dict]:
    try:
        return load_tickets(DATA_PATH)
    except ValueError as exc:
        raise SystemExit(f"Storage error: {exc}") from exc


def print_ticket(ticket: dict) -> None:
    print(f"ID: {ticket['id']}")
    print(f"Title: {ticket['title']}")
    print(f"Category: {ticket['category']}")
    print(f"Urgency: {ticket['urgency']}")
    print(f"Affected users: {ticket['affected_users']}")
    print(f"Priority: {ticket['priority']}")
    print(f"Status: {ticket['status']}")
    print(f"Assigned to: {ticket['assigned_to'] or 'Unassigned'}")
    print("-" * 40)


def create_ticket_from_cli(tickets: list[dict]) -> None:
    title = input("Title: ").strip()
    category = input("Category [Network/Hardware/Software/Other]: ").strip()
    urgency = input("Urgency [low/medium/high]: ").strip()
    affected_users = input("Affected users: ").strip()

    try:
        users = int(affected_users)
    except ValueError as exc:
        raise ValueError("affected_users must be a positive integer.") from exc

    ticket = create_ticket(title, category, urgency, users, existing_tickets=tickets)
    tickets.append(ticket)
    save_tickets(DATA_PATH, tickets)
    print(f"Ticket {ticket['id']} created successfully.")


def assign_ticket_from_cli(tickets: list[dict]) -> None:
    ticket_id = input("Ticket ID: ").strip().upper()
    assignee = input("Assign to: ").strip()
    match = next((ticket for ticket in tickets if ticket["id"].upper() == ticket_id), None)
    if match is None:
        raise ValueError(f"Unknown ticket ID: {ticket_id}")
    updated = assign_ticket(match, assignee)
    index = tickets.index(match)
    tickets[index] = updated
    save_tickets(DATA_PATH, tickets)
    print(f"Ticket {ticket_id} assigned to {assignee}.")


def update_ticket_status(tickets: list[dict]) -> None:
    ticket_id = input("Ticket ID: ").strip().upper()
    status = input("New status [open/in_progress/resolved/reopen]: ").strip().lower()
    match = next((ticket for ticket in tickets if ticket["id"].upper() == ticket_id), None)
    if match is None:
        raise ValueError(f"Unknown ticket ID: {ticket_id}")
    updated = update_status(match, status)
    index = tickets.index(match)
    tickets[index] = updated
    save_tickets(DATA_PATH, tickets)
    print(f"Ticket {ticket_id} status is now {updated['status']}.")


def show_all_tickets(tickets: list[dict]) -> None:
    if not tickets:
        print("No tickets found.")
        return
    for ticket in tickets:
        print_ticket(ticket)


def show_ticket_details(tickets: list[dict]) -> None:
    ticket_id = input("Ticket ID: ").strip().upper()
    match = next((ticket for ticket in tickets if ticket["id"].upper() == ticket_id), None)
    if match is None:
        raise ValueError(f"Unknown ticket ID: {ticket_id}")
    print_ticket(match)


def menu() -> None:
    tickets = load_ticket_store()
    while True:
        print("\nCampusFlow Helpdesk")
        print("1. Create ticket")
        print("2. List all tickets")
        print("3. View ticket")
        print("4. Assign ticket")
        print("5. Update status")
        print("6. Work queue")
        print("7. Reports")
        print("8. Exit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                create_ticket_from_cli(tickets)
            elif choice == "2":
                show_all_tickets(tickets)
            elif choice == "3":
                show_ticket_details(tickets)
            elif choice == "4":
                assign_ticket_from_cli(tickets)
            elif choice == "5":
                update_ticket_status(tickets)
            elif choice == "6":
                queue = get_queue(tickets)
                if not queue:
                    print("No unresolved tickets in the queue.")
                else:
                    for ticket in queue:
                        print_ticket(ticket)
            elif choice == "7":
                report = generate_report(tickets)
                print(f"Total tickets: {report['total_tickets']}")
                print(report['status_breakdown'])
                print(report['priority_breakdown'])
            elif choice == "8":
                print("Goodbye.")
                break
            else:
                print("Invalid option. Please choose 1-8.")
        except ValueError as exc:
            print(f"Invalid input: {exc}")


if __name__ == "__main__":
    menu()
