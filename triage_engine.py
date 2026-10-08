
import csv
from datetime import datetime
import json
import re

# SLA Target configuration in hours
SLA_HOURS_MAP = {
    "URGENT": 4,
    "MEDIUM": 12,
    "LOW": 24
}

# Keyword rules for priority triage classification
TRIAGE_RULES = {
    "URGENT": [r"payment failed", r"money debited", r"crash", r"urgently", r"error 500"],
    "MEDIUM": [r"updating", r"delivery address", r"delay", r"order status"],
    "LOW": [r"inquiry", r"subscription", r"pricing", r"how to"]
}


def load_tickets(file_path="tickets.json"):
    """Loads raw ticket records from JSON file with error handling."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"[ERROR] '{file_path}' file kanapadaledhu.")
        return []
    except json.JSONDecodeError:
        print(f"[ERROR] '{file_path}' lo JSON format invalid ga undhi.")
        return []


def classify_priority(subject_text):
    """Categorizes priority based on regex pattern matching."""
    text = subject_text.lower()
    for priority, patterns in TRIAGE_RULES.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return priority
    return "LOW"


def evaluate_sla(created_at_str, priority):
    """Calculates elapsed hours and determines whether SLA target is breached."""
    created_time = datetime.fromisoformat(created_at_str)
    current_time = datetime.now()

    elapsed_hours = (current_time - created_time).total_seconds() / 3600
    allowed_sla_hours = SLA_HOURS_MAP.get(priority, 24)

    is_breached = elapsed_hours > allowed_sla_hours
    hours_to_breach = round(allowed_sla_hours - elapsed_hours, 2)

    return {
        "elapsed_hours": round(elapsed_hours, 2),
        "allowed_sla_hours": allowed_sla_hours,
        "sla_breached": is_breached,
        "hours_to_breach": hours_to_breach
    }


def export_triage_report(triaged_tickets, output_file="triage_summary.csv"):
    """Exports processed triage results to a clean CSV summary report."""
    if not triaged_tickets:
        print("[WARNING] Export cheyyadaniki ticket data em ledu.")
        return

    fieldnames = [
        "ticket_id",
        "customer_name",
        "priority",
        "status",
        "elapsed_hours",
        "allowed_sla_hours",
        "sla_breached",
        "hours_to_breach"
    ]

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in triaged_tickets:
            writer.writerow(row)

    print(f"\n[SUCCESS] Report exported successfully -> {output_file}")


def run_pipeline():
    print("=== Automated Customer Ticket Triage & SLA Engine ===")
    raw_tickets = load_tickets("tickets.json")

    if not raw_tickets:
        print("Ticket data dorakaledhu. Execution stop chestunnam.")
        return

    triaged_results = []

    for ticket in raw_tickets:
        priority = classify_priority(ticket.get("subject", ""))
        sla_info = evaluate_sla(ticket.get("created_at"), priority)

        record = {
            "ticket_id": ticket.get("ticket_id"),
            "customer_name": ticket.get("customer_name"),
            "priority": priority,
            "status": ticket.get("status"),
            "elapsed_hours": sla_info["elapsed_hours"],
            "allowed_sla_hours": sla_info["allowed_sla_hours"],
            "sla_breached": sla_info["sla_breached"],
            "hours_to_breach": sla_info["hours_to_breach"]
        }
        triaged_results.append(record)

        print(
            f"Ticket: {record['ticket_id']} | Priority: {priority:<7} | "
            f"Breached: {str(record['sla_breached']):<5} | Remaining: {record['hours_to_breach']} hrs"
        )

    export_triage_report(triaged_results)


if __name__ == "__main__":
    run_pipeline()
