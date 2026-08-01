# DAWN Meeting Command — Capability Foundry Wave 1

## Status

`CAPABILITY_RESEARCH_COMPLETE`

This branch is isolated from the active DAWN V2 rebuild and does not activate Meetily on the live Mac.

## Objective

Build an adapter that accepts an explicitly supplied audio file or transcript and returns a bounded, evidence-linked sales intelligence package:

- participants and organisation;
- meeting summary;
- pains and requirements;
- objections and buying signals;
- decision process and stakeholders;
- commitments, owners and deadlines;
- risks and next-best actions;
- reviewable follow-up email draft;
- CRM-ready structured payload;
- opportunity score and evidence references.

## First implementation slice

1. Define transcript-input and sales-intelligence output schemas.
2. Add a local-only adapter that performs no CRM write and sends no messages.
3. Add fixture-based tests using synthetic meeting transcripts.
4. Add redaction and maximum-input/output controls.
5. Produce a canary runbook for imported files only.

## Standard response envelope

```json
{
  "schema_version": 1,
  "capability": "dawn-meeting-command",
  "operation": "extract_sales_actions",
  "status": "success|partial|blocked|failed",
  "evidence": [],
  "data": {},
  "warnings": [],
  "cost": {"currency": "USD", "estimated": 0},
  "runtime": {
    "started_at": "ISO-8601",
    "completed_at": "ISO-8601",
    "duration_ms": 0
  }
}
```

## Wave 1 boundary

No always-on microphone capture, live CRM mutation, external message sending, credential binding, service installation, public deployment or DAWN runtime connection is permitted.

## Connection gate

The workstream may advance to `CAPABILITY_DAWN_CONNECTION_READY` only after schemas, isolated adapter tests, security review, evidence samples and rollback instructions exist. Live connection remains a separate post-rebuild decision.
