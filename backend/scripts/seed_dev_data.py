"""
Dev-only seed script for Cortex ICU.

Seeds:
- permissions
- roles
- role-permission mappings
- hospital
- hospital units
- ICU units
- beds
- device masters
- users
- sample patients
- patient staff assignments
- sample vitals
- sample timeline events
- sample alarms
"""

import random
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.domain.enums.auth import ShiftType, UserRole
from app.domain.enums.patient import Gender
from app.domain.enums.permission import PermissionAction, PermissionModule
from app.domain.enums.timeline import TimelineEventType
from app.infrastructure.database.models.alarm import AlarmModel
from app.infrastructure.database.models.bed import BedMasterModel
from app.infrastructure.database.models.device_master import DeviceMasterModel
from app.infrastructure.database.models.hospital import HospitalModel
from app.infrastructure.database.models.hospital_unit import HospitalUnitModel
from app.infrastructure.database.models.icu_unit_master import ICUUnitMasterModel
from app.infrastructure.database.models.latest_vital import LatestVitalModel
from app.infrastructure.database.models.patient import PatientModel
from app.infrastructure.database.models.patient_staff_assignment import (
    PatientStaffAssignmentModel,
)
from app.infrastructure.database.models.permission import PermissionModel
from app.infrastructure.database.models.role import RoleModel
from app.infrastructure.database.models.role_permission import RolePermissionModel
from app.infrastructure.database.models.timeline import TimelineEventModel
from app.infrastructure.database.models.user import UserModel
from app.infrastructure.database.models.vital import VitalModel
from app.infrastructure.security.password_service import PasswordService


SEED_USERS = [
    {
        "user_id": "admin",
        "first_name": "System",
        "last_name": "Admin",
        "email": "admin@cortex.com",
        "password": "admin",
        "role": UserRole.ADMIN,
        "shift": ShiftType.MORNING,
    },
    {
        "user_id": "doctor",
        "first_name": "John",
        "last_name": "Doctor",
        "email": "doctor@cortex.com",
        "password": "doctor",
        "role": UserRole.DOCTOR,
        "shift": ShiftType.MORNING,
    },
    {
        "user_id": "nurse",
        "first_name": "Jane",
        "last_name": "Nurse",
        "email": "nurse@cortex.com",
        "password": "nurse",
        "role": UserRole.NURSE,
        "shift": ShiftType.MORNING,
    },
]

HOSPITAL_NAME = "Apollo Main Hospital"
HOSPITAL_CODE = "APOLLO-BLR-001"

UNIT_NAMES = ["MICU", "SICU", "NICU"]
SEED_ICU_NAMES = ["MICU-1", "SICU-1", "NICU-1"]
SEED_BED_IDS = ["B1", "B2", "B3"]

SEED_PATIENT_NAMES = [
    "Rahul Sharma",
    "Ananya Rao",
    "Vikram Mehta",
]

SEED_DEVICE_SERIALS = [
    "MONITOR-SEED-001",
    "VENT-SEED-001",
    "PUMP-SEED-001",
]

PERMISSION_MODULES = [
    PermissionModule.HOSPITALS,
    PermissionModule.PATIENTS,
    PermissionModule.VITALS,
    PermissionModule.TIMELINE,
    PermissionModule.ALARMS,
    PermissionModule.ICU_MANAGEMENT,
    PermissionModule.BED_MANAGEMENT,
    PermissionModule.DEVICE_MANAGEMENT,
    PermissionModule.MANAGE_USERS,
    PermissionModule.DASHBOARD,
]

PERMISSION_ACTIONS = [
    PermissionAction.VIEW,
    PermissionAction.CREATE,
    PermissionAction.MODIFY,
    PermissionAction.CANCEL,
    PermissionAction.DELETE,
]

password_service = PasswordService()


def utc_now() -> datetime:
    """
    Return timezone-aware UTC datetime.
    """
    return datetime.now(UTC)


