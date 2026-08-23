"""
app.py
------
ReCircuit backend API.

Exposes the recovery pipeline (scan -> decide -> validate -> inventory)
as a small Flask JSON API, so the logic in decision_engine.py and
vision_stub.py can be exercised over HTTP — e.g. from a future version
of the frontend, from Postman, or from other tools.

Run locally:
    pip install -r requirements.txt
    python app.py

Then visit http://localhost:5000/api/health
"""

from __future__ import annotations
from flask import Flask, jsonify, request
from flask_cors import CORS

from vision_stub import detect_components
from decision_engine import should_recover, validate_component
import database

app = Flask(__name__)
CORS(app)


@app.get("/api/health")
def health():
    return jsonify(status="ok", service="ReCircuit backend")


@app.post("/api/scan")
def scan():
    board_id = request.json.get("board_id", "PCB-001") if request.is_json else "PCB-001"
    components = detect_components(board_id)
    return jsonify(board_id=board_id, components=components)


@app.post("/api/decide")
def decide():
    component = request.get_json(force=True)
    decision = should_recover(component)
    return jsonify(decision.to_dict())


@app.post("/api/validate")
def validate():
    payload = request.get_json(force=True)
    component = payload.get("component", payload)
    measured_value = payload.get("measured_value")

    result = validate_component(component, measured_value)

    record = database.add_component(
        component_id=result.component_id,
        component_type=component.get("type", "Unknown"),
        measured_value=result.measured_value,
        status="PASS" if result.passed else "REJECT",
        grade=result.grade,
        source_board=component.get("board_id", "PCB-001"),
    )
    return jsonify({**result.to_dict(), "passport": record})


@app.get("/api/inventory")
def inventory():
    return jsonify(database.list_inventory())


@app.post("/api/inventory/reset")
def inventory_reset():
    database.reset()
    return jsonify(status="cleared")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
