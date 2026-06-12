"""
Dev-only seed script for Cortex ICU.
"""

import random
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.domain.enums.auth import ShiftType, UserRole
from app.domain.enums.clinical_note import ClinicalNoteType
from app.domain.enums.patient import Gender
from app.domain.enums.permission import PermissionAction, PermissionModule
from app.domain.enums.timeline import TimelineEventType
from app.infrastructure.database.models.alarm import AlarmModel
from app.infrastructure.database.models.bed import BedMasterModel
from app.infrastructure.database.models.clinical_note import ClinicalNoteModel
from app.infrastructure.database.models.device_master import DeviceMasterModel
from app.infrastructure.database.models.fluid_balance import FluidBalanceModel
from app.infrastructure.database.models.hospital import HospitalModel
from app.infrastructure.database.models.hospital_unit import HospitalUnitModel
from app.infrastructure.database.models.icu_unit_master import ICUUnitMasterModel
from app.infrastructure.database.models.lab_result import LabResultModel
from app.infrastructure.database.models.latest_vital import LatestVitalModel
from app.infrastructure.database.models.medication_order import MedicationOrderModel
from app.infrastructure.database.models.patient import PatientModel
from app.infrastructure.database.models.patient_staff_assignment import PatientStaffAssignmentModel
from app.infrastructure.database.models.permission import PermissionModel
from app.infrastructure.database.models.role import RoleModel
from app.infrastructure.database.models.role_permission import RolePermissionModel
from app.infrastructure.database.models.timeline import TimelineEventModel
from app.infrastructure.database.models.user import UserModel
from app.infrastructure.database.models.ventilator_setting import VentilatorSettingModel
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

SEED_BED_IDS = [
    "B1", "B2", "B3", "B4", "B5",
    "B6", "B7", "B8", "B9", "B10",
]

SEED_PATIENT_NAMES = [
    "Rahul Sharma",
    "Ananya Rao",
    "Vikram Mehta",
    "Priya Nair",
    "Arjun Reddy",
    "Sneha Kapoor",
    "Karthik Iyer",
    "Neha Verma",
    "Rohan Malhotra",
    "Meera Joshi",
]