def clear_seed_data(db: Session) -> None:
    """
    Clear known dev seed records in dependency-safe order.
    """
    seed_patients = (
        db.query(PatientModel)
        .filter(PatientModel.name.in_(SEED_PATIENT_NAMES))
        .all()
    )
    seed_patient_ids = [patient.id for patient in seed_patients]

    if seed_patient_ids:
        db.query(PatientStaffAssignmentModel).filter(
            PatientStaffAssignmentModel.patient_id.in_(seed_patient_ids)
        ).delete(synchronize_session=False)

        db.query(AlarmModel).filter(
            AlarmModel.patient_id.in_(seed_patient_ids)
        ).delete(synchronize_session=False)

        db.query(LatestVitalModel).filter(
            LatestVitalModel.patient_id.in_(seed_patient_ids)
        ).delete(synchronize_session=False)

        db.query(VitalModel).filter(
            VitalModel.patient_id.in_(seed_patient_ids)
        ).delete(synchronize_session=False)

        db.query(TimelineEventModel).filter(
            TimelineEventModel.patient_id.in_(seed_patient_ids)
        ).delete(synchronize_session=False)

        db.query(PatientModel).filter(
            PatientModel.id.in_(seed_patient_ids)
        ).delete(synchronize_session=False)

    db.query(DeviceMasterModel).filter(
        DeviceMasterModel.serial.in_(SEED_DEVICE_SERIALS)
    ).delete(synchronize_session=False)

    db.query(BedMasterModel).filter(
        BedMasterModel.bed_id.in_(SEED_BED_IDS)
    ).delete(synchronize_session=False)

    db.query(ICUUnitMasterModel).filter(
        ICUUnitMasterModel.icu_name.in_(SEED_ICU_NAMES)
    ).delete(synchronize_session=False)

    db.query(UserModel).filter(
        UserModel.user_id.in_([user["user_id"] for user in SEED_USERS])
    ).delete(synchronize_session=False)

    db.query(RolePermissionModel).delete(synchronize_session=False)
    db.query(PermissionModel).delete(synchronize_session=False)

    db.query(RoleModel).filter(
        RoleModel.name.in_([role.value for role in UserRole])
    ).delete(synchronize_session=False)

    hospital = (
        db.query(HospitalModel)
        .filter(HospitalModel.code == HOSPITAL_CODE)
        .first()
    )

    if hospital:
        db.query(HospitalUnitModel).filter(
            HospitalUnitModel.hospital_id == hospital.id
        ).delete(synchronize_session=False)

        db.query(HospitalModel).filter(
            HospitalModel.id == hospital.id
        ).delete(synchronize_session=False)

    db.commit()


def seed_permissions(db: Session) -> list[PermissionModel]:
    """
    Seed RBAC permissions.
    """
    permissions: list[PermissionModel] = []

    for module in PERMISSION_MODULES:
        for action in PERMISSION_ACTIONS:
            permission = PermissionModel(
                module=module.value,
                action=action.value,
            )
            db.add(permission)
            db.flush()
            permissions.append(permission)

    return permissions


def seed_roles(db: Session) -> dict[str, RoleModel]:
    """
    Seed roles matching UserRole enum values.
    """
    roles: dict[str, RoleModel] = {}

    for role in UserRole:
        role_model = RoleModel(
            name=role.value,
            description=f"{role.value.title()} role",
        )
        db.add(role_model)
        db.flush()
        roles[role.value] = role_model

    return roles


