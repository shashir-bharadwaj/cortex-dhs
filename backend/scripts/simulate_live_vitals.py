"""
State-based ICU vital simulator.

Design:
- Each bed maintains current vital values that drift gradually each tick.
- Most beds stay in normal ranges with small random perturbations.
- 2 beds are designated "critical" and drift into warning/critical zones.
- Alarms only fire when a value crosses a threshold AND a per-bed cooldown
  (5 minutes) has elapsed — preventing alarm spam.
- All bed measurements are batched into a single HTTP call per tick.
"""

import argparse
import random
import time
from datetime import datetime, timezone

import requests

# ---------------------------------------------------------------------------
# Vital metric definitions
# ---------------------------------------------------------------------------

# Drift magnitude per tick (maximum random step)
DRIFT = {
    "heart_rate": 2.5,
    "spo2": 0.4,
    "temperature": 0.12,
    "respiratory_rate": 1.2,
    "bp_systolic": 3.5,
    "bp_diastolic": 2.0,
}

# Clamp bounds for normal beds
NORMAL_BOUNDS = {
    "heart_rate":        (58,  100),
    "spo2":              (95,  100),
    "temperature":       (97.2, 99.8),
    "respiratory_rate":  (12,  20),
    "bp_systolic":       (90,  138),
    "bp_diastolic":      (60,  88),
}

# Starting baseline (center of normal range)
BASELINE = {
    "heart_rate": 76,
    "spo2": 97.5,
    "temperature": 98.6,
    "respiratory_rate": 15,
    "bp_systolic": 118,
    "bp_diastolic": 76,
}

# Clamp bounds for critical beds
CRITICAL_BOUNDS = {
    "heart_rate":        (108, 135),
    "spo2":              (85,  91),
    "temperature":       (101.0, 103.5),
    "respiratory_rate":  (24,  32),
    "bp_systolic":       (158, 185),
    "bp_diastolic":      (96,  112),
}

# Starting values for critical beds
CRITICAL_BASELINE = {
    "heart_rate": 118,
    "spo2": 88,
    "temperature": 102.2,
    "respiratory_rate": 27,
    "bp_systolic": 168,
    "bp_diastolic": 102,
}

# Alarm threshold checks — fire when True
ALARM_THRESHOLDS = {
    "heart_rate":       lambda v: v > 120 or v < 50,
    "spo2":             lambda v: v < 90,
    "temperature":      lambda v: v > 102.0 or v < 96.0,
    "respiratory_rate": lambda v: v > 25 or v < 10,
    "bp_systolic":      lambda v: v > 160 or v < 80,
}

ALARM_MESSAGES = {
    "heart_rate":       lambda v: f"HR {'tachycardia' if v > 120 else 'bradycardia'}: {v:.0f} bpm",
    "spo2":             lambda v: f"SpO2 critical low: {v:.1f}%",
    "temperature":      lambda v: f"Temp {'hyperthermia' if v > 102 else 'hypothermia'}: {v:.1f}°F",
    "respiratory_rate": lambda v: f"RR {'tachypnea' if v > 25 else 'bradypnea'}: {v:.0f}/min",
    "bp_systolic":      lambda v: f"BP {'hypertension' if v > 160 else 'hypotension'}: {v:.0f} mmHg",
}

ALARM_COOLDOWN_SECONDS = 300  # 5 minutes per bed


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def init_state(beds: list[str], critical_beds: set[str]) -> dict:
    state = {}
    for bed in beds:
        baseline = CRITICAL_BASELINE if bed in critical_beds else BASELINE
        noise_scale = 0.15
        state[bed] = {
            metric: round(baseline[metric] + random.uniform(
                -abs(baseline[metric]) * noise_scale,
                abs(baseline[metric]) * noise_scale,
            ), 1)
            for metric in DRIFT
        }
    return state


def drift_value(current: float, bounds: tuple[float, float], step: float) -> float:
    """Random walk clamped to bounds, with slight pull toward center."""
    lo, hi = bounds
    center = (lo + hi) / 2
    # Gentle pull toward center so values don't get stuck at extremes
    pull = (center - current) * 0.05
    delta = pull + random.uniform(-step, step)
    return round(max(lo, min(hi, current + delta)), 1)


