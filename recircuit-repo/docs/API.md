# Backend API Reference

Base URL (local development): `http://localhost:5000`

All request/response bodies are JSON.

---

### `GET /api/health`

Health check.

**Response**
```json
{ "status": "ok", "service": "ReCircuit backend" }
```

---

### `POST /api/scan`

Simulates scanning a discarded PCB and returns detected components.

**Request body**
```json
{ "board_id": "PCB-001" }
```
`board_id` is optional; defaults to `"PCB-001"`.

**Response**
```json
{
  "board_id": "PCB-001",
  "components": [
    {
      "id": "R1",
      "type": "Resistor",
      "expected_value": "10 kΩ",
      "vision_confidence": 0.96,
      "board_id": "PCB-001"
    }
  ]
}
```

---

### `POST /api/decide`

Runs the recovery decision engine on a single component.

**Request body**
```json
{ "id": "R1", "type": "Resistor", "vision_confidence": 0.96 }
```

**Response**
```json
{
  "component_id": "R1",
  "recoverable": true,
  "recoverability": "HIGH",
  "reason": "High detection confidence and a supported package type."
}
```

---

### `POST /api/validate`

Runs functional grading on a recovered component and stores the result in
the inventory (SQLite).

**Request body**
```json
{
  "component": { "id": "R1", "type": "Resistor", "board_id": "PCB-001" },
  "measured_value": 10000
}
```
`measured_value` is optional — if omitted, the nominal value is assumed
(useful for demoing without a connected test rig).

**Response**
```json
{
  "component_id": "R1",
  "passed": true,
  "grade": "A",
  "measured_value": "10000 Ω",
  "notes": "Deviation from nominal: 0.0% (tolerance: 5%).",
  "passport": {
    "passport_id": "RC-001",
    "component_id": "R1",
    "component_type": "Resistor",
    "measured_value": "10000 Ω",
    "status": "PASS",
    "grade": "A",
    "source_board": "PCB-001"
  }
}
```

---

### `GET /api/inventory`

Returns every validated component currently on record, most recent first.

**Response**
```json
[
  {
    "passport_id": "RC-001",
    "component_id": "R1",
    "component_type": "Resistor",
    "measured_value": "10000 Ω",
    "status": "PASS",
    "grade": "A",
    "source_board": "PCB-001",
    "created_at": "2026-08-23 12:00:00"
  }
]
```

---

### `POST /api/inventory/reset`

Clears the inventory table. Intended for demos/testing only.

**Response**
```json
{ "status": "cleared" }
```
