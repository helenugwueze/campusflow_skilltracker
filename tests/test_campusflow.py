import json
import os
import tempfile
import unittest

from campusflow.tickets import create_ticket, reset_ticket_counter
from campusflow.workflow import assign_ticket, get_queue, update_status
from campusflow.reports import generate_report
from campusflow.storage import save_tickets, load_tickets


class TestTicketCreation(unittest.TestCase):
    def setUp(self):
        reset_ticket_counter()

    def test_high_urgency_twelve_users_is_critical(self):
        ticket = create_ticket("Campus Wi-Fi is down", "Network", "high", 12)
        self.assertEqual(ticket["priority"], "critical")

    def test_high_urgency_two_users_is_high(self):
        ticket = create_ticket("Printer jam", "Hardware", "high", 2)
        self.assertEqual(ticket["priority"], "high")

    def test_low_urgency_four_users_is_medium(self):
        ticket = create_ticket("Slow portal", "Software", "low", 4)
        self.assertEqual(ticket["priority"], "medium")

    def test_low_urgency_single_user_is_low(self):
        ticket = create_ticket("Need a clean desk", "Other", "low", 1)
        self.assertEqual(ticket["priority"], "low")

    def test_zero_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket("Broken scanner", "Hardware", "medium", 0)

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket("   ", "Software", "medium", 3)


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        reset_ticket_counter()

    def test_assign_ticket_to_staff_member(self):
        ticket = create_ticket("Laptop issue", "Hardware", "medium", 2)
        updated = assign_ticket(ticket, "Maya")
        self.assertEqual(updated["assigned_to"], "Maya")

    def test_unassigned_ticket_cannot_move_to_in_progress(self):
        ticket = create_ticket("VPN blocked", "Network", "high", 8)
        with self.assertRaises(ValueError):
            update_status(ticket, "in_progress")

    def test_assigned_ticket_progresses_to_resolved(self):
        ticket = create_ticket("Dev env broken", "Software", "medium", 4)
        ticket = assign_ticket(ticket, "Noah")
        ticket = update_status(ticket, "in_progress")
        ticket = update_status(ticket, "resolved")
        self.assertEqual(ticket["status"], "resolved")

    def test_reopening_resolved_ticket_is_allowed(self):
        ticket = create_ticket("Portal outage", "Network", "high", 10)
        ticket = assign_ticket(ticket, "Ava")
        ticket = update_status(ticket, "in_progress")
        ticket = update_status(ticket, "resolved")
        reopened = update_status(ticket, "reopen")
        self.assertEqual(reopened["status"], "open")

    def test_queue_orders_by_priority_and_id(self):
        tickets = [
            create_ticket("Ticket 3", "Other", "low", 2),
            create_ticket("Ticket 1", "Network", "high", 10),
            create_ticket("Ticket 2", "Hardware", "medium", 5),
            create_ticket("Ticket 4", "Software", "low", 1),
        ]
        tickets[1] = assign_ticket(tickets[1], "A")
        tickets[2] = assign_ticket(tickets[2], "B")
        ordered = get_queue(tickets)
        self.assertEqual([item["id"] for item in ordered], ["T002", "T003", "T001", "T004"])


class TestReportsAndPersistence(unittest.TestCase):
    def setUp(self):
        reset_ticket_counter()

    def test_report_handles_empty_ticket_list(self):
        report = generate_report([])
        self.assertEqual(report["total_tickets"], 0)
        self.assertEqual(report["status_breakdown"], {"open": 0, "in_progress": 0, "resolved": 0})
        self.assertEqual(report["priority_breakdown"], {"critical": 0, "high": 0, "medium": 0, "low": 0})

    def test_report_counts_statuses_and_priorities(self):
        tickets = [
            create_ticket("A", "Network", "high", 12),
            create_ticket("B", "Software", "medium", 2),
            create_ticket("C", "Other", "low", 1),
        ]
        tickets[0] = assign_ticket(tickets[0], "Rae")
        tickets[0] = update_status(tickets[0], "in_progress")
        tickets[1] = assign_ticket(tickets[1], "Kai")
        tickets[1] = update_status(tickets[1], "in_progress")
        tickets[1] = update_status(tickets[1], "resolved")
        report = generate_report(tickets)
        self.assertEqual(report["total_tickets"], 3)
        self.assertEqual(report["status_breakdown"]["in_progress"], 1)
        self.assertEqual(report["status_breakdown"]["resolved"], 1)
        self.assertEqual(report["priority_breakdown"]["critical"], 1)
        self.assertEqual(report["priority_breakdown"]["low"], 1)

    def test_save_and_reload_preserves_ticket_data(self):
        tickets = [create_ticket("Campus Wi-Fi is down", "Network", "high", 12)]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "tickets.json")
            save_tickets(path, tickets)
            reloaded = load_tickets(path)
            self.assertEqual(len(reloaded), 1)
            self.assertEqual(reloaded[0]["title"], "Campus Wi-Fi is down")
            self.assertEqual(reloaded[0]["id"], tickets[0]["id"])

    def test_create_ticket_after_reload_keeps_unique_ids(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "tickets.json")
            save_tickets(path, [create_ticket("One", "Network", "low", 1)])
            tickets = load_tickets(path)
            tickets.append(create_ticket("Two", "Hardware", "medium", 2))
            save_tickets(path, tickets)
            reloaded = load_tickets(path)
            self.assertEqual([ticket["id"] for ticket in reloaded], ["T001", "T002"])

    def test_invalid_json_clears_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "tickets.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"bad": True}, f)
            with self.assertRaises(ValueError):
                load_tickets(path)


if __name__ == "__main__":
    unittest.main()