def update_state(state: dict, critical_beds: set[str]) -> None:
    for bed, vitals in state.items():
        bounds_map = CRITICAL_BOUNDS if bed in critical_beds else NORMAL_BOUNDS
        for metric, step in DRIFT.items():
            vitals[metric] = drift_value(vitals[metric], bounds_map[metric], step)


# ---------------------------------------------------------------------------
# Event builders
# ---------------------------------------------------------------------------

def make_measurement(bed_id: str, metric_code: str, value: float) -> dict:
    return {
        "event_type": "measurement",
        "event_time": datetime.now(timezone.utc).isoformat(),
        "source": {
            "bed_id": bed_id,
            "device_id": f"SIM_{bed_id}",
            "device_type": "MONITOR",
        },
        "metric": {"code": metric_code, "value": value},
    }


def make_alarm(bed_id: str, message: str, severity: str = "critical") -> dict:
    return {
        "event_type": "alarm",
        "event_time": datetime.now(timezone.utc).isoformat(),
        "source": {
            "bed_id": bed_id,
            "device_id": f"SIM_{bed_id}",
            "device_type": "MONITOR",
        },
        "severity": severity,
        "message": message,
    }


def post_events(api_base_url: str, events: list[dict]) -> None:
    if not events:
        return
    try:
        response = requests.post(
            f"{api_base_url}/api/v1/ingestion/device-events",
            json={"events": events},
            timeout=10,
        )
        if response.status_code not in (200, 201):
            print(f"  [warn] ingestion {response.status_code}: {response.text[:120]}")
    except requests.RequestException as exc:
        print(f"  [error] could not reach backend: {exc}")


# ---------------------------------------------------------------------------
# Main simulation loop
# ---------------------------------------------------------------------------

def simulate(
    api_base_url: str,
    beds: list[str],
    interval_seconds: float,
    critical_count: int,
) -> None:
    # Designate the first N beds as critical (deterministic for reproducibility)
    critical_beds: set[str] = set(beds[:critical_count])
    print(f"Critical beds: {sorted(critical_beds)}")

    state = init_state(beds, critical_beds)
    # last_alarm[bed] = last epoch time an alarm was fired for that bed
    last_alarm: dict[str, float] = {}

    tick = 0
    while True:
        tick += 1
        now = time.time()

        # Drift all beds
        update_state(state, critical_beds)

        events: list[dict] = []

        for bed, vitals in state.items():
            for metric, value in vitals.items():
                events.append(make_measurement(bed, metric, value))

            # Check alarm thresholds (with cooldown)
            for metric, check in ALARM_THRESHOLDS.items():
                if check(vitals[metric]):
                    last = last_alarm.get(bed, 0)
                    if now - last >= ALARM_COOLDOWN_SECONDS:
                        msg = ALARM_MESSAGES[metric](vitals[metric])
                        events.append(make_alarm(bed, msg, "critical"))
                        last_alarm[bed] = now
                        print(f"  ⚠ ALARM  bed={bed}  {msg}")
                        break  # one alarm per bed per cycle

        post_events(api_base_url, events)

        critical_vals = {b: f"HR={state[b]['heart_rate']:.0f} SpO2={state[b]['spo2']:.1f}" for b in critical_beds}
        print(f"[tick {tick:>4}] posted {len(events)} events | critical beds: {critical_vals}")

        time.sleep(interval_seconds)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="State-based ICU vital simulator")

    parser.add_argument("--api-base-url", default="http://localhost:8000")
    parser.add_argument(
        "--beds",
        nargs="+",
        default=[
            "B1",  "B2",  "B3",  "B4",  "B5",
            "B6",  "B7",  "B8",  "B9",  "B10",
            "S1",  "S2",  "S3",  "S4",  "S5",
            "S6",  "S7",  "S8",
            "N1",  "N2",  "N3",  "N4",  "N5",
            "N6",  "N7",  "N8",
        ],
    )
    parser.add_argument("--interval", type=float, default=2.0,
                        help="Seconds between ticks")
    parser.add_argument("--critical-beds", type=int, default=2,
                        help="Number of beds to keep in critical state (default: 2)")

    args = parser.parse_args()

    simulate(
        api_base_url=args.api_base_url,
        beds=args.beds,
        interval_seconds=args.interval,
        critical_count=args.critical_beds,
    )
