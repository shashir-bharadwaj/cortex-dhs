from typing import List

from app.domain.entities.patient import Patient
from app.infrastructure.database.mappers.vital_mapper import VitalMapper
from app.infrastructure.database.models.patient import PatientModel


class PatientMapper:
    """
    Mapper responsible for converting Patient domain entities
    and SQLAlchemy models.
    """

    @staticmethod
    def to_domain(
        patient_model: PatientModel,
    ) -> Patient:
        """
        Convert Patient SQLAlchemy model -> domain entity.
        """

        vitals = []

        if getattr(patient_model, "vitals", None):
            vitals = VitalMapper.to_domain_list(
                patient_model.vitals
            )

        timeline = []

        if getattr(patient_model, "timeline", None):
            timeline = [
                {
                    "id": event.id,
                    "time": (
                        event.created_at.strftime("%H:%M")
                        if event.created_at
                        else ""
                    ),
                    "event": event.event,
                    "type": event.type,
                }
                for event in patient_model.timeline
            ]

        return Patient(
            id=patient_model.id,

            # Patient identifiers
            mrn=patient_model.mrn,
            cr_number=patient_model.cr_number,

            # Demographics
            name=patient_model.name,
            contact_number=patient_model.contact_number,
            age=patient_model.age,
            gender=patient_model.gender,
            blood_group=patient_model.blood_group,
            weight=patient_model.weight,
            height=patient_model.height,

            # Admission details
            bed_id=patient_model.bed_id,
            diagnosis=patient_model.diagnosis,
            doctor=patient_model.doctor,
            admission_time=patient_model.admission_time,
            hospital_id=patient_model.hospital_id,
            status=patient_model.status,

            # Clinical context
            history=patient_model.history or [],
            comorbidities=patient_model.comorbidities or [],

            # Relationships
            vitals=vitals,
            timeline=timeline,
            bed=getattr(patient_model, "bed", None),
        )

    @staticmethod
    def to_model(
        entity: Patient,
    ) -> PatientModel:
        """
        Convert Patient domain entity -> SQLAlchemy model.
        """

        return PatientModel(
            id=entity.id,

            # Patient identifiers
            mrn=entity.mrn,
            cr_number=entity.cr_number,

            # Demographics
            name=entity.name,
            contact_number=entity.contact_number,
            age=entity.age,
            gender=entity.gender,
            blood_group=entity.blood_group,
            weight=entity.weight,
            height=entity.height,

            # Admission details
            bed_id=entity.bed_id,
            diagnosis=entity.diagnosis,
            doctor=entity.doctor,
            admission_time=entity.admission_time,
            hospital_id=entity.hospital_id,
            status=entity.status,

            # Clinical context
            history=entity.history,
            comorbidities=entity.comorbidities,
        )

    @staticmethod
    def to_domain_list(
        patient_models: List[PatientModel],
    ) -> List[Patient]:
        """
        Convert Patient model list -> domain entity list.
        """

        return [
            PatientMapper.to_domain(model)
            for model in patient_models
        ]