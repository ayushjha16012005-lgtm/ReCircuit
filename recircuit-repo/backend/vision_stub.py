"""
vision_stub.py
---------------
Placeholder for the real computer-vision component-detection stage.

In the full ReCircuit system this module would wrap an OpenCV /
ML-based object detector trained on PCB component images, and return
bounding boxes + classifications for every part found on a scanned
board.

For this student prototype, `detect_components()` returns a fixed,
labeled set of components so the rest of the pipeline (decision
engine, extraction, validation, inventory) can be built and tested
end-to-end without physical hardware.

Swap this module out for a real detector later without changing any
other part of the backend — every other module only depends on the
dict shape returned here.
"""

from __future__ import annotations
from typing import TypedDict, List


class DetectedComponent(TypedDict):
    id: str
    type: str
    expected_value: str
    vision_confidence: float  # 0.0 - 1.0
    board_id: str


def detect_components(board_id: str = "PCB-001") -> List[DetectedComponent]:
    """Simulate scanning a discarded PCB and detecting components.

    Returns a list of detected components with a vision-model
    confidence score. Replace this with a real OpenCV/ML pipeline
    (e.g. a YOLO/SSD model fine-tuned on PCB component datasets) when
    hardware is available.
    """
    return [
        {
            "id": "R1",
            "type": "Resistor",
            "expected_value": "10 kΩ",
            "vision_confidence": 0.96,
            "board_id": board_id,
        },
        {
            "id": "C1",
            "type": "Capacitor",
            "expected_value": "100 µF",
            "vision_confidence": 0.93,
            "board_id": board_id,
        },
        {
            "id": "D1",
            "type": "LED",
            "expected_value": "Green LED",
            "vision_confidence": 0.98,
            "board_id": board_id,
        },
        {
            "id": "U1",
            "type": "IC",
            "expected_value": "Complex IC",
            "vision_confidence": 0.89,
            "board_id": board_id,
        },
    ]
