"""
decision_engine.py
-------------------
Rule-based recovery decision and functional grading logic for
ReCircuit.

This is the real, runnable counterpart to the logic simulated in the
frontend prototype (frontend/js/app.js). It is deliberately simple —
threshold-based rules — so it is transparent, testable, and easy to
swap for a trained ML classifier later without changing its public
interface.

Public functions:
    should_recover(component)   -> RecoveryDecision
    validate_component(component) -> ValidationResult
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Literal, Dict, Any

# --- Tunable thresholds -----------------------------------------------
# A component is a HIGH-value recovery candidate if the vision model is
# confident enough about what it is. Below this, we defer/skip rather
# than risk extracting a misidentified or damaged part.
CONFIDENCE_THRESHOLD = 0.90

# Component types considered "simple" enough to reliably extract with
# a basic robotic arm in this stage of the project. Complex packages
# (e.g. dense multi-pin ICs) are deferred to a later hardware revision.
SIMPLE_TYPES = {"Resistor", "Capacitor", "LED", "Diode", "Inductor"}

Grade = Literal["A", "B", "C", "REJECT"]


@dataclass
class RecoveryDecision:
    component_id: str
    recoverable: bool
    recoverability: Literal["HIGH", "LOW"]
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ValidationResult:
    component_id: str
    passed: bool
    grade: Grade
    measured_value: str
    notes: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def should_recover(component: Dict[str, Any]) -> RecoveryDecision:
    """Decide whether a detected component is worth recovering.

    `component` is expected to have at least:
        id: str
        type: str
        vision_confidence: float (0.0 - 1.0)
    """
    confidence = component.get("vision_confidence", 0.0)
    comp_type = component.get("type", "Unknown")
    comp_id = component.get("id", "UNKNOWN")

    if confidence < CONFIDENCE_THRESHOLD:
        return RecoveryDecision(
            component_id=comp_id,
            recoverable=False,
            recoverability="LOW",
            reason=f"Vision confidence {confidence:.0%} below "
                   f"{CONFIDENCE_THRESHOLD:.0%} threshold.",
        )

    if comp_type not in SIMPLE_TYPES:
        return RecoveryDecision(
            component_id=comp_id,
            recoverable=False,
            recoverability="LOW",
            reason=f"'{comp_type}' packages are not yet supported by "
                   f"the current extraction hardware.",
        )

    return RecoveryDecision(
        component_id=comp_id,
        recoverable=True,
        recoverability="HIGH",
        reason="High detection confidence and a supported package type.",
    )


# Simple simulated measurement tolerances by component type, used to
# decide a functional grade. In the real system these would come from
# the electrical test rig (backend/testing hardware), not be invented.
_EXPECTED = {
    "Resistor": {"nominal": 10_000, "unit": "Ω", "tolerance": 0.05},
    "Capacitor": {"nominal": 100, "unit": "µF", "tolerance": 0.10},
    "LED": {"nominal": 2.1, "unit": "V (forward drop)", "tolerance": 0.15},
}


def validate_component(component: Dict[str, Any], measured_value: float | None = None) -> ValidationResult:
    """Grade a recovered component based on how close its measured
    value is to the expected nominal value for its type.

    If `measured_value` is not supplied (e.g. no test rig connected
    yet), a value within tolerance is assumed so the pipeline can
    still be demonstrated end-to-end.
    """
    comp_type = component.get("type", "Unknown")
    comp_id = component.get("id", "UNKNOWN")
    spec = _EXPECTED.get(comp_type)

    if spec is None:
        return ValidationResult(
            component_id=comp_id,
            passed=False,
            grade="REJECT",
            measured_value="N/A",
            notes=f"No test profile defined for component type '{comp_type}'.",
        )

    if measured_value is None:
        measured_value = spec["nominal"]  # assume in-spec for demo purposes

    deviation = abs(measured_value - spec["nominal"]) / spec["nominal"]

    if deviation <= spec["tolerance"] * 0.5:
        grade: Grade = "A"
        passed = True
    elif deviation <= spec["tolerance"]:
        grade = "B"
        passed = True
    elif deviation <= spec["tolerance"] * 2:
        grade = "C"
        passed = True
    else:
        grade = "REJECT"
        passed = False

    return ValidationResult(
        component_id=comp_id,
        passed=passed,
        grade=grade,
        measured_value=f"{measured_value} {spec['unit']}",
        notes=f"Deviation from nominal: {deviation:.1%} "
              f"(tolerance: {spec['tolerance']:.0%}).",
    )
