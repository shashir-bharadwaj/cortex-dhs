from datetime import datetime, timedelta
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.providers.auth import AuthProvider
from app.api.schemas.admin_dashboard import AdminDashboardOverviewResponse
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.db.database import get_db
from app.domain.enums.permission import PermissionAction, PermissionModule
from app.infrastructure.database.models.alarm import AlarmModel
from app.infrastructure.database.models.bed import BedMasterModel
from app.infrastructure.database.models.device_master import DeviceMasterModel
from app.infrastructure.database.models.hospital import HospitalModel
from app.infrastructure.database.models.icu_unit_master import ICUUnitMasterModel
from app.infrastructure.database.models.patient import PatientModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/dashboard", tags=["Admin - Dashboard"])


def dashboard_permission(action: PermissionAction):
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.DASHBOARD,
            action,
        )
    )


def _build_connectivity_trend(connected: int, offline: int):
    labels = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "Now"]

    return [
        {
            "time": label,
            "online": max(0, int(connected * (0.9 + index * 0.02))),
            "offline": max(0, int(offline * (0.85 + index * 0.01))),
        }
        for index, label in enumerate(labels)
    ]


def _build_alerts_data(db: Session):
    now = datetime.utcnow()

    start_time = now - timedelta(hours=12)

    alarms = (
        db.query(AlarmModel)
        .filter(AlarmModel.timestamp >= start_time)
        .all()
    )

    windows = [
        (6, "6 AM"),
        (8, "8 AM"),
        (10, "10 AM"),
        (12, "12 PM"),
    ]

    result = []

    for hours, label in windows:
        cutoff = now - timedelta(hours=hours)

        filtered = [
            alarm for alarm in alarms
            if alarm.timestamp and alarm.timestamp >= cutoff
        ]

        critical = sum(
            1 for alarm in filtered
            if (alarm.severity or "").lower() == "critical"
        )

        warning = sum(
            1 for alarm in filtered
            if (alarm.severity or "").lower() == "warning"
        )

        info = sum(
            1 for alarm in filtered
            if (alarm.severity or "").lower() not in {"critical", "warning"}
        )

        result.append(
            {
                "time": label,
                "critical": critical,
                "warning": warning,
                "info": info,
            }
        )

    return result


@router.get(
    "/overview",
    response_model=AdminDashboardOverviewResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_admin_dashboard_overview(
    _current_user=dashboard_permission(PermissionAction.VIEW),
    db: Session = Depends(get_db),
):
    try:
        hospitals = db.query(HospitalModel).count()

        icu_units = db.query(ICUUnitMasterModel).count()

        beds = db.query(BedMasterModel).count()

        connected_devices = (
            db.query(DeviceMasterModel)
            .filter(DeviceMasterModel.status == "ONLINE")
            .count()
        )

        offline_devices = (
            db.query(DeviceMasterModel)
            .filter(DeviceMasterModel.status != "ONLINE")
            .count()
        )

        patients = (
            db.query(PatientModel)
            .filter(func.lower(PatientModel.status) != "discharged")
            .count()
        )

        critical_alarms = (
            db.query(AlarmModel)
            .filter(func.lower(AlarmModel.severity) == "critical")
            .count()
        )

        recent_alarms = (
            db.query(AlarmModel)
            .order_by(AlarmModel.timestamp.desc())
            .limit(5)
            .all()
        )

        live_alerts = [
            {
                "bed": alarm.bed_id if alarm.bed_id else "N/A",
                "type": (alarm.severity or "Alert").title(),
                "message": alarm.message or "",
                "time": alarm.timestamp.strftime("%I:%M %p")
                if alarm.timestamp
                else "Now",
            }
            for alarm in recent_alarms
        ]

        return {
            "stats": {
                "hospitals": hospitals,
                "icuUnits": icu_units,
                "beds": beds,
                "connected": connected_devices,
                "offline": offline_devices,
                "patients": patients,
                "critical": critical_alarms,
            },
            "connectivityTrend": _build_connectivity_trend(
                connected_devices,
                offline_devices,
            ),
            "alertsData": _build_alerts_data(db),
            "liveAlerts": live_alerts,
        }

    except Exception as ex:
        logger.exception("Error while fetching admin dashboard overview")
        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )