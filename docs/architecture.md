# Prototype architecture

React/Vite browser -> `/api/analyze` proxy -> FastAPI -> seven deterministic heuristic patterns -> risk score and explanations.

No external AI model, database, Gmail, SMS, Android access, message persistence, or authentication.

## Limitations
The score is an uncalibrated heuristic, not a probability. Both false positives and false negatives are expected. URLs are not fetched. Only synthetic messages should be used.

## Next work
Evaluate detection accuracy on labeled synthetic examples, study Gmail OAuth verification and Android permissions, and design authentication, rate limits, secure retention, consent, deletion, and accessible alerts.
