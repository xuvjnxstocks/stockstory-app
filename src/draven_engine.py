from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


@dataclass(frozen=True)
class CaseMetrics:
    probability_weighted_value: float
    expected_return: float
    downside_probability: float
    upside_probability: float
    scenario_count: int
    version_hash: str


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def version_hash(data: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()[:12]


def validate_case(case: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(case), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "root"
        errors.append(f"{location}: {error.message}")

    probabilities = [float(item["probability"]) for item in case.get("scenarios", [])]
    if probabilities and abs(sum(probabilities) - 1.0) > 1e-9:
        errors.append(f"scenarios: probabilities sum to {sum(probabilities):.6f}, not 1.000000")

    evidence_ids = {item["id"] for item in case.get("evidence", [])}
    for index, catalyst in enumerate(case.get("catalysts", [])):
        missing = [source_id for source_id in catalyst.get("source_ids", []) if source_id not in evidence_ids]
        if missing:
            errors.append(f"catalysts.{index}: unknown source_ids {missing}")

    assumptions = case.get("assumptions", {})
    approval_probability = assumptions.get("approval_probability")
    if approval_probability is not None and not 0 <= float(approval_probability) <= 1:
        errors.append("assumptions.approval_probability must be between 0 and 1")

    return errors


def calculate_metrics(case: dict[str, Any]) -> CaseMetrics:
    spot = float(case["security"]["price"])
    scenarios = case["scenarios"]
    fair_value = sum(float(item["probability"]) * float(item["terminal_price"]) for item in scenarios)
    expected_return = fair_value / spot - 1.0
    downside_probability = sum(
        float(item["probability"]) for item in scenarios if float(item["terminal_price"]) < spot
    )
    upside_probability = sum(
        float(item["probability"]) for item in scenarios if float(item["terminal_price"]) > spot
    )
    return CaseMetrics(
        probability_weighted_value=round(fair_value, 4),
        expected_return=round(expected_return, 6),
        downside_probability=round(downside_probability, 6),
        upside_probability=round(upside_probability, 6),
        scenario_count=len(scenarios),
        version_hash=version_hash(case),
    )


def milestone_per_share(case: dict[str, Any]) -> float | None:
    milestone_m = case.get("assumptions", {}).get("approval_milestone_m")
    shares_m = case.get("security", {}).get("basic_shares_m")
    if milestone_m is None or shares_m is None:
        return None
    return round(float(milestone_m) / float(shares_m), 4)


def render_markdown(case: dict[str, Any], metrics: CaseMetrics) -> str:
    security = case["security"]
    lines = [
        f"# {security['ticker']}: {case['title']}",
        "",
        f"**Company:** {security['company']}  ",
        f"**Evidence cut-off:** {case['cutoff']}  ",
        f"**Case version:** `{metrics.version_hash}`",
        "",
        "## Investment conclusion",
        "",
        case["investment_conclusion"],
        "",
        "## Calculated event metrics",
        "",
        f"- Reference price: ${security['price']:.2f}",
        f"- Probability-weighted value: ${metrics.probability_weighted_value:.2f}",
        f"- Expected return: {metrics.expected_return:.1%}",
        f"- Probability above spot: {metrics.upside_probability:.1%}",
        f"- Probability below spot: {metrics.downside_probability:.1%}",
        "",
        "## Scenario distribution",
        "",
        "| Scenario | Probability | Terminal price | Drivers |",
        "|---|---:|---:|---|",
    ]
    for scenario in case["scenarios"]:
        drivers = "; ".join(scenario["drivers"])
        lines.append(
            f"| {scenario['name']} | {scenario['probability']:.1%} | ${scenario['terminal_price']:.2f} | {drivers} |"
        )

    lines.extend(["", "## Evidence ledger", "", "| ID | Claim | Tier | Confidence | As of |", "|---|---|---|---|---|"])
    for evidence in case["evidence"]:
        lines.append(
            f"| {evidence['id']} | {evidence['claim']} | {evidence['source_tier']} | {evidence['confidence']} | {evidence['as_of']} |"
        )

    lines.extend(["", "## Falsifiers", ""])
    lines.extend(f"- {item}" for item in case["falsifiers"])
    lines.extend(["", "## Instrument gate", "", f"**Preferred:** {case['instrument_gate']['preferred']}"])
    lines.extend(f"- Rejected: {item}" for item in case["instrument_gate"].get("rejected", []))
    lines.extend(
        [
            "",
            "---",
            "",
            "This research output is generated from a versioned public-information dossier. It is not investment advice.",
        ]
    )
    return "\n".join(lines)


def build_report(case_path: str | Path, schema_path: str | Path) -> tuple[str, CaseMetrics]:
    case = load_json(case_path)
    schema = load_json(schema_path)
    errors = validate_case(case, schema)
    if errors:
        raise ValueError("Invalid case:\n" + "\n".join(f"- {error}" for error in errors))
    metrics = calculate_metrics(case)
    return render_markdown(case, metrics), metrics