def seed_role_permissions(
    db: Session,
    roles: dict[str, RoleModel],
    permissions: list[PermissionModel],
) -> None:
    """
    Seed role-permission mappings.
    """
    permission_map = {
        (permission.module, permission.action): permission
        for permission in permissions
    }

    def permissions_for(
        module: PermissionModule,
        actions: list[PermissionAction],
    ) -> list[PermissionModel]:
        return [
            permission_map[(module.value, action.value)]
            for action in actions
        ]

    admin_permissions = permissions

    doctor_permissions: list[PermissionModel] = []
    doctor_permissions += permissions_for(
        PermissionModule.PATIENTS,
        [
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.MODIFY,
        ],
    )
    doctor_permissions += permissions_for(
        PermissionModule.VITALS,
        [
            PermissionAction.VIEW,
            PermissionAction.CREATE,
        ],
    )
    doctor_permissions += permissions_for(
        PermissionModule.TIMELINE,
        [
            PermissionAction.VIEW,
            PermissionAction.CREATE,
        ],
    )
    doctor_permissions += permissions_for(
        PermissionModule.ALARMS,
        [
            PermissionAction.VIEW,
            PermissionAction.MODIFY,
        ],
    )
    doctor_permissions += permissions_for(
        PermissionModule.DASHBOARD,
        [PermissionAction.VIEW],
    )

    nurse_permissions: list[PermissionModel] = []
    nurse_permissions += permissions_for(
        PermissionModule.PATIENTS,
        [PermissionAction.VIEW],
    )
    nurse_permissions += permissions_for(
        PermissionModule.VITALS,
        [
            PermissionAction.VIEW,
            PermissionAction.CREATE,
        ],
    )
    nurse_permissions += permissions_for(
        PermissionModule.TIMELINE,
        [
            PermissionAction.VIEW,
            PermissionAction.CREATE,
        ],
    )
    nurse_permissions += permissions_for(
        PermissionModule.ALARMS,
        [
            PermissionAction.VIEW,
            PermissionAction.MODIFY,
        ],
    )
    nurse_permissions += permissions_for(
        PermissionModule.DASHBOARD,
        [PermissionAction.VIEW],
    )

    role_permission_map = {
        UserRole.ADMIN.value: admin_permissions,
        UserRole.DOCTOR.value: doctor_permissions,
        UserRole.NURSE.value: nurse_permissions,
    }

    for role_name, mapped_permissions in role_permission_map.items():
        role = roles[role_name]

        for permission in mapped_permissions:
            db.add(
                RolePermissionModel(
                    role_id=role.id,
                    permission_id=permission.id,
                )
            )


def seed_hospital_and_units(
    db: Session,
) -> tuple[HospitalModel, list[HospitalUnitModel]]:
    """
    Seed one hospital and hospital units.
    """
    hospital = HospitalModel(
        name=HOSPITAL_NAME,
        code=HOSPITAL_CODE,
        address="Bengaluru",
        city="Bengaluru",
        state="Karnataka",
        country="India",
        contact_number="9999999999",
        email="admin@apollo.example",
    )

    db.add(hospital)
    db.flush()

    units: list[HospitalUnitModel] = []

    for unit_name in UNIT_NAMES:
        unit = HospitalUnitModel(
            hospital_id=hospital.id,
            name=unit_name,
            code=f"{HOSPITAL_CODE}-{unit_name}",
            is_active=True,
        )
        db.add(unit)
        db.flush()
        units.append(unit)

    return hospital, units


def seed_icu_units(db: Session) -> list[ICUUnitMasterModel]:
    """
    Seed ICU unit master records.
    """
    payloads = [
        {
            "icu_name": "MICU-1",
            "type": "Medical ICU",
            "department": "Critical Care",
            "beds": 10,
            "devices": 20,
            "gateway": "GW-MICU-001",
            "status": "ACTIVE",
        },
        {
            "icu_name": "SICU-1",
            "type": "Surgical ICU",
            "department": "Surgery",
            "beds": 8,
            "devices": 16,
            "gateway": "GW-SICU-001",
            "status": "ACTIVE",
        },
        {
            "icu_name": "NICU-1",
            "type": "Neonatal ICU",
            "department": "Neonatology",
            "beds": 6,
            "devices": 12,
            "gateway": "GW-NICU-001",
            "status": "ACTIVE",
        },
    ]

    icu_units: list[ICUUnitMasterModel] = []

    for payload in payloads:
        icu_unit = ICUUnitMasterModel(**payload)
        db.add(icu_unit)
        db.flush()
        icu_units.append(icu_unit)

    return icu_units


