"""Ticket assignment, status changes, and work-queue lookup operations."""


def assign_ticket(tickets: list[dict], ticket_id: str, assignee: str) -> dict:
    """Assign a ticket to a person.

    Arguments: tickets, the list of ticket dictionaries; ticket_id and assignee identify the ticket and assignee.
    Returns: The updated ticket dictionary.
    Raises: ValueError with a clear message for invalid input or an unknown ticket; NotImplementedError until implemented.
    """
    raise NotImplementedError


def change_status(tickets: list[dict], ticket_id: str, status: str) -> dict:
    """Change a ticket's status.

    Arguments: tickets, the list of ticket dictionaries; ticket_id and status identify the ticket and new status.
    Returns: The updated ticket dictionary.
    Raises: ValueError with a clear message for invalid input or an unknown ticket; NotImplementedError until implemented.
    """
    raise NotImplementedError


def reopen_ticket(tickets: list[dict], ticket_id: str) -> dict:
    """Reopen a ticket.

    Arguments: tickets, the list of ticket dictionaries; ticket_id identifies the ticket to reopen.
    Returns: The updated ticket dictionary.
    Raises: ValueError with a clear message for invalid input or an unknown ticket; NotImplementedError until implemented.
    """
    raise NotImplementedError


def get_work_queue(tickets: list[dict]) -> list[dict]:
    """Return tickets that are waiting for work.

    Arguments: tickets, the list of ticket dictionaries.
    Returns: A list of ticket dictionaries in the work queue.
    Raises: NotImplementedError until implemented.
    """
    raise NotImplementedError


def find_ticket(tickets: list[dict], ticket_id: str) -> dict:
    """Find a ticket by its identifier.

    Arguments: tickets, the list of ticket dictionaries; ticket_id identifies the ticket.
    Returns: The matching ticket dictionary.
    Raises: ValueError with a clear message for invalid input or an unknown ticket; NotImplementedError until implemented.
    """
    raise NotImplementedError