from typing import List

from app.domain.entities.patient import Patient
from app.domain.entities.vital import Vital

from app.infrastructure.database.models.patient import (
    PatientModel,
)
from app.infrastructure.database.models.vital import (
    VitalModel,
)


class PatientMapper:
    """
    Mapper responsible for converting Patient domain entities
    and SQLAlchemy models.
    """

    # ------------------------------------------------------------------
    # Vital mappings
    # ------------------------------------------------------------------

    @staticmethod
    def vital_to_domain(
        vital_model: VitalModel,
    ) -> Vital:
        """
        Convert Vital SQLAlchemy model -> Vital domain entity.
        """
        return Vital(
            id=vital_model.id,
            patient_id=vital_model.patient_id,
            hr=vital_model.hr,
            bp_sys=vital_model.bp_sys,
            bp_dia=vital_model.bp_dia,
            spo2=vital_model.spo2,
            temp=vital_model.temp,
            rr=vital_model.rr,
            recorded_at=vital_model.recorded_at,
        )

    @staticmethod
    def vital_to_domain_list(
        vital_models: List[VitalModel],
    ) -> List[Vital]:
        """
        Convert Vital model list -> Vital domain list.
        """
        return [
            PatientMapper.vital_to_domain(vital)
            for vital in vital_models
        ]

    # ------------------------------------------------------------------
    # Patient mappings
    # ------------------------------------------------------------------

    @staticmethod
    def to_domain(
        patient_model: PatientModel,
    ) -> Patient:
        """
        Convert Patient SQLAlchemy model -> domain entity.
        """
        vitals: List[Vital] = []

        if getattr(patient_model, "vitals", None):
            vitals = PatientMapper.vital_to_domain_list(
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