SEED_DEVICE_SERIALS = [
    f"MONITOR-SEED-{index:03d}"
    for index in range(1, 11)
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

# Per-patient seed data so each patient has a distinct clinical profile
PATIENT_PAYLOADS = [
    {
        "mrn": "MRN-100001",
        "cr_number": "CR-2026-0001",
        "contact_number": "9876543201",
        "name": "Rahul Sharma",
        "age": 45,
        "gender": Gender.MALE,
        "diagnosis": "Pneumonia",
        "weight": 72.5,
        "height": 171.0,
        "blood_group": "O+",
        "doctor": "Dr. Meera Nair",
        "history": ["Admitted with respiratory distress", "History of smoking"],
        "comorbidities": ["Hypertension"],
        "ventilator": {"mode": "PSV", "fio2": 0.35, "peep": 5.0, "set_rr": 14, "tidal_volume": 460.0},
        "labs": {"ph": 7.38, "pao2": 85.0, "paco2": 43.0, "hco3": 24.0, "rbs": 140.0},
        "medications": [
            {"drug_name": "Piperacillin-Tazobactam", "order_type": "STAT", "dose": "4.5g", "route": "IV", "schedule": "Q8H", "status": "Running", "rate_ml_hr": 10.0, "remaining_vol_ml": 90.0},
            {"drug_name": "Paracetamol", "order_type": "PRN", "dose": "500mg", "route": "Oral", "schedule": "Q6H", "status": "Given"},
            {"drug_name": "Pantoprazole", "order_type": "STAT", "dose": "40mg", "route": "IV", "schedule": "OD", "status": "Pending"},
            {"drug_name": "Salbutamol Nebulisation", "order_type": "PRN", "dose": "2.5mg", "route": "Inhaled", "schedule": "Q4H", "status": "Given"},
            {"drug_name": "Enoxaparin", "order_type": "STAT", "dose": "40mg", "route": "SC", "schedule": "OD", "status": "Pending"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Patient admitted with community-acquired pneumonia. SpO2 88% on RA. Started on IV antibiotics and supplemental oxygen. CXR shows bilateral infiltrates."),
            (ClinicalNoteType.NURSING, "Patient cooperative. Repositioned Q2H. Oral care done. IV line patent. O2 therapy maintained at 6L/min via face mask."),
        ],
    },
    {
        "mrn": "MRN-100002",
        "cr_number": "CR-2026-0002",
        "contact_number": "9876543202",
        "name": "Ananya Rao",
        "age": 52,
        "gender": Gender.FEMALE,
        "diagnosis": "Sepsis",
        "weight": 64.0,
        "height": 164.0,
        "blood_group": "A+",
        "doctor": "Dr. Arjun Menon",
        "history": ["Transferred from emergency ward", "Source: UTI"],
        "comorbidities": ["Diabetes"],
        "ventilator": {"mode": "AC/VC", "fio2": 0.50, "peep": 6.0, "set_rr": 16, "tidal_volume": 420.0},
        "labs": {"ph": 7.32, "pao2": 72.0, "paco2": 48.0, "hco3": 22.0, "rbs": 210.0},
        "medications": [
            {"drug_name": "Meropenem", "order_type": "STAT", "dose": "1g", "route": "IV", "schedule": "Q8H", "status": "Running", "rate_ml_hr": 8.0, "remaining_vol_ml": 60.0},
            {"drug_name": "Noradrenaline", "order_type": "Infusion", "dose": "4mg/50ml", "route": "IV", "schedule": "Titrate", "status": "Running", "rate_ml_hr": 5.0, "remaining_vol_ml": 35.0},
            {"drug_name": "Insulin Infusion", "order_type": "Infusion", "dose": "50U/50ml", "route": "IV", "schedule": "Sliding Scale", "status": "Running", "rate_ml_hr": 3.0, "remaining_vol_ml": 40.0},
            {"drug_name": "Hydrocortisone", "order_type": "STAT", "dose": "100mg", "route": "IV", "schedule": "Q8H", "status": "Pending"},
            {"drug_name": "Pantoprazole", "order_type": "STAT", "dose": "40mg", "route": "IV", "schedule": "BD", "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Sepsis secondary to UTI. Blood cultures sent. Started on broad-spectrum antibiotics. On vasopressor support. Lactate 4.2 mmol/L. Target MAP >65 mmHg."),
            (ClinicalNoteType.NURSING, "Patient intubated and mechanically ventilated. Hourly UO monitoring. Foley catheter in situ. Sedation: Propofol 10ml/hr."),
            (ClinicalNoteType.ORDER, "Blood cultures x2, urine C&S, CBC, LFT, RFT, Procalcitonin stat."),
        ],
    },
    {
        "mrn": "MRN-100003",
        "cr_number": "CR-2026-0003",
        "contact_number": "9876543203",
        "name": "Vikram Mehta",
        "age": 61,
        "gender": Gender.MALE,
        "diagnosis": "Post cardiac arrest monitoring",
        "weight": 78.0,
        "height": 176.0,
        "blood_group": "B+",
        "doctor": "Dr. Kavita Rao",
        "history": ["Witnessed VF arrest", "Bystander CPR performed", "ROSC after 12 min"],
        "comorbidities": ["Coronary artery disease"],
        "ventilator": {"mode": "AC/VC", "fio2": 0.40, "peep": 5.0, "set_rr": 14, "tidal_volume": 520.0},
        "labs": {"ph": 7.29, "pao2": 82.0, "paco2": 46.0, "hco3": 21.0, "rbs": 175.0},
        "medications": [
            {"drug_name": "Amiodarone", "order_type": "Infusion", "dose": "300mg/50ml", "route": "IV", "schedule": "Maintenance", "status": "Running", "rate_ml_hr": 4.0, "remaining_vol_ml": 32.0},
            {"drug_name": "Heparin", "order_type": "Infusion", "dose": "25000U/50ml", "route": "IV", "schedule": "Titrate APTT", "status": "Running", "rate_ml_hr": 3.0, "remaining_vol_ml": 45.0},
            {"drug_name": "Aspirin", "order_type": "STAT", "dose": "75mg", "route": "Oral", "schedule": "OD", "status": "Given"},
            {"drug_name": "Atorvastatin", "order_type": "STAT", "dose": "40mg", "route": "Oral", "schedule": "OD", "status": "Pending"},
            {"drug_name": "Propofol", "order_type": "Infusion", "dose": "200mg/20ml", "route": "IV", "schedule": "Titrate sedation", "status": "Running", "rate_ml_hr": 10.0, "remaining_vol_ml": 15.0},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Post VF arrest. Targeted temperature management initiated. Target temp 36°C. Neuro exam deferred pending sedation wean. Echo ordered — EF 30%."),
            (ClinicalNoteType.NURSING, "Cooling blanket in situ. Core temp 36.2°C. Continuous EEG monitoring in progress. Sedation maintained."),
        ],
    },
    {
        "mrn": "MRN-100004",
        "cr_number": "CR-2026-0004",
        "contact_number": "9876543204",
        "name": "Priya Nair",
        "age": 38,
        "gender": Gender.FEMALE,
        "diagnosis": "ARDS",
        "weight": 58.0,
        "height": 160.0,
        "blood_group": "AB+",
        "doctor": "Dr. V. Pillai",
        "history": ["Severe hypoxia on admission", "COVID-19 associated ARDS"],
        "comorbidities": ["Asthma"],
        "ventilator": {"mode": "AC/PC", "fio2": 0.70, "peep": 10.0, "set_rr": 18, "tidal_volume": 350.0},
        "labs": {"ph": 7.26, "pao2": 60.0, "paco2": 55.0, "hco3": 19.0, "rbs": 132.0},
        "medications": [
            {"drug_name": "Cisatracurium", "order_type": "Infusion", "dose": "200mg/50ml", "route": "IV", "schedule": "Titrate TOF", "status": "Running", "rate_ml_hr": 6.0, "remaining_vol_ml": 28.0},
            {"drug_name": "Noradrenaline", "order_type": "Infusion", "dose": "4mg/50ml", "route": "IV", "schedule": "Titrate MAP", "status": "Running", "rate_ml_hr": 4.0, "remaining_vol_ml": 20.0},
            {"drug_name": "Dexamethasone", "order_type": "STAT", "dose": "8mg", "route": "IV", "schedule": "OD", "status": "Given"},
            {"drug_name": "Enoxaparin", "order_type": "STAT", "dose": "60mg", "route": "SC", "schedule": "BD", "status": "Pending"},
            {"drug_name": "Pantoprazole", "order_type": "STAT", "dose": "40mg", "route": "IV", "schedule": "OD", "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Severe ARDS — P/F ratio 85. Prone positioning initiated for 16 hours. Low tidal volume ventilation. Daily RASS score -3. Paralysis maintained."),
            (ClinicalNoteType.NURSING, "Prone position secured with pillows. Pressure area care done. ETT ties checked. Suction performed Q2H. Eyes taped."),
            (ClinicalNoteType.HANDOVER, "Patient remains critically ill. Prone session ongoing. Vasopressor requirement stable. Family counselled about severity. ICU consultant to review AM."),
        ],
    },
    {
        "mrn": "MRN-100005",
        "cr_number": "CR-2026-0005",
        "contact_number": "9876543205",
        "name": "Arjun Reddy",
        "age": 70,
        "gender": Gender.MALE,
        "diagnosis": "Acute Kidney Injury",
        "weight": 80.0,
        "height": 174.0,
        "blood_group": "O-",
        "doctor": "Dr. Sana Khan",
        "history": ["Low urine output and hypotension", "CKD stage 3 at baseline"],
        "comorbidities": ["Chronic kidney disease"],
        "ventilator": {"mode": "CPAP", "fio2": 0.30, "peep": 4.0, "set_rr": 12, "tidal_volume": 480.0},
        "labs": {"ph": 7.34, "pao2": 90.0, "paco2": 42.0, "hco3": 21.0, "rbs": 160.0},
        "medications": [
            {"drug_name": "Furosemide", "order_type": "Infusion", "dose": "500mg/50ml", "route": "IV", "schedule": "Titrate UO", "status": "Running", "rate_ml_hr": 5.0, "remaining_vol_ml": 38.0},
            {"drug_name": "Sodium Bicarbonate", "order_type": "Infusion", "dose": "100 mEq/500ml", "route": "IV", "schedule": "Over 4 hrs", "status": "Completed"},
            {"drug_name": "Calcium Gluconate", "order_type": "STAT", "dose": "1g", "route": "IV", "schedule": "Immediate", "status": "Given"},
            {"drug_name": "Erythropoietin", "order_type": "STAT", "dose": "4000 IU", "route": "SC", "schedule": "TIW", "status": "Pending"},
            {"drug_name": "Pantoprazole", "order_type": "STAT", "dose": "40mg", "route": "IV", "schedule": "OD", "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "AKI stage 3. Urine output 15ml/hr. Creatinine 6.8 mg/dL, K+ 5.8. CRRT being considered if no improvement in next 6h. Nephrology consulted."),
            (ClinicalNoteType.NURSING, "Strict fluid balance every hour. Renal diet initiated. IV access secured bilaterally. Weight 80.2 kg this morning."),
        ],
    },
    {
        "mrn": "MRN-100006",
        "cr_number": "CR-2026-0006",
        "contact_number": "9876543206",
        "name": "Sneha Kapoor",
        "age": 47,
        "gender": Gender.FEMALE,
        "diagnosis": "Septic Shock",
        "weight": 62.0,
        "height": 162.0,
        "blood_group": "A-",
        "doctor": "Dr. Arjun Menon",
        "history": ["Started on vasopressor support", "Source: Abdominal (post-op)"],
        "comorbidities": ["Diabetes", "Hypothyroidism"],
        "ventilator": {"mode": "AC/VC", "fio2": 0.55, "peep": 7.0, "set_rr": 16, "tidal_volume": 410.0},
        "labs": {"ph": 7.28, "pao2": 68.0, "paco2": 50.0, "hco3": 20.0, "rbs": 240.0},
        "medications": [
            {"drug_name": "Vasopressin", "order_type": "Infusion", "dose": "20U/50ml", "route": "IV", "schedule": "0.03 U/min fixed", "status": "Running", "rate_ml_hr": 4.5, "remaining_vol_ml": 22.0},
            {"drug_name": "Noradrenaline", "order_type": "Infusion", "dose": "8mg/50ml", "route": "IV", "schedule": "Titrate MAP", "status": "Running", "rate_ml_hr": 8.0, "remaining_vol_ml": 18.0},
            {"drug_name": "Meropenem", "order_type": "STAT", "dose": "2g", "route": "IV", "schedule": "Q8H extended", "status": "Running", "rate_ml_hr": 12.0, "remaining_vol_ml": 80.0},
            {"drug_name": "Insulin Infusion", "order_type": "Infusion", "dose": "50U/50ml", "route": "IV", "schedule": "Sliding Scale", "status": "Running", "rate_ml_hr": 2.0, "remaining_vol_ml": 42.0},
            {"drug_name": "Levothyroxine", "order_type": "STAT", "dose": "100mcg", "route": "IV", "schedule": "OD", "status": "Pending"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Post-op day 2 septic shock. Two vasopressors running. Lactate 5.1 mmol/L — not improving. Surgical team notified of possible anastomotic leak. CT Abdomen ordered."),
            (ClinicalNoteType.NURSING, "Continuous vasopressor monitoring. MAP 62 mmHg. Foley draining 20ml/hr. Wound dressing intact. Blood glucose Q1H — 230 mg/dL, insulin adjusted."),
        ],
    },
    {
        "mrn": "MRN-100007",
        "cr_number": "CR-2026-0007",
        "contact_number": "9876543207",
        "name": "Karthik Iyer",
        "age": 59,
        "gender": Gender.MALE,
        "diagnosis": "Stroke",
        "weight": 74.0,
        "height": 172.0,
        "blood_group": "B-",
        "doctor": "Dr. Kavita Rao",
        "history": ["Right-sided weakness with aphasia", "NIHSS score 18 on admission"],
        "comorbidities": ["Hypertension", "Dyslipidemia"],
        "ventilator": {"mode": "PSV", "fio2": 0.28, "peep": 4.0, "set_rr": 12, "tidal_volume": 500.0},
        "labs": {"ph": 7.42, "pao2": 96.0, "paco2": 39.0, "hco3": 25.0, "rbs": 155.0},
        "medications": [
            {"drug_name": "Alteplase", "order_type": "STAT", "dose": "67mg", "route": "IV", "schedule": "Immediate (completed)", "status": "Completed"},
            {"drug_name": "Aspirin", "order_type": "STAT", "dose": "300mg", "route": "Oral", "schedule": "OD", "status": "Given"},
            {"drug_name": "Amlodipine", "order_type": "STAT", "dose": "5mg", "route": "Oral", "schedule": "OD", "status": "Given"},
            {"drug_name": "Atorvastatin", "order_type": "STAT", "dose": "80mg", "route": "Oral", "schedule": "OD", "status": "Pending"},
            {"drug_name": "Labetalol", "order_type": "PRN", "dose": "20mg", "route": "IV", "schedule": "PRN SBP >180", "status": "Pending"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Ischemic stroke left MCA territory. Thrombolysis with Alteplase completed. BP target <180/105 for next 24h. No haemorrhagic transformation on repeat CT."),
            (ClinicalNoteType.NURSING, "Neuro obs Q1H: GCS 11 (E3V3M5). Right arm power 1/5. Aspiration precautions in place. HOB 30 degrees. NG tube for medications."),
        ],
    },
    {
        "mrn": "MRN-100008",
        "cr_number": "CR-2026-0008",
        "contact_number": "9876543208",
        "name": "Neha Verma",
        "age": 66,
        "gender": Gender.FEMALE,
        "diagnosis": "COPD Exacerbation",
        "weight": 55.0,
        "height": 158.0,
        "blood_group": "O+",
        "doctor": "Dr. Meera Nair",
        "history": ["Presented with acute breathlessness", "COPD GOLD stage 3"],
        "comorbidities": ["COPD"],
        "ventilator": {"mode": "SIMV", "fio2": 0.32, "peep": 5.0, "set_rr": 14, "tidal_volume": 380.0},
        "labs": {"ph": 7.31, "pao2": 58.0, "paco2": 62.0, "hco3": 28.0, "rbs": 98.0},
        "medications": [
            {"drug_name": "Salbutamol Nebulisation", "order_type": "PRN", "dose": "5mg", "route": "Inhaled", "schedule": "Q4H", "status": "Given"},
            {"drug_name": "Ipratropium Nebulisation", "order_type": "PRN", "dose": "0.5mg", "route": "Inhaled", "schedule": "Q6H", "status": "Given"},
            {"drug_name": "Methylprednisolone", "order_type": "STAT", "dose": "40mg", "route": "IV", "schedule": "OD", "status": "Running", "rate_ml_hr": 10.0, "remaining_vol_ml": 40.0},
            {"drug_name": "Doxycycline", "order_type": "STAT", "dose": "200mg", "route": "Oral", "schedule": "OD", "status": "Given"},
            {"drug_name": "Theophylline", "order_type": "Infusion", "dose": "250mg/500ml", "route": "IV", "schedule": "Over 24h", "status": "Running", "rate_ml_hr": 21.0, "remaining_vol_ml": 300.0},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "COPD exacerbation with type 2 respiratory failure. pCO2 62 — on NIV BiPAP. Settings: IPAP 14, EPAP 4. ABG improving. Aim to avoid intubation."),
            (ClinicalNoteType.NURSING, "NIV mask fit checked. Pressure sore prevention — barrier cream applied. Patient anxious, reassured. Nebulisations given. Chest physio done."),
        ],
    },
    {
        "mrn": "MRN-100009",
        "cr_number": "CR-2026-0009",
        "contact_number": "9876543209",
        "name": "Rohan Malhotra",
        "age": 54,
        "gender": Gender.MALE,
        "diagnosis": "Myocardial Infarction",
        "weight": 82.0,
        "height": 178.0,
        "blood_group": "AB-",
        "doctor": "Dr. A. Mehta",
        "history": ["Chest pain with elevated troponin", "STEMI — LAD occlusion", "PCI performed"],
        "comorbidities": ["Diabetes", "Hypertension"],
        "ventilator": {"mode": "CPAP", "fio2": 0.28, "peep": 4.0, "set_rr": 12, "tidal_volume": 530.0},
        "labs": {"ph": 7.40, "pao2": 94.0, "paco2": 40.0, "hco3": 24.0, "rbs": 185.0},
        "medications": [
            {"drug_name": "Aspirin", "order_type": "STAT", "dose": "75mg", "route": "Oral", "schedule": "OD", "status": "Given"},
            {"drug_name": "Ticagrelor", "order_type": "STAT", "dose": "90mg", "route": "Oral", "schedule": "BD", "status": "Given"},
            {"drug_name": "Atorvastatin", "order_type": "STAT", "dose": "80mg", "route": "Oral", "schedule": "OD", "status": "Given"},
            {"drug_name": "Heparin", "order_type": "Infusion", "dose": "25000U/50ml", "route": "IV", "schedule": "Titrate APTT", "status": "Running", "rate_ml_hr": 3.0, "remaining_vol_ml": 40.0},
            {"drug_name": "Metoprolol", "order_type": "STAT", "dose": "25mg", "route": "Oral", "schedule": "BD", "status": "Pending"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "STEMI with successful primary PCI to LAD. Drug-eluting stent deployed. Post-procedure EF 40%. On dual antiplatelet and anticoagulation. Serial ECG and troponin monitoring."),
            (ClinicalNoteType.NURSING, "Groin site (right femoral) checked — no haematoma. Peripheral pulses intact. BP 130/80. Ambulation restricted for 6h post-procedure."),
        ],
    },
    {
        "mrn": "MRN-100010",
        "cr_number": "CR-2026-0010",
        "contact_number": "9876543210",
        "name": "Meera Joshi",
        "age": 73,
        "gender": Gender.FEMALE,
        "diagnosis": "Multi Organ Dysfunction",
        "weight": 60.0,
        "height": 159.0,
        "blood_group": "A+",
        "doctor": "Dr. V. Pillai",
        "history": ["Transferred from ward after clinical deterioration", "Background CLD — Child-Pugh C"],
        "comorbidities": ["Chronic liver disease"],
        "ventilator": {"mode": "AC/VC", "fio2": 0.60, "peep": 8.0, "set_rr": 16, "tidal_volume": 360.0},
        "labs": {"ph": 7.24, "pao2": 64.0, "paco2": 50.0, "hco3": 18.0, "rbs": 70.0},
        "medications": [
            {"drug_name": "Noradrenaline", "order_type": "Infusion", "dose": "4mg/50ml", "route": "IV", "schedule": "Titrate MAP", "status": "Running", "rate_ml_hr": 7.0, "remaining_vol_ml": 25.0},
            {"drug_name": "Terlipressin", "order_type": "Infusion", "dose": "1mg/50ml", "route": "IV", "schedule": "Q6H", "status": "Running", "rate_ml_hr": 8.0, "remaining_vol_ml": 30.0},
            {"drug_name": "Albumin", "order_type": "Infusion", "dose": "20g/100ml", "route": "IV", "schedule": "BD", "status": "Given"},
            {"drug_name": "Rifaximin", "order_type": "STAT", "dose": "550mg", "route": "Oral", "schedule": "BD", "status": "Pending"},
            {"drug_name": "Lactulose", "order_type": "STAT", "dose": "30ml", "route": "Oral", "schedule": "TDS", "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "MODS — liver (Child-Pugh C), renal (creatinine 3.2), respiratory failure (FiO2 0.6). Prognosis discussed with family. Goals of care conversation documented."),
            (ClinicalNoteType.NURSING, "Patient sedated — RASS -3. Pressure area care Q2H. Eye care done. NG tube in situ. Enteral feeding started at 20ml/hr. Family at bedside."),
            (ClinicalNoteType.HANDOVER, "Critical patient — MODS. Goals of care: full active treatment per family wishes. Palliative care referral declined. Senior review AM."),
        ],
    },
]

password_service = PasswordService()


def utc_now() -> datetime:
    return datetime.now(UTC)


def clear_seed_data(db: Session) -> None:
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

        db.query(ClinicalNoteModel).filter(
            ClinicalNoteModel.patient_id.in_(seed_patient_ids)
        ).delete(synchronize_session=False)

        db.query(VentilatorSettingModel).filter(
            VentilatorSettingModel.patient_id.in_(seed_patient_ids)
        ).delete(synchronize_session=False)

        db.query(LabResultModel).filter(
            LabResultModel.patient_id.in_(seed_patient_ids)
        ).delete(synchronize_session=False)

        db.query(FluidBalanceModel).filter(
            FluidBalanceModel.patient_id.in_(seed_patient_ids)
        ).delete(synchronize_session=False)

        db.query(MedicationOrderModel).filter(
            MedicationOrderModel.patient_id.in_(seed_patient_ids)
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
        [PermissionAction.VIEW, PermissionAction.CREATE, PermissionAction.MODIFY],
    )
    doctor_permissions += permissions_for(
        PermissionModule.VITALS,
        [PermissionAction.VIEW, PermissionAction.CREATE],
    )
    doctor_permissions += permissions_for(
        PermissionModule.TIMELINE,
        [PermissionAction.VIEW, PermissionAction.CREATE],
    )
    doctor_permissions += permissions_for(
        PermissionModule.ALARMS,
        [PermissionAction.VIEW, PermissionAction.MODIFY],
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
        [PermissionAction.VIEW, PermissionAction.CREATE],
    )
    nurse_permissions += permissions_for(
        PermissionModule.TIMELINE,
        [PermissionAction.VIEW, PermissionAction.CREATE],
    )
    nurse_permissions += permissions_for(
        PermissionModule.ALARMS,
        [PermissionAction.VIEW, PermissionAction.MODIFY],
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
    beds: list[BedMasterModel] = []

    for index, bed_code in enumerate(SEED_BED_IDS, start=1):
        if index <= 5:
            icu_unit = icu_units[0]
            ward = "MICU"
            floor = "1"
        elif index <= 8:
            icu_unit = icu_units[1]
            ward = "SICU"
            floor = "2"
        else:
            icu_unit = icu_units[2]
            ward = "NICU"
            floor = "3"

        bed = BedMasterModel(
            bed_id=bed_code,
            icu_unit_id=icu_unit.id,
            bed_type="ICU",
            department="Critical Care",
            ward=ward,
            floor=floor,
            room=f"{floor}{index:02d}",
            cleaning_status="CLEAN",
            maintenance_status="OK",
            operational_status="OCCUPIED",
            last_sanitized=utc_now(),
        )

        db.add(bed)
        db.flush()
        beds.append(bed)

    return beds


def seed_device_masters(
    db: Session,
    beds: list[BedMasterModel],
) -> list[DeviceMasterModel]:
    devices: list[DeviceMasterModel] = []

    for index, bed in enumerate(beds, start=1):
        device = DeviceMasterModel(
            device_type="MONITOR",
            manufacturer="Generic",
            model="Bedside Monitor",
            serial=f"MONITOR-SEED-{index:03d}",
            bed_id=bed.id,
            ip_address=f"192.168.1.{100 + index}",
            status="ONLINE",
        )

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
    patients: list[PatientModel] = []

    for index, payload in enumerate(PATIENT_PAYLOADS):
        patient = PatientModel(
            mrn=payload["mrn"],
            cr_number=payload["cr_number"],
            contact_number=payload["contact_number"],
            name=payload["name"],
            age=payload["age"],
            gender=payload["gender"],
            bed_id=beds[index].id,
            diagnosis=payload["diagnosis"],
            weight=payload["weight"],
            height=payload["height"],
            blood_group=payload["blood_group"],
            doctor=payload["doctor"],
            admission_time=utc_now() - timedelta(days=index),
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
    doctor = next(user for user in users if user.user_id == "doctor")
    nurse = next(user for user in users if user.user_id == "nurse")

    for patient in patients:
        db.add(PatientStaffAssignmentModel(
            patient_id=patient.id,
            user_id=doctor.id,
            assignment_type="DOCTOR",
            assigned_at=utc_now(),
            ended_at=None,
            is_active=True,
        ))
        db.add(PatientStaffAssignmentModel(
            patient_id=patient.id,
            user_id=nurse.id,
            assignment_type="NURSE",
            assigned_at=utc_now(),
            ended_at=None,
            is_active=True,
        ))


def seed_vitals(
    db: Session,
    patients: list[PatientModel],
) -> None:
    """Seed 24 hourly vitals per patient so the flowsheet tab is fully populated."""
    for patient in patients:
        base_hr = random.randint(75, 115)
        base_bp_sys = random.randint(100, 145)
        base_bp_dia = random.randint(62, 90)
        base_spo2 = random.randint(90, 99)
        base_temp = round(random.uniform(98.0, 101.5), 1)
        base_rr = random.randint(14, 26)

        now = utc_now()

        for hour_offset in range(24):
            recorded_at = now - timedelta(hours=23 - hour_offset)
            db.add(VitalModel(
                patient_id=patient.id,
                hr=base_hr + random.randint(-8, 8),
                bp_sys=base_bp_sys + random.randint(-10, 10),
                bp_dia=base_bp_dia + random.randint(-5, 5),
                spo2=min(100, base_spo2 + random.randint(-3, 2)),
                temp=round(base_temp + random.uniform(-0.4, 0.4), 1),
                rr=base_rr + random.randint(-3, 3),
                recorded_at=recorded_at,
            ))

        db.add(LatestVitalModel(
            patient_id=patient.id,
            bed_id=patient.bed_id,
            device_id=None,
            hr=base_hr,
            bp_sys=base_bp_sys,
            bp_dia=base_bp_dia,
            spo2=base_spo2,
            temp=base_temp,
            rr=base_rr,
            status="LIVE",
            recorded_at=utc_now(),
            updated_at=utc_now(),
        ))


def seed_timeline(
    db: Session,
    patients: list[PatientModel],
) -> None:
    for patient in patients:
        db.add(TimelineEventModel(
            patient_id=patient.id,
            type=TimelineEventType.STATUS_CHANGED.value,
            event=f"{patient.name} admitted to ICU — diagnosis: {patient.diagnosis}",
            created_at=patient.admission_time,
        ))
        db.add(TimelineEventModel(
            patient_id=patient.id,
            type=TimelineEventType.DEVICE_ASSIGNED.value,
            event=f"Bedside monitor assigned to {patient.name}",
            created_at=patient.admission_time + timedelta(minutes=15),
        ))
        db.add(TimelineEventModel(
            patient_id=patient.id,
            type=TimelineEventType.NOTE_ADDED.value,
            event=f"Initial ICU assessment and progress note documented for {patient.name}",
            created_at=patient.admission_time + timedelta(hours=1),
        ))


def seed_clinical_notes(
    db: Session,
    patients: list[PatientModel],
    doctor: UserModel,
    nurse: UserModel,
) -> None:
    for patient, payload in zip(patients, PATIENT_PAYLOADS):
        for note_type, note_text in payload["notes"]:
            author = nurse if note_type == ClinicalNoteType.NURSING else doctor
            author_name = f"{author.first_name} {author.last_name}"
            db.add(ClinicalNoteModel(
                patient_id=patient.id,
                author_id=author.id,
                author_name=author_name,
                note_type=note_type,
                note_text=note_text,
                created_at=utc_now() - timedelta(hours=random.randint(1, 6)),
                updated_at=utc_now(),
            ))


def seed_ventilator_settings(
    db: Session,
    patients: list[PatientModel],
) -> None:
    for patient, payload in zip(patients, PATIENT_PAYLOADS):
        v = payload["ventilator"]
        db.add(VentilatorSettingModel(
            patient_id=patient.id,
            mode=v["mode"],
            fio2=v["fio2"],
            peep=v["peep"],
            set_rr=v["set_rr"],
            tidal_volume=v["tidal_volume"],
            recorded_at=utc_now() - timedelta(hours=1),
        ))


def seed_lab_results(
    db: Session,
    patients: list[PatientModel],
) -> None:
    for patient, payload in zip(patients, PATIENT_PAYLOADS):
        lab = payload["labs"]
        db.add(LabResultModel(
            patient_id=patient.id,
            ph=lab["ph"],
            pao2=lab["pao2"],
            paco2=lab["paco2"],
            hco3=lab["hco3"],
            rbs=lab["rbs"],
            recorded_at=utc_now() - timedelta(hours=2),
        ))


def seed_fluid_balance(
    db: Session,
    patients: list[PatientModel],
) -> None:
    now = utc_now()
    for patient in patients:
        db.add(FluidBalanceModel(
            patient_id=patient.id,
            in_ml=500.0,
            out_ml=0.0,
            source="IV Fluids",
            recorded_at=now.replace(hour=6, minute=0, second=0, microsecond=0),
        ))
        db.add(FluidBalanceModel(
            patient_id=patient.id,
            in_ml=200.0,
            out_ml=0.0,
            source="Oral / NG",
            recorded_at=now.replace(hour=9, minute=0, second=0, microsecond=0),
        ))
        db.add(FluidBalanceModel(
            patient_id=patient.id,
            in_ml=0.0,
            out_ml=350.0,
            source="Urine",
            recorded_at=now.replace(hour=12, minute=0, second=0, microsecond=0),
        ))
        db.add(FluidBalanceModel(
            patient_id=patient.id,
            in_ml=300.0,
            out_ml=0.0,
            source="IV Medications",
            recorded_at=now.replace(hour=14, minute=0, second=0, microsecond=0),
        ))
        db.add(FluidBalanceModel(
            patient_id=patient.id,
            in_ml=0.0,
            out_ml=200.0,
            source="Drain / Other",
            recorded_at=now.replace(hour=16, minute=0, second=0, microsecond=0),
        ))


def seed_medication_orders(
    db: Session,
    patients: list[PatientModel],
) -> None:
    for patient, payload in zip(patients, PATIENT_PAYLOADS):
        for order in payload["medications"]:
            db.add(MedicationOrderModel(
                patient_id=patient.id,
                drug_name=order["drug_name"],
                order_type=order["order_type"],
                dose=order["dose"],
                route=order["route"],
                schedule=order["schedule"],
                status=order["status"],
                rate_ml_hr=order.get("rate_ml_hr"),
                remaining_vol_ml=order.get("remaining_vol_ml"),
                est_end_time=(
                    utc_now() + timedelta(hours=random.randint(8, 20))
                    if order.get("rate_ml_hr") and order["status"] == "Running"
                    else None
                ),
                created_at=utc_now() - timedelta(hours=random.randint(1, 8)),
                updated_at=utc_now(),
            ))


def seed_alarms(
    db: Session,
    patients: list[PatientModel],
    beds: list[BedMasterModel],
    devices: list[DeviceMasterModel],
) -> None:
    severities = ["Info", "Warning", "Critical"]

    for index, patient in enumerate(patients):
        severity = severities[index % len(severities)]

        db.add(AlarmModel(
            timestamp=utc_now(),
            patient_id=patient.id,
            patient_name=patient.name,
            bed_id=beds[index].bed_id,
            device=devices[index].model,
            message=f"{severity} alert generated for {patient.name}",
            severity=severity,
            acknowledged=severity == "Info",
            silenced=False,
            escalated=severity == "Critical",
            acknowledged_by="nurse" if severity == "Info" else None,
            silenced_by=None,
            silence_until=None,
            escalated_by="system" if severity == "Critical" else None,
            escalate_to="doctor" if severity == "Critical" else None,
        ))


def main() -> None:
    db = SessionLocal()

    try:
        print("Clearing existing dev seed data...")
        clear_seed_data(db)

        print("Creating permissions...")
        permissions = seed_permissions(db)

        print("Creating roles...")
        roles = seed_roles(db)

        print("Assigning role permissions...")
        seed_role_permissions(db=db, roles=roles, permissions=permissions)

        print("Creating hospital and units...")
        hospital, units = seed_hospital_and_units(db)

        print("Creating ICU units...")
        icu_units = seed_icu_units(db)

        print("Creating beds...")
        beds = seed_beds(db=db, icu_units=icu_units)

        print("Creating device masters...")
        devices = seed_device_masters(db=db, beds=beds)

        print("Creating users...")
        users = seed_users(
            db=db,
            roles=roles,
            hospital=hospital,
            unit=units[0],
        )

        print("Creating patients...")
        patients = seed_patients(db=db, hospital=hospital, beds=beds)

        print("Creating staff assignments...")
        seed_patient_staff_assignments(db=db, patients=patients, users=users)

        print("Seeding 24h vitals (flowsheet)...")
        seed_vitals(db=db, patients=patients)

        print("Creating timeline events...")
        seed_timeline(db=db, patients=patients)

        print("Creating clinical notes...")
        doctor = next(u for u in users if u.user_id == "doctor")
        nurse = next(u for u in users if u.user_id == "nurse")
        seed_clinical_notes(db=db, patients=patients, doctor=doctor, nurse=nurse)

        print("Creating alarms...")
        seed_alarms(db=db, patients=patients, beds=beds, devices=devices)

        print("Creating ventilator settings...")
        seed_ventilator_settings(db=db, patients=patients)

        print("Creating lab results...")
        seed_lab_results(db=db, patients=patients)

        print("Creating fluid balance records...")
        seed_fluid_balance(db=db, patients=patients)

        print("Creating medication orders...")
        seed_medication_orders(db=db, patients=patients)

        db.commit()

        print("\nSeeding complete.")
        print(f"  Patients : {len(patients)}")
        print(f"  Vitals   : {len(patients) * 24} readings (24h flowsheet)")
        print(f"  Notes    : {sum(len(p['notes']) for p in PATIENT_PAYLOADS)}")
        print(f"  Meds     : {sum(len(p['medications']) for p in PATIENT_PAYLOADS)}")
        print("\nDev login users:")

        for user in SEED_USERS:
            print(f"  {user['email']} / {user['password']} ({user['role'].value})")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
