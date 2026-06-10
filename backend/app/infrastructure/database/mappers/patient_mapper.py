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
            vitals = VitalMapper.to_domain_list(patient_model.vitals)

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
            name=patient_model.name,
            age=patient_model.age,
            gender=patient_model.gender,
            bed_id=patient_model.bed_id,
            diagnosis=patient_model.diagnosis,
            weight=patient_model.weight,
            height=patient_model.height,
            blood_group=patient_model.blood_group,
            doctor=patient_model.doctor,
            admission_time=patient_model.admission_time,
            hospital_id=patient_model.hospital_id,
            status=patient_model.status,
            history=patient_model.history or [],
            comorbidities=patient_model.comorbidities or [],
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
            name=entity.name,
            age=entity.age,
            gender=entity.gender,
            bed_id=entity.bed_id,
            diagnosis=entity.diagnosis,
            weight=entity.weight,
            height=entity.height,
            blood_group=entity.blood_group,
            doctor=entity.doctor,
            admission_time=entity.admission_time,
            hospital_id=entity.hospital_id,
            status=entity.status,
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