import argparse
import random
import time
from datetime import datetime, timezone

import requests


METRICS = [
    ("heart_rate", 70, 140),
    ("spo2", 86, 100),
    ("temperature", 97.0, 103.0),
    ("respiratory_rate", 12, 32),
    ("bp_systolic", 100, 160),
    ("bp_diastolic", 60, 100),
]


def build_measurement_event(
    bed_id: str,
    metric_code: str,
    value: float,
) -> dict:
    return {
        "event_type": "measurement",
        "event_time": datetime.now(timezone.utc).isoformat(),
        "source": {
            "bed_id": bed_id,
            "device_id": f"SIM_MONITOR_{bed_id}",
            "device_type": "MONITOR",
        },
        "metric": {
            "code": metric_code,
            "value": value,
        },
    }


def build_alarm_event(
    bed_id: str,
    message: str,
    severity: str = "critical",
) -> dict:
    return {
        "event_type": "alarm",
        "event_time": datetime.now(timezone.utc).isoformat(),
        "source": {
            "bed_id": bed_id,
            "device_id": f"SIM_MONITOR_{bed_id}",
            "device_type": "MONITOR",
        },
        "severity": severity,
        "message": message,
    }


def post_event(
    api_base_url: str,
    event: dict,
) -> None:
    url = f"{api_base_url}/api/v1/ingestion/device-events"

    response = requests.post(
        url,
        json={"events": [event]},
        timeout=10,
    )

    print(
        response.status_code,
        response.json(),
    )


def simulate(
    api_base_url: str,
    beds: list[str],
    interval_seconds: float,
    alarm_probability: float,
) -> None:
    while True:
        bed_id = random.choice(beds)
        metric_code, min_value, max_value = random.choice(METRICS)

        value = round(
            random.uniform(min_value, max_value),
            1,
        )

        event = build_measurement_event(
            bed_id=bed_id,
            metric_code=metric_code,
            value=value,
        )

        print(
            f"Sending measurement: bed={bed_id}, metric={metric_code}, value={value}"
        )
        post_event(api_base_url, event)

        if random.random() < alarm_probability:
            alarm_event = build_alarm_event(
                bed_id=bed_id,
                message=f"Simulated alarm for {metric_code}: {value}",
                severity="critical",
            )

            print(
                f"Sending alarm: bed={bed_id}, message={alarm_event['message']}"
            )
            post_event(api_base_url, alarm_event)

        time.sleep(interval_seconds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulate live ICU vital events through ingestion API."
    )

    parser.add_argument(
        "--api-base-url",
        default="http://localhost:8000",
    )

    parser.add_argument(
        "--beds",
        nargs="+",
        default=["B1", "B2", "B3", "B4", "B5"],
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
    )

    parser.add_argument(
        "--alarm-probability",
        type=float,
        default=0.15,
    )

    args = parser.parse_args()

    simulate(
        api_base_url=args.api_base_url,
        beds=args.beds,
        interval_seconds=args.interval,
        alarm_probability=args.alarm_probability,
    )