def seed_beds(
    db: Session,
    icu_units: list[ICUUnitMasterModel],
) -> list[BedMasterModel]:
    """
    Seed bed master records mapped to ICU units.
    """
    payloads = [
        {
            "bed_id": "B1",
            "icu_unit_id": icu_units[0].id,
            "bed_type": "ICU",
            "department": "Critical Care",
            "ward": "MICU",
            "floor": "1",
            "room": "101",
            "cleaning_status": "CLEAN",
            "maintenance_status": "OK",
            "operational_status": "AVAILABLE",
            "last_sanitized": utc_now(),
        },
        {
            "bed_id": "B2",
            "icu_unit_id": icu_units[0].id,
            "bed_type": "ICU",
            "department": "Critical Care",
            "ward": "MICU",
            "floor": "1",
            "room": "102",
            "cleaning_status": "CLEAN",
            "maintenance_status": "OK",
            "operational_status": "AVAILABLE",
            "last_sanitized": utc_now(),
        },
        {
            "bed_id": "B3",
            "icu_unit_id": icu_units[1].id,
            "bed_type": "ICU",
            "department": "Surgery",
            "ward": "SICU",
            "floor": "2",
            "room": "201",
            "cleaning_status": "CLEAN",
            "maintenance_status": "OK",
            "operational_status": "AVAILABLE",
            "last_sanitized": utc_now(),
        },
    ]

    beds: list[BedMasterModel] = []

    for payload in payloads:
        bed = BedMasterModel(**payload)
        db.add(bed)
        db.flush()
        beds.append(bed)

    return beds


def seed_device_masters(
    db: Session,
    beds: list[BedMasterModel],
) -> list[DeviceMasterModel]:
    """
    Seed device master records mapped to beds.
    """
    payloads = [
        {
            "device_type": "MONITOR",
            "manufacturer": "Generic",
            "model": "Bedside Monitor",
            "serial": "MONITOR-SEED-001",
            "bed_id": beds[0].id,
            "ip_address": "192.168.1.101",
            "status": "ONLINE",
        },
        {
            "device_type": "VENTILATOR",
            "manufacturer": "Generic",
            "model": "Ventilator",
            "serial": "VENT-SEED-001",
            "bed_id": beds[1].id,
            "ip_address": "192.168.1.102",
            "status": "ONLINE",
        },
        {
            "device_type": "INFUSION_PUMP",
            "manufacturer": "Generic",
            "model": "Infusion Pump",
            "serial": "PUMP-SEED-001",
            "bed_id": beds[2].id,
            "ip_address": "192.168.1.103",
            "status": "OFFLINE",
        },
    ]

    devices: list[DeviceMasterModel] = []

    for payload in payloads:
        device = DeviceMasterModel(**payload)
        db.add(device)
        db.flush()
        devices.append(device)

    return devices


def seed_users(
    db: Session,
    roles: dict[str, RoleModel],
    hospital: HospitalModel,
    unit: HospitalUnitModel,
) -> list[UserModel]:
    """
    Seed default dev users.
    """
    users: list[UserModel] = []

    for user_data in SEED_USERS:
        user = UserModel(
            user_id=user_data["user_id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password_hash=password_service.hash_password(
                user_data["password"]
            ),
            role_id=roles[user_data["role"].value].id,
            hospital_id=hospital.id,
            unit_id=unit.id,
            shift=user_data["shift"].value,
            is_active=True,
        )

        db.add(user)
        db.flush()
        users.append(user)

    return users


