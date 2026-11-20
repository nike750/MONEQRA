import json
from pathlib import Path

folder = Path(".")

expected_files = [
    ("normal_transactions.json", "normal", 2, 173500.00),
    ("timeouts.json", "timeout", 2, 146000.00),
    ("delayed_confirmations.json", "delayed_confirmation", 1, 82000.00),
    ("duplicate_events.json", "duplicate_event", 1, 128500.00),
    ("upstream_infra_failure.json", "upstream_infrastructure_failure", 2, 215000.00),
    ("settlement_failure.json", "settlement_failure", 1, 940000.00),
    ("provider_recovery.json", "provider_recovery", 2, 73000.00),
]

all_events = []

for filename, expected_cat, expected_count, expected_total in expected_files:
    filepath = folder / filename
    assert filepath.exists(), f"Missing file: {filename}"

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("category") == expected_cat, f"{filename}: wrong category {data.get('category')}"
    events = data.get("events", [])
    assert len(events) == expected_count, f"{filename}: expected {expected_count} events, got {len(events)}"

    total_amount = sum(e.get("amount", 0.0) for e in events)
    assert round(total_amount, 2) == expected_total, f"{filename}: expected {expected_total}, got {total_amount}"

    for e in events:
        assert e.get("category") == expected_cat, f"{e.get('event_id')} category mismatch in {filename}"
        assert e.get("event_id") and e.get("occurred_at") and e.get("provider"), f"Missing required fields in {e}"
        all_events.append(e)

all_events.sort(key=lambda x: x["occurred_at"])
assert [e["event_id"] for e in all_events] == [
    "evt_001", "evt_002", "evt_003", "evt_004", "evt_005",
    "evt_006", "evt_007", "evt_008", "evt_009", "evt_010", "evt_011"
], "Timeline order or event IDs do not match!"

print(f"SUCCESS: All 7 files valid and all {len(all_events)} events reassemble cleanly in chronological order.")