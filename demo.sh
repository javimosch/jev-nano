#!/bin/sh
# smoke test against a running jev-nano server
B="${JEVNANO_URL:-http://127.0.0.1:8097}"
curl -s "$B/v1/systemone" -H 'content-type: application/json' -d '{
  "state": "Payouts failing for 3 days, help ASAP.",
  "model": "jev-latest",
  "questions": {
    "u": {"type": "noul", "instructions": "Does this convey urgency?"},
    "d": {"type": "choice", "instructions": "Which department owns this?",
          "criteria": {"billing": "payments and invoices",
                       "technical": "login and outage issues",
                       "returns": "refunds and returns"}},
    "r": {"type": "score", "instructions": "How risky is this interaction?",
          "criteria": ["low", "medium", "high"]}
  }
}' | python3 -m json.tool
