import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from decision_engine import should_recover, validate_component


def test_high_confidence_simple_component_is_recoverable():
    component = {"id": "R1", "type": "Resistor", "vision_confidence": 0.96}
    decision = should_recover(component)
    assert decision.recoverable is True
    assert decision.recoverability == "HIGH"


def test_low_confidence_component_is_deferred():
    component = {"id": "U1", "type": "IC", "vision_confidence": 0.89}
    decision = should_recover(component)
    assert decision.recoverable is False
    assert decision.recoverability == "LOW"


def test_unsupported_package_type_is_deferred_even_with_high_confidence():
    component = {"id": "U2", "type": "IC", "vision_confidence": 0.99}
    decision = should_recover(component)
    assert decision.recoverable is False
    assert "not yet supported" in decision.reason


def test_validate_component_within_tight_tolerance_grades_a():
    component = {"id": "R1", "type": "Resistor"}
    result = validate_component(component, measured_value=10_000)
    assert result.grade == "A"
    assert result.passed is True


def test_validate_component_far_out_of_spec_is_rejected():
    component = {"id": "C1", "type": "Capacitor"}
    result = validate_component(component, measured_value=40)  # way under 100µF
    assert result.grade == "REJECT"
    assert result.passed is False


def test_validate_unknown_component_type_is_rejected():
    component = {"id": "X1", "type": "Mystery"}
    result = validate_component(component, measured_value=1)
    assert result.grade == "REJECT"
    assert "No test profile" in result.notes
