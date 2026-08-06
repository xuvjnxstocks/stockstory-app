from pathlib import Path

import pytest

from src.draven_engine import build_report, calculate_metrics, load_json, milestone_per_share, validate_case


ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = ROOT / "cases" / "zyme_2026_08_25.json"
SCHEMA_PATH = ROOT / "schemas" / "case.schema.json"


def test_reference_case_validates() -> None:
    case = load_json(CASE_PATH)
    schema = load_json(SCHEMA_PATH)
    assert validate_case(case, schema) == []


def test_probabilities_and_expected_value_are_deterministic() -> None:
    case = load_json(CASE_PATH)
    metrics = calculate_metrics(case)
    assert metrics.scenario_count == 5
    assert metrics.probability_weighted_value == pytest.approx(27.2125)
    assert metrics.expected_return == pytest.approx(0.150148, abs=1e-6)
    assert metrics.downside_probability == pytest.approx(0.07)
    assert metrics.upside_probability == pytest.approx(0.93)


def test_milestone_per_share_reconciles() -> None:
    case = load_json(CASE_PATH)
    assert milestone_per_share(case) == pytest.approx(3.4236)


def test_report_contains_audit_fields() -> None:
    report, metrics = build_report(CASE_PATH, SCHEMA_PATH)
    assert "Evidence ledger" in report
    assert "Falsifiers" in report
    assert "Instrument gate" in report
    assert metrics.version_hash in report


def test_probability_sum_failure_is_rejected() -> None:
    case = load_json(CASE_PATH)
    schema = load_json(SCHEMA_PATH)
    case["scenarios"][0]["probability"] = 0.31
    errors = validate_case(case, schema)
    assert any("probabilities sum" in error for error in errors)
