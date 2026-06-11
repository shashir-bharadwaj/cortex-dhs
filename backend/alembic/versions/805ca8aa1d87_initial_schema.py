"""initial schema

Revision ID: 805ca8aa1d87
Revises:
Create Date: 2026-04-15 18:17:29.249491
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "805ca8aa1d87"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # -------------------------------------------------------------------------
    # Device Type / Runtime Device Tables
    # -------------------------------------------------------------------------

    op.create_table(
        "device_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("company", sa.String(), nullable=True),
        sa.Column("output_spec", sa.String(), nullable=True),
        sa.Column("adapter_name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_device_types_id"), "device_types", ["id"], unique=False)

    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("serial_number", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("last_sync", sa.DateTime(), nullable=True),
        sa.Column("error", sa.String(), nullable=True),
        sa.Column("location", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_devices_id"), "devices", ["id"], unique=False)
    op.create_index(
        op.f("ix_devices_serial_number"),
        "devices",
        ["serial_number"],
        unique=True,
    )

    # -------------------------------------------------------------------------
    # Hospital Tables
    # -------------------------------------------------------------------------

    op.create_table(
        "hospitals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=True),
        sa.Column("address", sa.String(length=500), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("contact_number", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_hospitals_id"), "hospitals", ["id"], unique=False)

    op.create_table(
        "hospital_units",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hospital_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["hospital_id"], ["hospitals.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "hospital_id",
            "name",
            name="uq_hospital_units_hospital_id_name",
        ),
    )
    op.create_index(
        op.f("ix_hospital_units_hospital_id"),
        "hospital_units",
        ["hospital_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_hospital_units_id"),
        "hospital_units",
        ["id"],
        unique=False,
    )

    # -------------------------------------------------------------------------
    # Admin Master Tables
    # -------------------------------------------------------------------------

    op.create_table(
        "icu_unit_masters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("icu_name", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("department", sa.String(), nullable=False),
        sa.Column("beds", sa.Integer(), nullable=False),
        sa.Column("devices", sa.String(), nullable=True),
        sa.Column("gateway", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_icu_unit_masters_id"),
        "icu_unit_masters",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_icu_unit_masters_icu_name"),
        "icu_unit_masters",
        ["icu_name"],
        unique=True,
    )

    op.create_table(
        "bed_masters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("bed_id", sa.String(), nullable=False),
        sa.Column("icu_unit_id", sa.Integer(), nullable=False),
        sa.Column("bed_type", sa.String(), nullable=False),
        sa.Column("department", sa.String(), nullable=False),
        sa.Column("ward", sa.String(), nullable=False),
        sa.Column("floor", sa.String(), nullable=False),
        sa.Column("room", sa.String(), nullable=False),
        sa.Column("cleaning_status", sa.String(), nullable=False),
        sa.Column("maintenance_status", sa.String(), nullable=False),
        sa.Column("operational_status", sa.String(), nullable=False),
        sa.Column("last_sanitized", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["icu_unit_id"], ["icu_unit_masters.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_bed_masters_id"), "bed_masters", ["id"], unique=False)
    op.create_index(
        op.f("ix_bed_masters_bed_id"),
        "bed_masters",
        ["bed_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_bed_masters_icu_unit_id"),
        "bed_masters",
        ["icu_unit_id"],
        unique=False,
    )

    op.create_table(
        "device_masters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("device_type", sa.String(), nullable=False),
        sa.Column("manufacturer", sa.String(), nullable=False),
        sa.Column("model", sa.String(), nullable=False),
        sa.Column("serial", sa.String(), nullable=False),
        sa.Column("bed_id", sa.Integer(), nullable=True),
        sa.Column("ip_address", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["bed_id"], ["bed_masters.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_device_masters_id"), "device_masters", ["id"], unique=False)
    op.create_index(
        op.f("ix_device_masters_serial"),
        "device_masters",
        ["serial"],
        unique=True,
    )
    op.create_index(
        op.f("ix_device_masters_bed_id"),
        "device_masters",
        ["bed_id"],
        unique=False,
    )

    # -------------------------------------------------------------------------
    # Patient Tables
    # -------------------------------------------------------------------------

    op.create_table(
        "patients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column(
            "gender",
            sa.Enum("MALE", "FEMALE", "OTHER", name="gender"),
            nullable=False,
        ),
        sa.Column("bed_id", sa.Integer(), nullable=True),
        sa.Column("diagnosis", sa.String(), nullable=True),
        sa.Column("weight", sa.Float(), nullable=True),
        sa.Column("height", sa.Float(), nullable=True),
        sa.Column("blood_group", sa.String(), nullable=True),
        sa.Column("doctor", sa.String(), nullable=True),
        sa.Column("admission_time", sa.DateTime(), nullable=False),
        sa.Column("hospital_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("history", sa.JSON(), nullable=True),
        sa.Column("comorbidities", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["bed_id"], ["bed_masters.id"]),
        sa.ForeignKeyConstraint(["hospital_id"], ["hospitals.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_patients_id"), "patients", ["id"], unique=False)
    op.create_index(op.f("ix_patients_bed_id"), "patients", ["bed_id"], unique=False)
    op.create_index(
        op.f("ix_patients_hospital_id"),
        "patients",
        ["hospital_id"],
        unique=False,
    )

    # -------------------------------------------------------------------------
    # Role / Permission Tables
    # -------------------------------------------------------------------------

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_roles_id"), "roles", ["id"], unique=False)

    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("module", sa.String(), nullable=False),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("module", "action", name="uq_permission_module_action"),
    )
    op.create_index(op.f("ix_permissions_id"), "permissions", ["id"], unique=False)

    op.create_table(
        "role_permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("permission_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["permission_id"],
            ["permissions.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
    )
    op.create_index(
        op.f("ix_role_permissions_id"),
        "role_permissions",
        ["id"],
        unique=False,
    )

    # -------------------------------------------------------------------------
    # Users Tables
    # -------------------------------------------------------------------------

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        # These remain String because UserModel currently defines them as String.
        # Convert these later only after refactoring UserModel/auth claims together.
        sa.Column("hospital_id", sa.String(), nullable=False),
        sa.Column("unit_id", sa.String(), nullable=False),
        sa.Column("shift", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_role_id"), "users", ["role_id"], unique=False)
    op.create_index(op.f("ix_users_user_id"), "users", ["user_id"], unique=True)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)


    # -------------------------------------------------------------------------
    # Clinical Notes Tables
    # -------------------------------------------------------------------------

    op.create_table(
        "clinical_notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column(
            "author_name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "note_type",
            sa.Enum(
                "progress",
                "nursing",
                "order",
                "handover",
                name="clinicalnotetype",
            ),
            nullable=False,
        ),
        sa.Column("note_text", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["patient_id"],
            ["patients.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_clinical_notes_id"),
        "clinical_notes",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_clinical_notes_patient_id"),
        "clinical_notes",
        ["patient_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_clinical_notes_author_id"),
        "clinical_notes",
        ["author_id"],
        unique=False,
    )

    # -------------------------------------------------------------------------
    # Patient Staff Assignment Tables
    # -------------------------------------------------------------------------

    op.create_table(
        "patient_staff_assignments",
        sa.Column("id", sa.Integer(), nullable=False),

        sa.Column(
            "patient_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "assignment_type",
            sa.String(),
            nullable=False,
        ),

        sa.Column(
            "assigned_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.Column(
            "ended_at",
            sa.DateTime(),
            nullable=True,
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["patient_id"],
            ["patients.id"],
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_patient_staff_assignments_id"),
        "patient_staff_assignments",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_patient_staff_assignments_patient_id"),
        "patient_staff_assignments",
        ["patient_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_patient_staff_assignments_user_id"),
        "patient_staff_assignments",
        ["user_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_patient_staff_assignments_is_active"),
        "patient_staff_assignments",
        ["is_active"],
        unique=False,
    )

    # -------------------------------------------------------------------------
    # Patient Device Assignment Tables
    # -------------------------------------------------------------------------

    op.create_table(
        "patient_devices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("assigned_at", sa.DateTime(), nullable=True),
        sa.Column("removed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"]),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_patient_devices_id"),
        "patient_devices",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_patient_devices_patient_id"),
        "patient_devices",
        ["patient_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_patient_devices_device_id"),
        "patient_devices",
        ["device_id"],
        unique=False,
    )

    # -------------------------------------------------------------------------
    # Timeline Tables
    # -------------------------------------------------------------------------

    op.create_table(
        "timeline_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "DEVICE_ASSIGNED",
                "DEVICE_REMOVED",
                "STATUS_CHANGED",
                "NOTE_ADDED",
                name="timelineeventtype",
            ),
            nullable=False,
        ),
        sa.Column("event", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_timeline_events_id"), "timeline_events", ["id"], unique=False)
    op.create_index(
        op.f("ix_timeline_events_patient_id"),
        "timeline_events",
        ["patient_id"],
        unique=False,
    )

    # -------------------------------------------------------------------------
    # Vitals Tables
    # -------------------------------------------------------------------------

    op.create_table(
        "vitals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("hr", sa.Float(), nullable=True),
        sa.Column("bp_sys", sa.Float(), nullable=True),
        sa.Column("bp_dia", sa.Float(), nullable=True),
        sa.Column("spo2", sa.Float(), nullable=True),
        sa.Column("temp", sa.Float(), nullable=True),
        sa.Column("rr", sa.Float(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_vitals_id"), "vitals", ["id"], unique=False)
    op.create_index(op.f("ix_vitals_patient_id"), "vitals", ["patient_id"], unique=False)

    # -------------------------------------------------------------------------
    # Alarm Tables
    # -------------------------------------------------------------------------

    op.create_table(
        "alarms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("patient_name", sa.String(), nullable=False),
        sa.Column("bed_id", sa.String(), nullable=False),
        sa.Column("device", sa.String(), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("severity", sa.String(), nullable=False),
        sa.Column("acknowledged", sa.Boolean(), nullable=False),
        sa.Column("silenced", sa.Boolean(), nullable=False),
        sa.Column("escalated", sa.Boolean(), nullable=False),
        sa.Column("acknowledged_by", sa.String(), nullable=True),
        sa.Column("silenced_by", sa.String(), nullable=True),
        sa.Column("silence_until", sa.DateTime(), nullable=True),
        sa.Column("escalated_by", sa.String(), nullable=True),
        sa.Column("escalate_to", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_alarms_id"), "alarms", ["id"], unique=False)
    op.create_index(op.f("ix_alarms_patient_id"), "alarms", ["patient_id"], unique=False)
    op.create_index(op.f("ix_alarms_severity"), "alarms", ["severity"], unique=False)

    # -------------------------------------------------------------------------
    # Latest Patient Vitals Table
    # -------------------------------------------------------------------------

    op.create_table(
        "latest_patient_vitals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("bed_id", sa.Integer(), nullable=True),
        sa.Column("device_id", sa.Integer(), nullable=True),
        sa.Column("hr", sa.Float(), nullable=True),
        sa.Column("bp_sys", sa.Float(), nullable=True),
        sa.Column("bp_dia", sa.Float(), nullable=True),
        sa.Column("spo2", sa.Float(), nullable=True),
        sa.Column("temp", sa.Float(), nullable=True),
        sa.Column("rr", sa.Float(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.ForeignKeyConstraint(["bed_id"], ["bed_masters.id"]),
        sa.ForeignKeyConstraint(["device_id"], ["device_masters.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("patient_id", name="uq_latest_patient_vitals_patient_id"),
    )
    op.create_index(
        op.f("ix_latest_patient_vitals_id"),
        "latest_patient_vitals",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_latest_patient_vitals_patient_id"),
        "latest_patient_vitals",
        ["patient_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_latest_patient_vitals_bed_id"),
        "latest_patient_vitals",
        ["bed_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_latest_patient_vitals_device_id"),
        "latest_patient_vitals",
        ["device_id"],
        unique=False,
    )


def downgrade() -> None:
    # -------------------------------------------------------------------------
    # Latest Patient Vitals Table
    # -------------------------------------------------------------------------

    op.drop_index(op.f("ix_latest_patient_vitals_device_id"), table_name="latest_patient_vitals")
    op.drop_index(op.f("ix_latest_patient_vitals_bed_id"), table_name="latest_patient_vitals")
    op.drop_index(op.f("ix_latest_patient_vitals_patient_id"), table_name="latest_patient_vitals")
    op.drop_index(op.f("ix_latest_patient_vitals_id"), table_name="latest_patient_vitals")
    op.drop_table("latest_patient_vitals")

    # -------------------------------------------------------------------------
    # Alarm Tables
    # -------------------------------------------------------------------------

    op.drop_index(op.f("ix_alarms_severity"), table_name="alarms")
    op.drop_index(op.f("ix_alarms_patient_id"), table_name="alarms")
    op.drop_index(op.f("ix_alarms_id"), table_name="alarms")
    op.drop_table("alarms")

    # -------------------------------------------------------------------------
    # Vitals Tables
    # -------------------------------------------------------------------------

    op.drop_index(op.f("ix_vitals_patient_id"), table_name="vitals")
    op.drop_index(op.f("ix_vitals_id"), table_name="vitals")
    op.drop_table("vitals")

    # -------------------------------------------------------------------------
    # Timeline Tables
    # -------------------------------------------------------------------------

    op.drop_index(op.f("ix_timeline_events_patient_id"), table_name="timeline_events")
    op.drop_index(op.f("ix_timeline_events_id"), table_name="timeline_events")
    op.drop_table("timeline_events")

    # -------------------------------------------------------------------------
    # Patient Staff Assignment Tables
    # -------------------------------------------------------------------------

    op.drop_index(
        op.f("ix_patient_staff_assignments_is_active"),
        table_name="patient_staff_assignments",
    )

    op.drop_index(
        op.f("ix_patient_staff_assignments_user_id"),
        table_name="patient_staff_assignments",
    )

    op.drop_index(
        op.f("ix_patient_staff_assignments_patient_id"),
        table_name="patient_staff_assignments",
    )

    op.drop_index(
        op.f("ix_patient_staff_assignments_id"),
        table_name="patient_staff_assignments",
    )

    op.drop_table("patient_staff_assignments")

    # -------------------------------------------------------------------------
    # Patient Device Assignment Tables
    # -------------------------------------------------------------------------

    op.drop_index(op.f("ix_patient_devices_device_id"), table_name="patient_devices")
    op.drop_index(op.f("ix_patient_devices_patient_id"), table_name="patient_devices")
    op.drop_index(op.f("ix_patient_devices_id"), table_name="patient_devices")
    op.drop_table("patient_devices")

    # -------------------------------------------------------------------------
    # Clinical Notes Tables
    # -------------------------------------------------------------------------

    op.drop_index(
        op.f("ix_clinical_notes_author_id"),
        table_name="clinical_notes",
    )

    op.drop_index(
        op.f("ix_clinical_notes_patient_id"),
        table_name="clinical_notes",
    )

    op.drop_index(
        op.f("ix_clinical_notes_id"),
        table_name="clinical_notes",
    )

    op.drop_table("clinical_notes")

    # -------------------------------------------------------------------------
    # User Tables
    # -------------------------------------------------------------------------

    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_user_id"), table_name="users")
    op.drop_index(op.f("ix_users_role_id"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")

    # -------------------------------------------------------------------------
    # Role / Permission Tables
    # -------------------------------------------------------------------------

    op.drop_index(op.f("ix_role_permissions_id"), table_name="role_permissions")
    op.drop_table("role_permissions")

    op.drop_index(op.f("ix_permissions_id"), table_name="permissions")
    op.drop_table("permissions")

    op.drop_index(op.f("ix_roles_id"), table_name="roles")
    op.drop_table("roles")

    # -------------------------------------------------------------------------
    # Patient Tables
    # -------------------------------------------------------------------------

    op.drop_index(op.f("ix_patients_hospital_id"), table_name="patients")
    op.drop_index(op.f("ix_patients_bed_id"), table_name="patients")
    op.drop_index(op.f("ix_patients_id"), table_name="patients")
    op.drop_table("patients")

    # -------------------------------------------------------------------------
    # Admin Master Tables
    # -------------------------------------------------------------------------

    op.drop_index(op.f("ix_device_masters_bed_id"), table_name="device_masters")
    op.drop_index(op.f("ix_device_masters_serial"), table_name="device_masters")
    op.drop_index(op.f("ix_device_masters_id"), table_name="device_masters")
    op.drop_table("device_masters")

    op.drop_index(op.f("ix_bed_masters_icu_unit_id"), table_name="bed_masters")
    op.drop_index(op.f("ix_bed_masters_bed_id"), table_name="bed_masters")
    op.drop_index(op.f("ix_bed_masters_id"), table_name="bed_masters")
    op.drop_table("bed_masters")

    op.drop_index(op.f("ix_icu_unit_masters_icu_name"), table_name="icu_unit_masters")
    op.drop_index(op.f("ix_icu_unit_masters_id"), table_name="icu_unit_masters")
    op.drop_table("icu_unit_masters")

    # -------------------------------------------------------------------------
    # Hospital Tables
    # -------------------------------------------------------------------------

    op.drop_index(op.f("ix_hospital_units_id"), table_name="hospital_units")
    op.drop_index(op.f("ix_hospital_units_hospital_id"), table_name="hospital_units")
    op.drop_table("hospital_units")

    op.drop_index(op.f("ix_hospitals_id"), table_name="hospitals")
    op.drop_table("hospitals")

    # -------------------------------------------------------------------------
    # Device Type / Runtime Device Tables
    # -------------------------------------------------------------------------

    op.drop_index(op.f("ix_devices_serial_number"), table_name="devices")
    op.drop_index(op.f("ix_devices_id"), table_name="devices")
    op.drop_table("devices")

    op.drop_index(op.f("ix_device_types_id"), table_name="device_types")
    op.drop_table("device_types")