def seed_patients(
    db: Session,
    hospital: HospitalModel,
    beds: list[BedMasterModel],
) -> list[PatientModel]:
    """
    Seed sample ICU patients assigned to bed master records.
    """
    patient_payloads = [
        {
            "name": "Rahul Sharma",
            "age": 45,
            "gender": Gender.MALE,
            "bed_id": beds[0].id,
            "diagnosis": "Pneumonia",
            "weight": 72.5,
            "height": 171.0,
            "blood_group": "O+",
            "doctor": "Dr. Meera Nair",
            "history": ["Admitted with respiratory distress"],
            "comorbidities": ["Hypertension"],
        },
        {
            "name": "Ananya Rao",
            "age": 52,
            "gender": Gender.FEMALE,
            "bed_id": beds[1].id,
            "diagnosis": "Sepsis",
            "weight": 64.0,
            "height": 164.0,
            "blood_group": "A+",
            "doctor": "Dr. Arjun Menon",
            "history": ["Transferred from emergency ward"],
            "comorbidities": ["Diabetes"],
        },
        {
            "name": "Vikram Mehta",
            "age": 61,
            "gender": Gender.MALE,
            "bed_id": beds[2].id,
            "diagnosis": "Post cardiac arrest monitoring",
            "weight": 78.0,
            "height": 176.0,
            "blood_group": "B+",
            "doctor": "Dr. Kavita Rao",
            "history": ["Post CPR observation"],
            "comorbidities": ["Coronary artery disease"],
        },
    ]

    patients: list[PatientModel] = []

    for payload in patient_payloads:
        patient = PatientModel(
            name=payload["name"],
            age=payload["age"],
            gender=payload["gender"],
            bed_id=payload["bed_id"],
            diagnosis=payload["diagnosis"],
            weight=payload["weight"],
            height=payload["height"],
            blood_group=payload["blood_group"],
            doctor=payload["doctor"],
            admission_time=utc_now(),
            hospital_id=hospital.id,
            status="admitted",
            history=payload["history"],
            comorbidities=payload["comorbidities"],
        )

        db.add(patient)
        db.flush()
        patients.append(patient)

    return patients


def seed_patient_staff_assignments(
    db: Session,
    patients: list[PatientModel],
    users: list[UserModel],
) -> None:
    """
    Seed active doctor and nurse assignments for each patient.
    """
    doctor = next(
        user
        for user in users
        if user.user_id == "doctor"
    )

    nurse = next(
        user
        for user in users
        if user.user_id == "nurse"
    )

    for patient in patients:
        db.add(
            PatientStaffAssignmentModel(
                patient_id=patient.id,
                user_id=doctor.id,
                assignment_type="DOCTOR",
                assigned_at=utc_now(),
                ended_at=None,
                is_active=True,
            )
        )

        db.add(
            PatientStaffAssignmentModel(
                patient_id=patient.id,
                user_id=nurse.id,
                assignment_type="NURSE",
                assigned_at=utc_now(),
                ended_at=None,
                is_active=True,
            )
        )


def seed_vitals(
    db: Session,
    patients: list[PatientModel],
) -> None:
    """
    Seed sample vitals and latest vital snapshot for each patient.
    """
    for patient in patients:
        for index in range(5):
            db.add(
                VitalModel(
                    patient_id=patient.id,
                    hr=random.randint(70, 115),
                    bp_sys=random.randint(105, 145),
                    bp_dia=random.randint(65, 95),
                    spo2=random.randint(92, 100),
                    temp=round(random.uniform(97.0, 100.5), 1),
                    rr=random.randint(14, 26),
                    recorded_at=utc_now() - timedelta(minutes=index * 15),
                )
            )

        db.add(
            LatestVitalModel(
                patient_id=patient.id,
                bed_id=patient.bed_id,
                device_id=None,
                hr=random.randint(70, 115),
                bp_sys=random.randint(105, 145),
                bp_dia=random.randint(65, 95),
                spo2=random.randint(92, 100),
                temp=round(random.uniform(97.0, 100.5), 1),
                rr=random.randint(14, 26),
                status="LIVE",
                recorded_at=utc_now(),
                updated_at=utc_now(),
            )
        )


