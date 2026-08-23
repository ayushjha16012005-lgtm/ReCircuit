/**
 * ReCircuit — Virtual Prototype Logic
 *
 * This is a client-side simulation of the ReCircuit recovery pipeline:
 * Scan -> Identify -> Decide -> Recover -> Validate -> Passport -> Inventory
 *
 * All confidence scores, measurements, and pass/fail results here are
 * DEMONSTRATION DATA, not physical sensor or lab readings. The equivalent
 * decision-making logic (thresholds, grading rules) is implemented for
 * real in `backend/decision_engine.py`, so the same rules can later be
 * driven by an actual computer-vision + electrical-testing pipeline.
 */

let scanned = 0;
let validated = 0;
let selected = null;
let recovered = false;

function flow(n) {
  for (let i = 1; i <= 6; i++) {
    document.getElementById('f' + i).classList.toggle('on', i === n);
  }
}

function log(t) {
  const x = document.getElementById('log');
  x.innerHTML += '&gt; ' + t + '<br>';
  x.scrollTop = x.scrollHeight;
}

function scan() {
  scanned++;
  m1.textContent = scanned;
  scanline.style.display = 'block';
  log('Initializing PCB vision scan...');
  setTimeout(() => {
    scanline.style.display = 'none';
    m2.textContent = 4;
    m3.textContent = 3;
    flow(2);
    status.innerHTML =
      '<b>Scan complete ✓</b><br>4 components detected. Select a candidate for analysis.';
    log('Detected R1, C1, D1 and U1.');
  }, 1500);
}

function pick(el, id, type, value, confidence, recoverability) {
  if (!scanned) {
    status.textContent = 'Start scanning first.';
    return;
  }
  document.querySelectorAll('.part').forEach((x) => x.classList.remove('sel'));
  el.classList.add('sel');
  selected = { id, type, value, confidence, recoverability };
  recovered = false;
  flow(3);
  analysis.innerHTML =
    '<b>' + id + ' — ' + type + '</b>' +
    '<div class="row"><span>Expected value</span><b>' + value + '</b></div>' +
    '<div class="row"><span>Vision confidence</span><b>' + confidence + '</b></div>' +
    '<div class="row"><span>Recoverability</span><b>' + recoverability + '</b></div>';
  conf.textContent = confidence;
  recov.textContent = recoverability;
  decision.textContent = 'Pending evaluation';
  log('Selected ' + id + ' for recovery analysis.');
}

function decide() {
  if (!selected) return;
  flow(3);
  const yes = selected.recoverability === 'HIGH';
  decision.innerHTML = yes
    ? '<span class="green">RECOVER ✓</span>'
    : '<span class="yellow">SKIP / DEFER</span>';
  status.innerHTML = yes
    ? '<b>Recovery candidate confirmed ✓</b><br>High simulated recoverability.'
    : '<b>Recovery deferred</b><br>Complex/low-recoverability candidate.';
  log('Decision engine → ' + (yes ? 'RECOVER' : 'SKIP') + ' ' + selected.id);
}

function recover() {
  if (!selected || selected.recoverability !== 'HIGH') return;
  flow(4);
  recovered = true;
  bar.style.width = '100%';
  status.innerHTML =
    '<b>Selective extraction simulated ✓</b><br>' +
    selected.id + ' transferred to validation station.';
  log('Positioning extraction tool → ' + selected.id);
  log('Transfer complete → test station.');
}

function validate() {
  if (!selected || !recovered) {
    status.textContent = 'Evaluate a recoverable component and simulate extraction first.';
    return;
  }
  validated++;
  m4.textContent = validated;
  flow(5);
  const measured =
    selected.type === 'Resistor'
      ? '9.96 kΩ'
      : selected.type === 'Capacitor'
      ? '98.7 µF'
      : 'Forward drop: 2.1 V';
  passport.innerHTML =
    '<h3>RC-' + String(validated).padStart(3, '0') + '</h3>' +
    '<div class="row"><span>Component</span><b>' + selected.type + '</b></div>' +
    '<div class="row"><span>Source</span><b>PCB-001 / ' + selected.id + '</b></div>' +
    '<div class="row"><span>Measured</span><b>' + measured + '</b></div>' +
    '<div class="row"><span>Functional status</span><b class="green">PASS ✓</b></div>' +
    '<div class="row"><span>Reuse grade</span><b class="green">A</b></div>';
  status.innerHTML = '<b>Functional validation complete ✓</b><br>Simulated result: PASS';
  flow(6);
  if (inv.children.length === 1 && inv.children[0].children.length === 1) {
    inv.innerHTML = '';
  }
  const tr = document.createElement('tr');
  tr.innerHTML =
    '<td>RC-' + String(validated).padStart(3, '0') + '</td>' +
    '<td>' + selected.type + '</td>' +
    '<td>' + measured + '</td>' +
    '<td class="green">PASS</td>' +
    '<td>A</td>' +
    '<td>PCB-001</td>';
  inv.appendChild(tr);
  log('Digital passport created.');
}
