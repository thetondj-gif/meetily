#!/usr/bin/env python3
"""Secret-free, offline acceptance runner for DAWN Meeting Command."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
MAX_CONTENT = 200_000
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d .()-]{7,}\d)(?!\w)")

CATEGORIES = {
    "pains": ("problem", "issue", "manual", "takes too long", "bottleneck"),
    "requirements": ("we need", "need to", "must", "want", "require"),
    "objections": ("concern", "too expensive", "budget", "risk", "worried"),
    "buying_signals": ("next step", "proposal", "when can", "start", "move forward"),
}


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {"schema_version", "meeting_id", "source_type", "authorised", "content"}
    missing = sorted(required - payload.keys())
    if missing:
        errors.append(f"missing:{','.join(missing)}")
    if payload.get("schema_version") != 1:
        errors.append("schema_version")
    if payload.get("source_type") not in {"transcript", "audio_file_reference"}:
        errors.append("source_type")
    if payload.get("authorised") is not True:
        errors.append("authorised")
    content = payload.get("content")
    if not isinstance(content, str) or not content.strip() or len(content) > MAX_CONTENT:
        errors.append("content")
    return errors


def redact(text: str) -> str:
    return PHONE_RE.sub("[REDACTED_PHONE]", EMAIL_RE.sub("[REDACTED_EMAIL]", text))


def analyse(payload: dict[str, Any]) -> dict[str, Any]:
    errors = validate(payload)
    if errors:
        return {
            "schema_version": 1,
            "meeting_id": str(payload.get("meeting_id", "invalid")),
            "status": "blocked",
            "summary": "Input rejected by the DAWN authority and schema gate.",
            "actions": [],
            "evidence": [],
            "warnings": errors,
            "external_actions_performed": False,
        }

    content = redact(payload["content"]) if payload.get("redact_personal_data", True) else payload["content"]
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", content) if s.strip()]
    result: dict[str, Any] = {
        "schema_version": 1,
        "meeting_id": payload["meeting_id"],
        "status": "success",
        "summary": " ".join(sentences[:3])[:6000],
        "actions": [],
        "evidence": [],
        "warnings": [],
        "external_actions_performed": False,
    }
    for category, markers in CATEGORIES.items():
        result[category] = [s for s in sentences if any(m in s.lower() for m in markers)][:50]
    for index, sentence in enumerate(sentences):
        lower = sentence.lower()
        if any(marker in lower for marker in ("i will", "we will", "can you", "please", "next step")):
            ref = f"transcript:{index + 1}"
            result["actions"].append({"action": sentence[:1000], "owner": "unassigned", "deadline": None, "evidence_refs": [ref]})
            result["evidence"].append(ref)
    result["follow_up_draft"] = None
    result["crm_payload"] = None
    result["opportunity_score"] = min(100, 20 * len(result["buying_signals"]) + 10 * len(result["requirements"]))
    return result


def main() -> int:
    valid = json.loads((ROOT / "fixtures" / "valid-transcript.json").read_text())
    invalid = json.loads((ROOT / "fixtures" / "invalid-transcript.json").read_text())
    accepted = analyse(valid)
    refused = analyse(invalid)
    redacted_content = redact(valid["content"])
    assertions = [
        accepted["status"] == "success",
        accepted["external_actions_performed"] is False,
        "[REDACTED_EMAIL]" in redacted_content and "founder@example.com" not in redacted_content,
        "[REDACTED_PHONE]" in redacted_content and "+44 7700 900123" not in redacted_content,
        bool(accepted["requirements"]),
        refused["status"] == "blocked",
        "authorised" in refused["warnings"],
    ]
    report = {
        "capability": "dawn.meeting-command",
        "status": "passed" if all(assertions) else "failed",
        "tests": len(assertions),
        "passed": sum(assertions),
        "network_used": False,
        "credentials_required": False,
        "external_actions_performed": False,
    }
    print(json.dumps(report, indent=2))
    return 0 if all(assertions) else 1


if __name__ == "__main__":
    sys.exit(main())