def seed_timeline(
    db: Session,
    patients: list[PatientModel],
) -> None:
    """
    Seed sample timeline events.
    """
    for patient in patients:
        db.add(
            TimelineEventModel(
                patient_id=patient.id,
                type=TimelineEventType.NOTE_ADDED.value,
                event=f"Initial ICU assessment completed for {patient.name}",
                created_at=utc_now(),
            )
        )


def seed_alarms(
    db: Session,
    patients: list[PatientModel],
    beds: list[BedMasterModel],
    devices: list[DeviceMasterModel],
) -> None:
    """
    Seed sample ICU alarms.
    """
    alarm_payloads = [
        {
            "patient": patients[0],
            "bed": beds[0],
            "device": devices[0],
            "message": "SpO2 within safe threshold.",
            "severity": "Info",
            "acknowledged": False,
            "silenced": False,
            "escalated": False,
        },
        {
            "patient": patients[1],
            "bed": beds[1],
            "device": devices[1],
            "message": "Possible sepsis deterioration alert.",
            "severity": "Critical",
            "acknowledged": False,
            "silenced": False,
            "escalated": True,
            "escalate_to": "doctor",
            "escalated_by": "system",
        },
        {
            "patient": patients[2],
            "bed": beds[2],
            "device": devices[2],
            "message": "Heart rate above expected monitoring range.",
            "severity": "Warning",
            "acknowledged": True,
            "silenced": False,
            "escalated": False,
            "acknowledged_by": "nurse",
        },
    ]

    for payload in alarm_payloads:
        patient = payload["patient"]
        bed = payload["bed"]
        device = payload["device"]

        db.add(
            AlarmModel(
                timestamp=utc_now(),
                patient_id=patient.id,
                patient_name=patient.name,
                bed_id=bed.bed_id,
                device=device.model,
                message=payload["message"],
                severity=payload["severity"],
                acknowledged=payload["acknowledged"],
                silenced=payload["silenced"],
                escalated=payload["escalated"],
                acknowledged_by=payload.get("acknowledged_by"),
                silenced_by=payload.get("silenced_by"),
                silence_until=payload.get("silence_until"),
                escalated_by=payload.get("escalated_by"),
                escalate_to=payload.get("escalate_to"),
            )
        )


def main() -> None:
    """
    Run full dev seed process.
    """
    db = SessionLocal()

    try:
        print("Clearing existing dev seed data...")
        clear_seed_data(db)

        print("Creating permissions...")
        permissions = seed_permissions(db)

        print("Creating roles...")
        roles = seed_roles(db)

        print("Assigning role permissions...")
        seed_role_permissions(
            db=db,
            roles=roles,
            permissions=permissions,
        )

        print("Creating hospital and units...")
        hospital, units = seed_hospital_and_units(db)

        print("Creating ICU units...")
        icu_units = seed_icu_units(db)

        print("Creating beds...")
        beds = seed_beds(
            db=db,
            icu_units=icu_units,
        )

        print("Creating device masters...")
        devices = seed_device_masters(
            db=db,
            beds=beds,
        )

        print("Creating users...")
        users = seed_users(
            db=db,
            roles=roles,
            hospital=hospital,
            unit=units[0],
        )

        print("Creating patients...")
        patients = seed_patients(
            db=db,
            hospital=hospital,
            beds=beds,
        )

        print("Creating staff assignments...")
        seed_patient_staff_assignments(
            db=db,
            patients=patients,
            users=users,
        )

        print("Creating vitals...")
        seed_vitals(
            db=db,
            patients=patients,
        )

        print("Creating timeline events...")
        seed_timeline(
            db=db,
            patients=patients,
        )

        print("Creating alarms...")
        seed_alarms(
            db=db,
            patients=patients,
            beds=beds,
            devices=devices,
        )

        db.commit()

        print("Seeding complete.")
        print("Dev login users:")

        for user in SEED_USERS:
            print(
                f"- {user['email']} / "
                f"{user['password']} / "
                f"{user['role'].value}"
            )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()