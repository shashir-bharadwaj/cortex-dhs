"""
Dev-only seed script for Cortex ICU.

Units:
  MICU-1 — Medical ICU       — 10 patients (B1–B10)
  SICU-1 — Surgical ICU      — 8 patients  (S1–S8)
  NICU-1 — Neurological ICU  — 8 patients  (N1–N8)
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


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SEED_USERS = [
    {"user_id": "admin",  "first_name": "System", "last_name": "Admin",  "email": "admin@cortex.com",  "password": "admin",  "role": UserRole.ADMIN,  "shift": ShiftType.MORNING},
    {"user_id": "doctor", "first_name": "John",   "last_name": "Doctor", "email": "doctor@cortex.com", "password": "doctor", "role": UserRole.DOCTOR, "shift": ShiftType.MORNING},
    {"user_id": "nurse",  "first_name": "Jane",   "last_name": "Nurse",  "email": "nurse@cortex.com",  "password": "nurse",  "role": UserRole.NURSE,  "shift": ShiftType.MORNING},
]

HOSPITAL_NAME = "Apollo Main Hospital"
HOSPITAL_CODE = "APOLLO-BLR-001"
UNIT_NAMES    = ["MICU", "SICU", "NICU"]
SEED_ICU_NAMES = ["MICU-1", "SICU-1", "NICU-1"]

MICU_BED_IDS = ["B1",  "B2",  "B3",  "B4",  "B5",  "B6",  "B7",  "B8",  "B9",  "B10"]
SICU_BED_IDS = ["S1",  "S2",  "S3",  "S4",  "S5",  "S6",  "S7",  "S8"]
NICU_BED_IDS = ["N1",  "N2",  "N3",  "N4",  "N5",  "N6",  "N7",  "N8"]
ALL_BED_IDS  = MICU_BED_IDS + SICU_BED_IDS + NICU_BED_IDS

MICU_DEVICE_SERIALS = [f"MICU-MONITOR-{i:03d}" for i in range(1, 11)]
SICU_DEVICE_SERIALS = [f"SICU-MONITOR-{i:03d}" for i in range(1, 9)]
NICU_DEVICE_SERIALS = [f"NICU-MONITOR-{i:03d}" for i in range(1, 9)]
ALL_DEVICE_SERIALS  = MICU_DEVICE_SERIALS + SICU_DEVICE_SERIALS + NICU_DEVICE_SERIALS

PERMISSION_MODULES = [
    PermissionModule.HOSPITALS, PermissionModule.PATIENTS, PermissionModule.VITALS,
    PermissionModule.TIMELINE,  PermissionModule.ALARMS,   PermissionModule.ICU_MANAGEMENT,
    PermissionModule.BED_MANAGEMENT, PermissionModule.DEVICE_MANAGEMENT,
    PermissionModule.MANAGE_USERS,   PermissionModule.DASHBOARD,
]
PERMISSION_ACTIONS = [
    PermissionAction.VIEW, PermissionAction.CREATE, PermissionAction.MODIFY,
    PermissionAction.CANCEL, PermissionAction.DELETE,
]

# ---------------------------------------------------------------------------
# Patient payloads
# ---------------------------------------------------------------------------

MICU_PATIENT_PAYLOADS = [
    {
        "mrn": "MRN-100001", "cr_number": "CR-2026-0001", "contact_number": "9876543201",
        "name": "Rahul Sharma", "age": 45, "gender": Gender.MALE,
        "diagnosis": "Pneumonia", "weight": 72.5, "height": 171.0, "blood_group": "O+",
        "doctor": "Dr. Meera Nair",
        "history": ["Admitted with respiratory distress", "History of smoking"],
        "comorbidities": ["Hypertension"],
        "ventilator": {"mode": "PSV",   "fio2": 0.35, "peep": 5.0,  "set_rr": 14, "tidal_volume": 460.0},
        "labs": {"ph": 7.38, "pao2": 85.0, "paco2": 43.0, "hco3": 24.0, "rbs": 140.0},
        "medications": [
            {"drug_name": "Piperacillin-Tazobactam", "order_type": "STAT",     "dose": "4.5g",   "route": "IV",      "schedule": "Q8H",          "status": "Running", "rate_ml_hr": 10.0, "remaining_vol_ml": 90.0},
            {"drug_name": "Paracetamol",              "order_type": "PRN",      "dose": "500mg",  "route": "Oral",    "schedule": "Q6H",          "status": "Given"},
            {"drug_name": "Pantoprazole",             "order_type": "STAT",     "dose": "40mg",   "route": "IV",      "schedule": "OD",           "status": "Pending"},
            {"drug_name": "Salbutamol Nebulisation",  "order_type": "PRN",      "dose": "2.5mg",  "route": "Inhaled", "schedule": "Q4H",          "status": "Given"},
            {"drug_name": "Enoxaparin",               "order_type": "STAT",     "dose": "40mg",   "route": "SC",      "schedule": "OD",           "status": "Pending"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Patient admitted with community-acquired pneumonia. SpO2 88% on RA. Started on IV antibiotics and supplemental oxygen. CXR shows bilateral infiltrates."),
            (ClinicalNoteType.NURSING,  "Patient cooperative. Repositioned Q2H. Oral care done. IV line patent. O2 therapy maintained at 6L/min via face mask."),
        ],
    },
    {
        "mrn": "MRN-100002", "cr_number": "CR-2026-0002", "contact_number": "9876543202",
        "name": "Ananya Rao", "age": 52, "gender": Gender.FEMALE,
        "diagnosis": "Sepsis", "weight": 64.0, "height": 164.0, "blood_group": "A+",
        "doctor": "Dr. Arjun Menon",
        "history": ["Transferred from emergency ward", "Source: UTI"],
        "comorbidities": ["Diabetes"],
        "ventilator": {"mode": "AC/VC", "fio2": 0.50, "peep": 6.0,  "set_rr": 16, "tidal_volume": 420.0},
        "labs": {"ph": 7.32, "pao2": 72.0, "paco2": 48.0, "hco3": 22.0, "rbs": 210.0},
        "medications": [
            {"drug_name": "Meropenem",       "order_type": "STAT",     "dose": "1g",        "route": "IV", "schedule": "Q8H",          "status": "Running", "rate_ml_hr": 8.0, "remaining_vol_ml": 60.0},
            {"drug_name": "Noradrenaline",   "order_type": "Infusion", "dose": "4mg/50ml",  "route": "IV", "schedule": "Titrate",      "status": "Running", "rate_ml_hr": 5.0, "remaining_vol_ml": 35.0},
            {"drug_name": "Insulin Infusion","order_type": "Infusion", "dose": "50U/50ml",  "route": "IV", "schedule": "Sliding Scale","status": "Running", "rate_ml_hr": 3.0, "remaining_vol_ml": 40.0},
            {"drug_name": "Hydrocortisone",  "order_type": "STAT",     "dose": "100mg",     "route": "IV", "schedule": "Q8H",          "status": "Pending"},
            {"drug_name": "Pantoprazole",    "order_type": "STAT",     "dose": "40mg",      "route": "IV", "schedule": "BD",           "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Sepsis secondary to UTI. Blood cultures sent. Started on broad-spectrum antibiotics. On vasopressor support. Lactate 4.2 mmol/L."),
            (ClinicalNoteType.NURSING,  "Patient intubated and mechanically ventilated. Hourly UO monitoring. Foley catheter in situ. Sedation: Propofol 10ml/hr."),
            (ClinicalNoteType.ORDER,    "Blood cultures x2, urine C&S, CBC, LFT, RFT, Procalcitonin stat."),
        ],
    },
    {
        "mrn": "MRN-100003", "cr_number": "CR-2026-0003", "contact_number": "9876543203",
        "name": "Vikram Mehta", "age": 61, "gender": Gender.MALE,
        "diagnosis": "Post cardiac arrest monitoring", "weight": 78.0, "height": 176.0, "blood_group": "B+",
        "doctor": "Dr. Kavita Rao",
        "history": ["Witnessed VF arrest", "Bystander CPR performed", "ROSC after 12 min"],
        "comorbidities": ["Coronary artery disease"],
        "ventilator": {"mode": "AC/VC", "fio2": 0.40, "peep": 5.0,  "set_rr": 14, "tidal_volume": 520.0},
        "labs": {"ph": 7.29, "pao2": 82.0, "paco2": 46.0, "hco3": 21.0, "rbs": 175.0},
        "medications": [
            {"drug_name": "Amiodarone",  "order_type": "Infusion", "dose": "300mg/50ml",  "route": "IV", "schedule": "Maintenance",      "status": "Running", "rate_ml_hr": 4.0,  "remaining_vol_ml": 32.0},
            {"drug_name": "Heparin",     "order_type": "Infusion", "dose": "25000U/50ml", "route": "IV", "schedule": "Titrate APTT",     "status": "Running", "rate_ml_hr": 3.0,  "remaining_vol_ml": 45.0},
            {"drug_name": "Aspirin",     "order_type": "STAT",     "dose": "75mg",        "route": "Oral","schedule": "OD",              "status": "Given"},
            {"drug_name": "Atorvastatin","order_type": "STAT",     "dose": "40mg",        "route": "Oral","schedule": "OD",              "status": "Pending"},
            {"drug_name": "Propofol",    "order_type": "Infusion", "dose": "200mg/20ml",  "route": "IV", "schedule": "Titrate sedation", "status": "Running", "rate_ml_hr": 10.0, "remaining_vol_ml": 15.0},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Post VF arrest. Targeted temperature management initiated. Target temp 36°C. Echo ordered — EF 30%."),
            (ClinicalNoteType.NURSING,  "Cooling blanket in situ. Core temp 36.2°C. Continuous EEG monitoring. Sedation maintained."),
        ],
    },
    {
        "mrn": "MRN-100004", "cr_number": "CR-2026-0004", "contact_number": "9876543204",
        "name": "Priya Nair", "age": 38, "gender": Gender.FEMALE,
        "diagnosis": "ARDS", "weight": 58.0, "height": 160.0, "blood_group": "AB+",
        "doctor": "Dr. V. Pillai",
        "history": ["Severe hypoxia on admission", "COVID-19 associated ARDS"],
        "comorbidities": ["Asthma"],
        "ventilator": {"mode": "AC/PC", "fio2": 0.70, "peep": 10.0, "set_rr": 18, "tidal_volume": 350.0},
        "labs": {"ph": 7.26, "pao2": 60.0, "paco2": 55.0, "hco3": 19.0, "rbs": 132.0},
        "medications": [
            {"drug_name": "Cisatracurium",  "order_type": "Infusion", "dose": "200mg/50ml", "route": "IV", "schedule": "Titrate TOF", "status": "Running", "rate_ml_hr": 6.0, "remaining_vol_ml": 28.0},
            {"drug_name": "Noradrenaline",  "order_type": "Infusion", "dose": "4mg/50ml",   "route": "IV", "schedule": "Titrate MAP", "status": "Running", "rate_ml_hr": 4.0, "remaining_vol_ml": 20.0},
            {"drug_name": "Dexamethasone",  "order_type": "STAT",     "dose": "8mg",        "route": "IV", "schedule": "OD",          "status": "Given"},
            {"drug_name": "Enoxaparin",     "order_type": "STAT",     "dose": "60mg",       "route": "SC", "schedule": "BD",          "status": "Pending"},
            {"drug_name": "Pantoprazole",   "order_type": "STAT",     "dose": "40mg",       "route": "IV", "schedule": "OD",          "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS,  "Severe ARDS — P/F ratio 85. Prone positioning initiated for 16 hours. Low tidal volume ventilation."),
            (ClinicalNoteType.NURSING,   "Prone position secured. Pressure area care done. ETT ties checked. Suction Q2H."),
            (ClinicalNoteType.HANDOVER,  "Patient critically ill. Prone ongoing. Vasopressor stable. Family counselled."),
        ],
    },
    {
        "mrn": "MRN-100005", "cr_number": "CR-2026-0005", "contact_number": "9876543205",
        "name": "Arjun Reddy", "age": 70, "gender": Gender.MALE,
        "diagnosis": "Acute Kidney Injury", "weight": 80.0, "height": 174.0, "blood_group": "O-",
        "doctor": "Dr. Sana Khan",
        "history": ["Low urine output and hypotension", "CKD stage 3 at baseline"],
        "comorbidities": ["Chronic kidney disease"],
        "ventilator": {"mode": "CPAP",  "fio2": 0.30, "peep": 4.0,  "set_rr": 12, "tidal_volume": 480.0},
        "labs": {"ph": 7.34, "pao2": 90.0, "paco2": 42.0, "hco3": 21.0, "rbs": 160.0},
        "medications": [
            {"drug_name": "Furosemide",         "order_type": "Infusion", "dose": "500mg/50ml",    "route": "IV", "schedule": "Titrate UO",  "status": "Running", "rate_ml_hr": 5.0, "remaining_vol_ml": 38.0},
            {"drug_name": "Sodium Bicarbonate", "order_type": "Infusion", "dose": "100 mEq/500ml", "route": "IV", "schedule": "Over 4 hrs",  "status": "Completed"},
            {"drug_name": "Calcium Gluconate",  "order_type": "STAT",     "dose": "1g",            "route": "IV", "schedule": "Immediate",   "status": "Given"},
            {"drug_name": "Erythropoietin",     "order_type": "STAT",     "dose": "4000 IU",       "route": "SC", "schedule": "TIW",         "status": "Pending"},
            {"drug_name": "Pantoprazole",       "order_type": "STAT",     "dose": "40mg",          "route": "IV", "schedule": "OD",          "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "AKI stage 3. UO 15ml/hr. Creatinine 6.8 mg/dL, K+ 5.8. CRRT considered if no improvement. Nephrology consulted."),
            (ClinicalNoteType.NURSING,  "Strict fluid balance hourly. Renal diet. IV access bilateral. Weight 80.2 kg this morning."),
        ],
    },
    {
        "mrn": "MRN-100006", "cr_number": "CR-2026-0006", "contact_number": "9876543206",
        "name": "Sneha Kapoor", "age": 47, "gender": Gender.FEMALE,
        "diagnosis": "Septic Shock", "weight": 62.0, "height": 162.0, "blood_group": "A-",
        "doctor": "Dr. Arjun Menon",
        "history": ["Started on vasopressor support", "Source: Abdominal (post-op)"],
        "comorbidities": ["Diabetes", "Hypothyroidism"],
        "ventilator": {"mode": "AC/VC", "fio2": 0.55, "peep": 7.0,  "set_rr": 16, "tidal_volume": 410.0},
        "labs": {"ph": 7.28, "pao2": 68.0, "paco2": 50.0, "hco3": 20.0, "rbs": 240.0},
        "medications": [
            {"drug_name": "Vasopressin",     "order_type": "Infusion", "dose": "20U/50ml",   "route": "IV", "schedule": "0.03 U/min",   "status": "Running", "rate_ml_hr": 4.5,  "remaining_vol_ml": 22.0},
            {"drug_name": "Noradrenaline",   "order_type": "Infusion", "dose": "8mg/50ml",   "route": "IV", "schedule": "Titrate MAP",  "status": "Running", "rate_ml_hr": 8.0,  "remaining_vol_ml": 18.0},
            {"drug_name": "Meropenem",       "order_type": "STAT",     "dose": "2g",         "route": "IV", "schedule": "Q8H extended", "status": "Running", "rate_ml_hr": 12.0, "remaining_vol_ml": 80.0},
            {"drug_name": "Insulin Infusion","order_type": "Infusion", "dose": "50U/50ml",   "route": "IV", "schedule": "Sliding Scale","status": "Running", "rate_ml_hr": 2.0,  "remaining_vol_ml": 42.0},
            {"drug_name": "Levothyroxine",   "order_type": "STAT",     "dose": "100mcg",     "route": "IV", "schedule": "OD",           "status": "Pending"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Post-op day 2 septic shock. Two vasopressors running. Lactate 5.1. CT Abdomen ordered for possible anastomotic leak."),
            (ClinicalNoteType.NURSING,  "MAP 62 mmHg. Foley 20ml/hr. Blood glucose Q1H — 230, insulin adjusted."),
        ],
    },
    {
        "mrn": "MRN-100007", "cr_number": "CR-2026-0007", "contact_number": "9876543207",
        "name": "Karthik Iyer", "age": 59, "gender": Gender.MALE,
        "diagnosis": "Stroke", "weight": 74.0, "height": 172.0, "blood_group": "B-",
        "doctor": "Dr. Kavita Rao",
        "history": ["Right-sided weakness with aphasia", "NIHSS 18 on admission"],
        "comorbidities": ["Hypertension", "Dyslipidemia"],
        "ventilator": {"mode": "PSV",   "fio2": 0.28, "peep": 4.0,  "set_rr": 12, "tidal_volume": 500.0},
        "labs": {"ph": 7.42, "pao2": 96.0, "paco2": 39.0, "hco3": 25.0, "rbs": 155.0},
        "medications": [
            {"drug_name": "Alteplase",    "order_type": "STAT", "dose": "67mg",  "route": "IV",   "schedule": "Immediate (done)", "status": "Completed"},
            {"drug_name": "Aspirin",      "order_type": "STAT", "dose": "300mg", "route": "Oral", "schedule": "OD",               "status": "Given"},
            {"drug_name": "Amlodipine",   "order_type": "STAT", "dose": "5mg",   "route": "Oral", "schedule": "OD",               "status": "Given"},
            {"drug_name": "Atorvastatin", "order_type": "STAT", "dose": "80mg",  "route": "Oral", "schedule": "OD",               "status": "Pending"},
            {"drug_name": "Labetalol",    "order_type": "PRN",  "dose": "20mg",  "route": "IV",   "schedule": "PRN SBP >180",     "status": "Pending"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Ischemic stroke left MCA. Thrombolysis with Alteplase done. No haemorrhagic transformation on repeat CT."),
            (ClinicalNoteType.NURSING,  "Neuro obs Q1H: GCS 11. Right arm power 1/5. Aspiration precautions. HOB 30°."),
        ],
    },
    {
        "mrn": "MRN-100008", "cr_number": "CR-2026-0008", "contact_number": "9876543208",
        "name": "Neha Verma", "age": 66, "gender": Gender.FEMALE,
        "diagnosis": "COPD Exacerbation", "weight": 55.0, "height": 158.0, "blood_group": "O+",
        "doctor": "Dr. Meera Nair",
        "history": ["Acute breathlessness", "COPD GOLD stage 3"],
        "comorbidities": ["COPD"],
        "ventilator": {"mode": "SIMV",  "fio2": 0.32, "peep": 5.0,  "set_rr": 14, "tidal_volume": 380.0},
        "labs": {"ph": 7.31, "pao2": 58.0, "paco2": 62.0, "hco3": 28.0, "rbs": 98.0},
        "medications": [
            {"drug_name": "Salbutamol Nebulisation",  "order_type": "PRN",  "dose": "5mg",      "route": "Inhaled", "schedule": "Q4H",      "status": "Given"},
            {"drug_name": "Ipratropium Nebulisation", "order_type": "PRN",  "dose": "0.5mg",    "route": "Inhaled", "schedule": "Q6H",      "status": "Given"},
            {"drug_name": "Methylprednisolone",       "order_type": "STAT", "dose": "40mg",     "route": "IV",      "schedule": "OD",       "status": "Running", "rate_ml_hr": 10.0, "remaining_vol_ml": 40.0},
            {"drug_name": "Doxycycline",              "order_type": "STAT", "dose": "200mg",    "route": "Oral",    "schedule": "OD",       "status": "Given"},
            {"drug_name": "Theophylline",             "order_type": "Infusion", "dose": "250mg/500ml", "route": "IV", "schedule": "Over 24h", "status": "Running", "rate_ml_hr": 21.0, "remaining_vol_ml": 300.0},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "COPD exacerbation with type 2 RF. pCO2 62 — on NIV BiPAP IPAP 14/EPAP 4. ABG improving. Aim to avoid intubation."),
            (ClinicalNoteType.NURSING,  "NIV mask fit checked. Barrier cream applied. Chest physio done."),
        ],
    },
    {
        "mrn": "MRN-100009", "cr_number": "CR-2026-0009", "contact_number": "9876543209",
        "name": "Rohan Malhotra", "age": 54, "gender": Gender.MALE,
        "diagnosis": "Myocardial Infarction", "weight": 82.0, "height": 178.0, "blood_group": "AB-",
        "doctor": "Dr. A. Mehta",
        "history": ["Chest pain with elevated troponin", "STEMI LAD occlusion", "Primary PCI performed"],
        "comorbidities": ["Diabetes", "Hypertension"],
        "ventilator": {"mode": "CPAP",  "fio2": 0.28, "peep": 4.0,  "set_rr": 12, "tidal_volume": 530.0},
        "labs": {"ph": 7.40, "pao2": 94.0, "paco2": 40.0, "hco3": 24.0, "rbs": 185.0},
        "medications": [
            {"drug_name": "Aspirin",      "order_type": "STAT",     "dose": "75mg",        "route": "Oral", "schedule": "OD",          "status": "Given"},
            {"drug_name": "Ticagrelor",   "order_type": "STAT",     "dose": "90mg",        "route": "Oral", "schedule": "BD",          "status": "Given"},
            {"drug_name": "Atorvastatin", "order_type": "STAT",     "dose": "80mg",        "route": "Oral", "schedule": "OD",          "status": "Given"},
            {"drug_name": "Heparin",      "order_type": "Infusion", "dose": "25000U/50ml", "route": "IV",   "schedule": "Titrate APTT","status": "Running", "rate_ml_hr": 3.0, "remaining_vol_ml": 40.0},
            {"drug_name": "Metoprolol",   "order_type": "STAT",     "dose": "25mg",        "route": "Oral", "schedule": "BD",          "status": "Pending"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "STEMI with successful primary PCI to LAD. DES deployed. Post-PCI EF 40%. Dual antiplatelet and anticoagulation started."),
            (ClinicalNoteType.NURSING,  "Groin site (right femoral) — no haematoma. Peripheral pulses intact. Ambulation restricted 6h post-procedure."),
        ],
    },
    {
        "mrn": "MRN-100010", "cr_number": "CR-2026-0010", "contact_number": "9876543210",
        "name": "Meera Joshi", "age": 73, "gender": Gender.FEMALE,
        "diagnosis": "Multi Organ Dysfunction", "weight": 60.0, "height": 159.0, "blood_group": "A+",
        "doctor": "Dr. V. Pillai",
        "history": ["Clinical deterioration from ward", "Background CLD Child-Pugh C"],
        "comorbidities": ["Chronic liver disease"],
        "ventilator": {"mode": "AC/VC", "fio2": 0.60, "peep": 8.0,  "set_rr": 16, "tidal_volume": 360.0},
        "labs": {"ph": 7.24, "pao2": 64.0, "paco2": 50.0, "hco3": 18.0, "rbs": 70.0},
        "medications": [
            {"drug_name": "Noradrenaline", "order_type": "Infusion", "dose": "4mg/50ml",   "route": "IV",   "schedule": "Titrate MAP", "status": "Running", "rate_ml_hr": 7.0, "remaining_vol_ml": 25.0},
            {"drug_name": "Terlipressin",  "order_type": "Infusion", "dose": "1mg/50ml",   "route": "IV",   "schedule": "Q6H",         "status": "Running", "rate_ml_hr": 8.0, "remaining_vol_ml": 30.0},
            {"drug_name": "Albumin",       "order_type": "Infusion", "dose": "20g/100ml",  "route": "IV",   "schedule": "BD",          "status": "Given"},
            {"drug_name": "Rifaximin",     "order_type": "STAT",     "dose": "550mg",      "route": "Oral", "schedule": "BD",          "status": "Pending"},
            {"drug_name": "Lactulose",     "order_type": "STAT",     "dose": "30ml",       "route": "Oral", "schedule": "TDS",         "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS,  "MODS — liver (Child-Pugh C), renal (Cr 3.2), respiratory failure (FiO2 0.6). Goals of care discussed with family."),
            (ClinicalNoteType.NURSING,   "RASS -3. Pressure care Q2H. NG tube in situ. Enteral feed at 20ml/hr. Family at bedside."),
            (ClinicalNoteType.HANDOVER,  "Critical — MODS. Full active treatment per family wishes. Palliative referral declined. Senior review AM."),
        ],
    },
]

SICU_PATIENT_PAYLOADS = [
    {
        "mrn": "MRN-200001", "cr_number": "CR-2026-1001", "contact_number": "9876540001",
        "name": "Ramesh Kumar", "age": 58, "gender": Gender.MALE,
        "diagnosis": "Post-op Bowel Resection", "weight": 70.0, "height": 168.0, "blood_group": "O+",
        "doctor": "Dr. Suresh Nair",
        "history": ["Colorectal carcinoma sigmoid colon", "Hartmann's procedure performed"],
        "comorbidities": ["Hypertension", "Diabetes"],
        "ventilator": {"mode": "SIMV",  "fio2": 0.35, "peep": 5.0,  "set_rr": 12, "tidal_volume": 460.0},
        "labs": {"ph": 7.36, "pao2": 88.0, "paco2": 42.0, "hco3": 23.0, "rbs": 145.0},
        "medications": [
            {"drug_name": "Morphine",          "order_type": "Infusion", "dose": "30mg/30ml",  "route": "IV",   "schedule": "Titrate pain",  "status": "Running", "rate_ml_hr": 2.0, "remaining_vol_ml": 22.0},
            {"drug_name": "Cefazolin",         "order_type": "STAT",     "dose": "1g",         "route": "IV",   "schedule": "Q8H",           "status": "Given"},
            {"drug_name": "Metronidazole",     "order_type": "STAT",     "dose": "500mg",      "route": "IV",   "schedule": "Q8H",           "status": "Running", "rate_ml_hr": 8.0, "remaining_vol_ml": 50.0},
            {"drug_name": "Ondansetron",       "order_type": "PRN",      "dose": "4mg",        "route": "IV",   "schedule": "Q8H PRN",       "status": "Given"},
            {"drug_name": "Enoxaparin",        "order_type": "STAT",     "dose": "40mg",       "route": "SC",   "schedule": "OD",            "status": "Pending"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Post Hartmann's day 1. Stoma output 300ml/8h (dark green). Wound dry and intact. NG tube draining. Awaiting return of bowel sounds."),
            (ClinicalNoteType.NURSING,  "Patient on PCA morphine — pain score 4/10. Stoma bag changed. Wound dressing intact. Chest physio performed."),
        ],
    },
    {
        "mrn": "MRN-200002", "cr_number": "CR-2026-1002", "contact_number": "9876540002",
        "name": "Lakshmi Devi", "age": 64, "gender": Gender.FEMALE,
        "diagnosis": "Post-op CABG", "weight": 65.0, "height": 155.0, "blood_group": "B+",
        "doctor": "Dr. A. Mehta",
        "history": ["Triple vessel CAD", "Off-pump CABG x3 grafts performed yesterday"],
        "comorbidities": ["Hypertension", "Dyslipidemia"],
        "ventilator": {"mode": "PSV",   "fio2": 0.40, "peep": 5.0,  "set_rr": 12, "tidal_volume": 420.0},
        "labs": {"ph": 7.38, "pao2": 90.0, "paco2": 41.0, "hco3": 24.0, "rbs": 120.0},
        "medications": [
            {"drug_name": "Noradrenaline",   "order_type": "Infusion", "dose": "4mg/50ml",   "route": "IV",   "schedule": "Titrate MAP>65", "status": "Running", "rate_ml_hr": 3.0, "remaining_vol_ml": 38.0},
            {"drug_name": "Aspirin",         "order_type": "STAT",     "dose": "100mg",      "route": "Oral", "schedule": "OD",             "status": "Given"},
            {"drug_name": "Atorvastatin",    "order_type": "STAT",     "dose": "40mg",       "route": "Oral", "schedule": "OD",             "status": "Given"},
            {"drug_name": "Bisoprolol",      "order_type": "STAT",     "dose": "2.5mg",      "route": "Oral", "schedule": "OD",             "status": "Pending"},
            {"drug_name": "Amiodarone",      "order_type": "Infusion", "dose": "150mg/50ml", "route": "IV",   "schedule": "Prophylaxis",    "status": "Running", "rate_ml_hr": 5.0, "remaining_vol_ml": 30.0},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Post CABG day 1. Haemodynamically stable on low-dose vasopressor. Chest drains output 50ml/h (reducing). Plan to extubate if FiO2 <0.35 maintained."),
            (ClinicalNoteType.NURSING,  "Mediastinal and pleural drains patent. ECG SR 78/min. Surgical wound: sternal and leg harvest sites intact."),
        ],
    },
    {
        "mrn": "MRN-200003", "cr_number": "CR-2026-1003", "contact_number": "9876540003",
        "name": "Suresh Pillai", "age": 34, "gender": Gender.MALE,
        "diagnosis": "Abdominal Trauma", "weight": 76.0, "height": 175.0, "blood_group": "O-",
        "doctor": "Dr. Suresh Nair",
        "history": ["Road traffic accident", "Grade IV splenic laceration", "Emergency splenectomy done"],
        "comorbidities": [],
        "ventilator": {"mode": "AC/VC", "fio2": 0.45, "peep": 6.0,  "set_rr": 14, "tidal_volume": 500.0},
        "labs": {"ph": 7.33, "pao2": 80.0, "paco2": 44.0, "hco3": 22.0, "rbs": 130.0},
        "medications": [
            {"drug_name": "Piperacillin-Tazobactam", "order_type": "STAT",     "dose": "4.5g",       "route": "IV", "schedule": "Q6H",        "status": "Running", "rate_ml_hr": 10.0, "remaining_vol_ml": 70.0},
            {"drug_name": "Tranexamic Acid",         "order_type": "Infusion", "dose": "1g/100ml",   "route": "IV", "schedule": "Over 10 min","status": "Completed"},
            {"drug_name": "Morphine",                "order_type": "Infusion", "dose": "30mg/30ml",  "route": "IV", "schedule": "Titrate",    "status": "Running", "rate_ml_hr": 3.0, "remaining_vol_ml": 18.0},
            {"drug_name": "Pneumococcal Vaccine",    "order_type": "STAT",     "dose": "0.5ml",      "route": "IM", "schedule": "Once",       "status": "Pending"},
            {"drug_name": "Pantoprazole",            "order_type": "STAT",     "dose": "40mg",       "route": "IV", "schedule": "BD",         "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Post emergency splenectomy day 1. Haemoglobin stable at 9.2 g/dL. No active bleeding. Massive transfusion protocol de-escalated."),
            (ClinicalNoteType.NURSING,  "Abdominal wound dressing intact. Two abdominal drains in situ — minimal serous output. Pain managed on morphine infusion."),
        ],
    },
    {
        "mrn": "MRN-200004", "cr_number": "CR-2026-1004", "contact_number": "9876540004",
        "name": "Divya Menon", "age": 49, "gender": Gender.FEMALE,
        "diagnosis": "Post-op Liver Resection", "weight": 58.0, "height": 158.0, "blood_group": "A+",
        "doctor": "Dr. Arjun Menon",
        "history": ["Hepatocellular carcinoma segment VI/VII", "Right hepatectomy performed"],
        "comorbidities": ["Hepatitis B"],
        "ventilator": {"mode": "PSV",   "fio2": 0.32, "peep": 5.0,  "set_rr": 12, "tidal_volume": 380.0},
        "labs": {"ph": 7.37, "pao2": 87.0, "paco2": 43.0, "hco3": 23.0, "rbs": 95.0},
        "medications": [
            {"drug_name": "Fresh Frozen Plasma",  "order_type": "Infusion", "dose": "2 units",    "route": "IV", "schedule": "PRN INR >2",  "status": "Given"},
            {"drug_name": "Vitamin K",            "order_type": "STAT",     "dose": "10mg",       "route": "IV", "schedule": "OD x3",       "status": "Given"},
            {"drug_name": "Ondansetron",          "order_type": "PRN",      "dose": "4mg",        "route": "IV", "schedule": "Q8H PRN",     "status": "Given"},
            {"drug_name": "Cefazolin",            "order_type": "STAT",     "dose": "1g",         "route": "IV", "schedule": "Q8H",         "status": "Running", "rate_ml_hr": 8.0, "remaining_vol_ml": 50.0},
            {"drug_name": "Dextrose 10%",         "order_type": "Infusion", "dose": "500ml",      "route": "IV", "schedule": "12 hrly",     "status": "Running", "rate_ml_hr": 42.0, "remaining_vol_ml": 280.0},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Post right hepatectomy day 2. INR 2.1 (improving). Bilirubin 4.2. Liver drain 80ml/h bile-stained. LFTs trending down."),
            (ClinicalNoteType.NURSING,  "Jackson-Pratt drain patent. Glucose monitoring Q2H — 92 mg/dL. Patient alert and oriented. Pain score 3/10."),
        ],
    },
    {
        "mrn": "MRN-200005", "cr_number": "CR-2026-1005", "contact_number": "9876540005",
        "name": "Ajay Singh", "age": 55, "gender": Gender.MALE,
        "diagnosis": "Post-op Thoracotomy", "weight": 68.0, "height": 170.0, "blood_group": "B-",
        "doctor": "Dr. Kavita Rao",
        "history": ["Squamous cell carcinoma right upper lobe", "Right upper lobe resection (VATS)"],
        "comorbidities": ["Smoking", "COPD"],
        "ventilator": {"mode": "SIMV",  "fio2": 0.38, "peep": 5.0,  "set_rr": 14, "tidal_volume": 440.0},
        "labs": {"ph": 7.35, "pao2": 82.0, "paco2": 45.0, "hco3": 23.0, "rbs": 115.0},
        "medications": [
            {"drug_name": "Thoracic Epidural (Bupivacaine)", "order_type": "Infusion", "dose": "0.125%/10ml",  "route": "Epidural", "schedule": "Continuous", "status": "Running", "rate_ml_hr": 6.0, "remaining_vol_ml": 80.0},
            {"drug_name": "Paracetamol",                     "order_type": "STAT",     "dose": "1g",           "route": "IV",       "schedule": "Q6H",        "status": "Given"},
            {"drug_name": "Ketorolac",                       "order_type": "PRN",      "dose": "15mg",         "route": "IV",       "schedule": "Q8H",        "status": "Pending"},
            {"drug_name": "Salbutamol Nebulisation",         "order_type": "PRN",      "dose": "2.5mg",        "route": "Inhaled",  "schedule": "Q4H",        "status": "Given"},
            {"drug_name": "Cefuroxime",                      "order_type": "STAT",     "dose": "1.5g",         "route": "IV",       "schedule": "Q8H",        "status": "Running", "rate_ml_hr": 8.0, "remaining_vol_ml": 45.0},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Post VATS day 1. Air leak from intercostal drain resolving. SpO2 94% on 2L/min O2. Chest physio Q4H. Plan: wean FiO2, remove drain when leak ceases."),
            (ClinicalNoteType.NURSING,  "Intercostal drain — moderate air leak, serosanguineous fluid 120ml/h. Epidural running — pain score 2/10. Ambulation target tomorrow."),
        ],
    },
    {
        "mrn": "MRN-200006", "cr_number": "CR-2026-1006", "contact_number": "9876540006",
        "name": "Pooja Sharma", "age": 42, "gender": Gender.FEMALE,
        "diagnosis": "Post-op Esophagectomy", "weight": 52.0, "height": 157.0, "blood_group": "A-",
        "doctor": "Dr. Arjun Menon",
        "history": ["Squamous cell carcinoma mid-esophagus", "McKeown's esophagectomy performed"],
        "comorbidities": [],
        "ventilator": {"mode": "AC/VC", "fio2": 0.45, "peep": 6.0,  "set_rr": 14, "tidal_volume": 340.0},
        "labs": {"ph": 7.36, "pao2": 85.0, "paco2": 43.0, "hco3": 23.0, "rbs": 110.0},
        "medications": [
            {"drug_name": "Fentanyl",           "order_type": "Infusion", "dose": "500mcg/50ml", "route": "IV",  "schedule": "Titrate",    "status": "Running", "rate_ml_hr": 4.0, "remaining_vol_ml": 32.0},
            {"drug_name": "Piperacillin-Tazobactam", "order_type": "STAT", "dose": "4.5g",       "route": "IV",  "schedule": "Q8H",        "status": "Running", "rate_ml_hr": 10.0, "remaining_vol_ml": 60.0},
            {"drug_name": "Pantoprazole",        "order_type": "Infusion", "dose": "80mg/50ml",  "route": "IV",  "schedule": "Continuous", "status": "Running", "rate_ml_hr": 2.0, "remaining_vol_ml": 40.0},
            {"drug_name": "Metoclopramide",      "order_type": "STAT",     "dose": "10mg",       "route": "IV",  "schedule": "Q8H",        "status": "Given"},
            {"drug_name": "Jejunal Feeding (EN)","order_type": "Infusion", "dose": "Standard formula", "route": "Jejunostomy", "schedule": "30ml/hr", "status": "Running", "rate_ml_hr": 30.0, "remaining_vol_ml": 250.0},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Post esophagectomy day 2. Anastomotic integrity leak test pending. Jejunal feeds started at 30ml/hr. No respiratory complications. Chest drains minimal."),
            (ClinicalNoteType.NURSING,  "Cervical wound clean and dry. Chest drain serous 40ml/8h. Jejunal tube patent. Oral hygiene Q2H. Sedation weaning plan in progress."),
        ],
    },
    {
        "mrn": "MRN-200007", "cr_number": "CR-2026-1007", "contact_number": "9876540007",
        "name": "Ravi Verma", "age": 29, "gender": Gender.MALE,
        "diagnosis": "Polytrauma", "weight": 74.0, "height": 178.0, "blood_group": "O+",
        "doctor": "Dr. Suresh Nair",
        "history": ["RTA — high-speed MVA", "Rib fractures R4-R7, pulmonary contusion, pelvic fracture"],
        "comorbidities": [],
        "ventilator": {"mode": "AC/PC", "fio2": 0.50, "peep": 7.0,  "set_rr": 16, "tidal_volume": 480.0},
        "labs": {"ph": 7.30, "pao2": 75.0, "paco2": 46.0, "hco3": 21.0, "rbs": 138.0},
        "medications": [
            {"drug_name": "Ketamine",              "order_type": "Infusion", "dose": "500mg/50ml",  "route": "IV",   "schedule": "Analgesia",   "status": "Running", "rate_ml_hr": 5.0, "remaining_vol_ml": 28.0},
            {"drug_name": "Piperacillin-Tazobactam","order_type": "STAT",    "dose": "4.5g",        "route": "IV",   "schedule": "Q8H",         "status": "Running", "rate_ml_hr": 10.0, "remaining_vol_ml": 80.0},
            {"drug_name": "Tranexamic Acid",       "order_type": "STAT",     "dose": "1g",          "route": "IV",   "schedule": "Completed",   "status": "Completed"},
            {"drug_name": "Enoxaparin",            "order_type": "STAT",     "dose": "40mg",        "route": "SC",   "schedule": "OD",          "status": "Pending"},
            {"drug_name": "Pantoprazole",          "order_type": "STAT",     "dose": "40mg",        "route": "IV",   "schedule": "BD",          "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Polytrauma — rib fractures with pulmonary contusion. Pelvic external fixator in situ. Haemodynamically stable. Lung-protective ventilation. Ortho review planned."),
            (ClinicalNoteType.NURSING,  "External pelvic fixator checked — pin sites clean. Pain score on ketamine infusion 3/10. Repositioned Q2H with log-roll. ICP monitoring not required."),
        ],
    },
    {
        "mrn": "MRN-200008", "cr_number": "CR-2026-1008", "contact_number": "9876540008",
        "name": "Deepa Nair", "age": 36, "gender": Gender.FEMALE,
        "diagnosis": "Major Burn Injury", "weight": 56.0, "height": 160.0, "blood_group": "AB+",
        "doctor": "Dr. Sana Khan",
        "history": ["40% TBSA flame burn", "Inhalation injury present", "Emergency escharotomy and wound debridement"],
        "comorbidities": [],
        "ventilator": {"mode": "AC/VC", "fio2": 0.55, "peep": 8.0,  "set_rr": 16, "tidal_volume": 360.0},
        "labs": {"ph": 7.35, "pao2": 78.0, "paco2": 44.0, "hco3": 22.0, "rbs": 155.0},
        "medications": [
            {"drug_name": "Morphine",           "order_type": "Infusion", "dose": "50mg/50ml",    "route": "IV",    "schedule": "Titrate",      "status": "Running", "rate_ml_hr": 5.0, "remaining_vol_ml": 30.0},
            {"drug_name": "Meropenem",          "order_type": "STAT",     "dose": "1g",           "route": "IV",    "schedule": "Q8H",          "status": "Running", "rate_ml_hr": 8.0, "remaining_vol_ml": 60.0},
            {"drug_name": "Hartmann's Solution","order_type": "Infusion", "dose": "Parkland formula", "route": "IV", "schedule": "Titrate UO", "status": "Running", "rate_ml_hr": 500.0, "remaining_vol_ml": 3000.0},
            {"drug_name": "Silver Sulfadiazine","order_type": "STAT",     "dose": "Topical",      "route": "Topical","schedule": "OD dressing", "status": "Given"},
            {"drug_name": "Pantoprazole",       "order_type": "STAT",     "dose": "40mg",         "route": "IV",    "schedule": "BD",          "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "40% TBSA burns with inhalation injury. Parkland resuscitation ongoing — target UO 0.5-1ml/kg/hr. Bronchoscopy: carbonaceous deposits in trachea. ETT cuff inflated."),
            (ClinicalNoteType.NURSING,  "Wounds dressed under sedation. UO 55ml/hr — adequate. Bilateral upper limb escharotomy sites monitored. Pain score 2/10 on morphine infusion."),
        ],
    },
]

NICU_PATIENT_PAYLOADS = [
    {
        "mrn": "MRN-300001", "cr_number": "CR-2026-2001", "contact_number": "9876550001",
        "name": "Amit Joshi", "age": 32, "gender": Gender.MALE,
        "diagnosis": "Severe Traumatic Brain Injury", "weight": 72.0, "height": 174.0, "blood_group": "O+",
        "doctor": "Dr. R. Krishnan",
        "history": ["Fall from height 4m", "GCS 7 on admission", "CT: bifrontal contusions + subdural haematoma"],
        "comorbidities": [],
        "ventilator": {"mode": "AC/VC", "fio2": 0.40, "peep": 5.0,  "set_rr": 14, "tidal_volume": 480.0},
        "labs": {"ph": 7.38, "pao2": 90.0, "paco2": 38.0, "hco3": 22.0, "rbs": 148.0},
        "medications": [
            {"drug_name": "Mannitol 20%",        "order_type": "Infusion", "dose": "200ml",       "route": "IV",   "schedule": "Q6H",          "status": "Running", "rate_ml_hr": 100.0, "remaining_vol_ml": 150.0},
            {"drug_name": "Levetiracetam",       "order_type": "STAT",     "dose": "1000mg",      "route": "IV",   "schedule": "BD",           "status": "Given"},
            {"drug_name": "Propofol",            "order_type": "Infusion", "dose": "200mg/20ml",  "route": "IV",   "schedule": "Titrate ICP",  "status": "Running", "rate_ml_hr": 12.0, "remaining_vol_ml": 10.0},
            {"drug_name": "Noradrenaline",       "order_type": "Infusion", "dose": "4mg/50ml",    "route": "IV",   "schedule": "CPP >60 mmHg", "status": "Running", "rate_ml_hr": 4.0, "remaining_vol_ml": 30.0},
            {"drug_name": "Piperacillin-Tazobactam","order_type": "STAT",  "dose": "4.5g",        "route": "IV",   "schedule": "Q8H",          "status": "Running", "rate_ml_hr": 10.0, "remaining_vol_ml": 70.0},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Severe TBI. ICP monitoring probe in situ — ICP 22 mmHg. CPP 64 mmHg. Mannitol Q6H. Head of bed 30°. Normothermia maintained. Neurosurgery on standby."),
            (ClinicalNoteType.NURSING,  "ICP probe secured. Pupils: R 3mm sluggish, L 3mm brisk. Sedation RASS -3. Neuro obs Q1H. HOB strictly 30°."),
        ],
    },
    {
        "mrn": "MRN-300002", "cr_number": "CR-2026-2002", "contact_number": "9876550002",
        "name": "Sunita Rao", "age": 57, "gender": Gender.FEMALE,
        "diagnosis": "Subarachnoid Haemorrhage", "weight": 60.0, "height": 160.0, "blood_group": "A+",
        "doctor": "Dr. R. Krishnan",
        "history": ["Sudden-onset worst headache", "WFNS grade 4", "CT: diffuse SAH Fisher grade 3"],
        "comorbidities": ["Hypertension"],
        "ventilator": {"mode": "AC/VC", "fio2": 0.45, "peep": 5.0,  "set_rr": 14, "tidal_volume": 390.0},
        "labs": {"ph": 7.40, "pao2": 88.0, "paco2": 40.0, "hco3": 24.0, "rbs": 162.0},
        "medications": [
            {"drug_name": "Nimodipine",     "order_type": "Infusion", "dose": "50ml/50ml",   "route": "IV",   "schedule": "Continuous",      "status": "Running", "rate_ml_hr": 2.0,  "remaining_vol_ml": 40.0},
            {"drug_name": "Levetiracetam",  "order_type": "STAT",     "dose": "1000mg",      "route": "IV",   "schedule": "BD",              "status": "Given"},
            {"drug_name": "Noradrenaline",  "order_type": "Infusion", "dose": "4mg/50ml",    "route": "IV",   "schedule": "Keep MAP 80-100", "status": "Running", "rate_ml_hr": 5.0,  "remaining_vol_ml": 25.0},
            {"drug_name": "Dexamethasone",  "order_type": "STAT",     "dose": "4mg",         "route": "IV",   "schedule": "Q6H",             "status": "Given"},
            {"drug_name": "Enoxaparin",     "order_type": "STAT",     "dose": "40mg",        "route": "SC",   "schedule": "OD (after clipping)","status": "Pending"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "SAH WFNS grade 4 — aneurysm clipping (R MCA) performed yesterday. On nimodipine for vasospasm prevention. TCD daily. Daily neuro assessment."),
            (ClinicalNoteType.NURSING,  "External ventricular drain at 15 cmH2O — CSF 10ml/h (clear). Pupils equal 3mm reactive. GCS improving E3V2M4."),
        ],
    },
    {
        "mrn": "MRN-300003", "cr_number": "CR-2026-2003", "contact_number": "9876550003",
        "name": "Pramod Kumar", "age": 28, "gender": Gender.MALE,
        "diagnosis": "Status Epilepticus", "weight": 68.0, "height": 172.0, "blood_group": "B+",
        "doctor": "Dr. R. Krishnan",
        "history": ["Known epilepsy — non-compliance with medication", "Generalised tonic-clonic seizures >30 min"],
        "comorbidities": ["Epilepsy"],
        "ventilator": {"mode": "CPAP",  "fio2": 0.30, "peep": 4.0,  "set_rr": 12, "tidal_volume": 460.0},
        "labs": {"ph": 7.35, "pao2": 92.0, "paco2": 42.0, "hco3": 23.0, "rbs": 90.0},
        "medications": [
            {"drug_name": "Midazolam",        "order_type": "Infusion", "dose": "50mg/50ml",  "route": "IV",   "schedule": "Titrate EEG",  "status": "Running", "rate_ml_hr": 5.0,  "remaining_vol_ml": 35.0},
            {"drug_name": "Valproate",        "order_type": "Infusion", "dose": "1200mg",     "route": "IV",   "schedule": "Loading done", "status": "Running", "rate_ml_hr": 4.0,  "remaining_vol_ml": 40.0},
            {"drug_name": "Levetiracetam",    "order_type": "STAT",     "dose": "1500mg",     "route": "IV",   "schedule": "BD",           "status": "Given"},
            {"drug_name": "Lacosamide",       "order_type": "STAT",     "dose": "200mg",      "route": "IV",   "schedule": "BD",           "status": "Pending"},
            {"drug_name": "Pantoprazole",     "order_type": "STAT",     "dose": "40mg",       "route": "IV",   "schedule": "OD",           "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "RSE — refractory to lorazepam, levetiracetam, valproate. Intubated for airway protection. Continuous EEG: burst-suppression achieved on midazolam 5mg/hr."),
            (ClinicalNoteType.NURSING,  "Continuous EEG leads secured. Midazolam running — RASS -4. Temperature 37.2°C. Foley catheter draining 60ml/hr."),
        ],
    },
    {
        "mrn": "MRN-300004", "cr_number": "CR-2026-2004", "contact_number": "9876550004",
        "name": "Usha Krishnan", "age": 44, "gender": Gender.FEMALE,
        "diagnosis": "Guillain-Barré Syndrome", "weight": 58.0, "height": 162.0, "blood_group": "O-",
        "doctor": "Dr. R. Krishnan",
        "history": ["Ascending weakness over 1 week", "AMSAN variant", "Intubated for respiratory failure"],
        "comorbidities": [],
        "ventilator": {"mode": "AC/VC", "fio2": 0.35, "peep": 5.0,  "set_rr": 14, "tidal_volume": 380.0},
        "labs": {"ph": 7.39, "pao2": 92.0, "paco2": 41.0, "hco3": 24.0, "rbs": 102.0},
        "medications": [
            {"drug_name": "IVIG",              "order_type": "Infusion", "dose": "0.4g/kg/day", "route": "IV",   "schedule": "5 days",        "status": "Running", "rate_ml_hr": 40.0, "remaining_vol_ml": 200.0},
            {"drug_name": "Enoxaparin",        "order_type": "STAT",     "dose": "40mg",        "route": "SC",   "schedule": "OD",            "status": "Given"},
            {"drug_name": "Gabapentin",        "order_type": "STAT",     "dose": "300mg",       "route": "Oral", "schedule": "TDS",           "status": "Given"},
            {"drug_name": "Metoprolol",        "order_type": "PRN",      "dose": "25mg",        "route": "Oral", "schedule": "PRN HR >100",   "status": "Pending"},
            {"drug_name": "Pantoprazole",      "order_type": "STAT",     "dose": "40mg",        "route": "IV",   "schedule": "OD",            "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "GBS AMSAN — IVIG day 3 of 5. MRC sum score 14/60. Autonomic instability: BP labile. Plan NIV trial when FVC >15ml/kg. Physio Q6H."),
            (ClinicalNoteType.NURSING,  "Pressure care Q2H. Passive limb exercises performed. Eye care — artificial tears Q4H. Autonomic obs Q1H: HR 92, BP 130/85."),
        ],
    },
    {
        "mrn": "MRN-300005", "cr_number": "CR-2026-2005", "contact_number": "9876550005",
        "name": "Manoj Patel", "age": 22, "gender": Gender.MALE,
        "diagnosis": "Bacterial Meningitis", "weight": 65.0, "height": 170.0, "blood_group": "B-",
        "doctor": "Dr. R. Krishnan",
        "history": ["Fever, headache, neck stiffness 3 days", "CSF: turbid, neutrophilic, gram +ve diplococci"],
        "comorbidities": [],
        "ventilator": {"mode": "PSV",   "fio2": 0.30, "peep": 4.0,  "set_rr": 12, "tidal_volume": 440.0},
        "labs": {"ph": 7.38, "pao2": 93.0, "paco2": 40.0, "hco3": 23.0, "rbs": 88.0},
        "medications": [
            {"drug_name": "Ceftriaxone",    "order_type": "STAT",     "dose": "2g",         "route": "IV",   "schedule": "Q12H",    "status": "Running", "rate_ml_hr": 10.0, "remaining_vol_ml": 80.0},
            {"drug_name": "Dexamethasone",  "order_type": "STAT",     "dose": "10mg",       "route": "IV",   "schedule": "Q6H x4d", "status": "Given"},
            {"drug_name": "Paracetamol",    "order_type": "PRN",      "dose": "1g",         "route": "IV",   "schedule": "Q6H PRN", "status": "Given"},
            {"drug_name": "Levetiracetam",  "order_type": "STAT",     "dose": "500mg",      "route": "IV",   "schedule": "BD",      "status": "Given"},
            {"drug_name": "Mannitol 20%",   "order_type": "PRN",      "dose": "100ml",      "route": "IV",   "schedule": "PRN ICP", "status": "Pending"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Pneumococcal meningitis confirmed. Ceftriaxone day 3. GCS improving E4V4M6. Fever settling. Daily neuro review. Contact tracing initiated."),
            (ClinicalNoteType.NURSING,  "Dark room and low stimulation maintained. Neuro obs Q2H — GCS 14. Temperature 38.2°C. Paracetamol given."),
        ],
    },
    {
        "mrn": "MRN-300006", "cr_number": "CR-2026-2006", "contact_number": "9876550006",
        "name": "Rekha Singh", "age": 68, "gender": Gender.FEMALE,
        "diagnosis": "Hypertensive Intracerebral Haemorrhage", "weight": 62.0, "height": 156.0, "blood_group": "A+",
        "doctor": "Dr. R. Krishnan",
        "history": ["Sudden right-sided weakness and dysphasia", "CT: left basal ganglia ICH 35ml", "Hypertensive emergency"],
        "comorbidities": ["Hypertension", "Atrial Fibrillation"],
        "ventilator": {"mode": "PSV",   "fio2": 0.32, "peep": 5.0,  "set_rr": 12, "tidal_volume": 400.0},
        "labs": {"ph": 7.41, "pao2": 89.0, "paco2": 40.0, "hco3": 25.0, "rbs": 175.0},
        "medications": [
            {"drug_name": "Labetalol",      "order_type": "Infusion", "dose": "200mg/50ml",  "route": "IV",   "schedule": "Titrate SBP<160","status": "Running", "rate_ml_hr": 4.0,  "remaining_vol_ml": 30.0},
            {"drug_name": "Mannitol 20%",   "order_type": "PRN",      "dose": "200ml",       "route": "IV",   "schedule": "Q6H PRN ICP",    "status": "Given"},
            {"drug_name": "Levetiracetam",  "order_type": "STAT",     "dose": "500mg",       "route": "IV",   "schedule": "BD prophylaxis",  "status": "Given"},
            {"drug_name": "Atorvastatin",   "order_type": "STAT",     "dose": "40mg",        "route": "Oral", "schedule": "OD",             "status": "Given"},
            {"drug_name": "Pantoprazole",   "order_type": "STAT",     "dose": "40mg",        "route": "IV",   "schedule": "OD",             "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Hypertensive ICH 35ml left BG. Conservative management — BP target SBP 140-160. Repeat CT at 24h — no expansion. Anticoagulation held."),
            (ClinicalNoteType.NURSING,  "Neuro obs Q2H: GCS 12 (E4V3M5). Right arm power 2/5. HOB 30°. Anti-embolic stockings applied. Atrial fibrillation on cardiac monitor."),
        ],
    },
    {
        "mrn": "MRN-300007", "cr_number": "CR-2026-2007", "contact_number": "9876550007",
        "name": "Vijay Nair", "age": 50, "gender": Gender.MALE,
        "diagnosis": "Myasthenic Crisis", "weight": 75.0, "height": 173.0, "blood_group": "O+",
        "doctor": "Dr. R. Krishnan",
        "history": ["Myasthenia gravis (ocular to generalised)", "Respiratory muscle weakness — intubated"],
        "comorbidities": ["Myasthenia Gravis"],
        "ventilator": {"mode": "SIMV",  "fio2": 0.35, "peep": 5.0,  "set_rr": 12, "tidal_volume": 500.0},
        "labs": {"ph": 7.40, "pao2": 91.0, "paco2": 40.0, "hco3": 24.0, "rbs": 105.0},
        "medications": [
            {"drug_name": "Plasmapheresis",    "order_type": "STAT",     "dose": "1 session",    "route": "IV",   "schedule": "5 sessions total", "status": "Running", "rate_ml_hr": 80.0, "remaining_vol_ml": 1200.0},
            {"drug_name": "Pyridostigmine",    "order_type": "STAT",     "dose": "60mg",         "route": "Oral", "schedule": "Q4H",              "status": "Given"},
            {"drug_name": "Prednisolone",      "order_type": "STAT",     "dose": "60mg",         "route": "Oral", "schedule": "OD",               "status": "Given"},
            {"drug_name": "Pantoprazole",      "order_type": "STAT",     "dose": "40mg",         "route": "IV",   "schedule": "OD",               "status": "Given"},
            {"drug_name": "Enoxaparin",        "order_type": "STAT",     "dose": "40mg",         "route": "SC",   "schedule": "OD",               "status": "Given"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Myasthenic crisis — intubated day 3. Plasmapheresis session 2 of 5 completed. FVC trending up (800ml today). Plan: SBT trial when FVC >1L."),
            (ClinicalNoteType.NURSING,  "Spontaneous breathing trial attempted — failed (RR 32, SpO2 88%). Patient fatigues quickly. Repositioned for comfort."),
        ],
    },
    {
        "mrn": "MRN-300008", "cr_number": "CR-2026-2008", "contact_number": "9876550008",
        "name": "Anita Reddy", "age": 61, "gender": Gender.FEMALE,
        "diagnosis": "Posterior Circulation Stroke", "weight": 63.0, "height": 158.0, "blood_group": "B+",
        "doctor": "Dr. R. Krishnan",
        "history": ["Sudden onset vertigo, diplopia, ataxia", "MRI: acute basilar artery territory infarct"],
        "comorbidities": ["Hypertension", "Diabetes"],
        "ventilator": {"mode": "PSV",   "fio2": 0.30, "peep": 4.0,  "set_rr": 12, "tidal_volume": 420.0},
        "labs": {"ph": 7.39, "pao2": 93.0, "paco2": 41.0, "hco3": 24.0, "rbs": 192.0},
        "medications": [
            {"drug_name": "Aspirin",            "order_type": "STAT",     "dose": "300mg",     "route": "Oral", "schedule": "OD",             "status": "Given"},
            {"drug_name": "Clopidogrel",        "order_type": "STAT",     "dose": "75mg",      "route": "Oral", "schedule": "OD",             "status": "Given"},
            {"drug_name": "Atorvastatin",       "order_type": "STAT",     "dose": "80mg",      "route": "Oral", "schedule": "OD",             "status": "Given"},
            {"drug_name": "Insulin Infusion",   "order_type": "Infusion", "dose": "50U/50ml",  "route": "IV",   "schedule": "Sliding Scale",  "status": "Running", "rate_ml_hr": 2.0, "remaining_vol_ml": 42.0},
            {"drug_name": "Amlodipine",         "order_type": "STAT",     "dose": "5mg",       "route": "Oral", "schedule": "OD",             "status": "Pending"},
        ],
        "notes": [
            (ClinicalNoteType.PROGRESS, "Basilar artery infarct — posterior circulation. No thrombolysis (outside window). Dual antiplatelet started. Swallowing assessment failed — NG inserted."),
            (ClinicalNoteType.NURSING,  "Neuro obs Q2H: GCS 13. Diplopia persisting. Aspiration precautions strict. NG feeds started. Blood glucose Q2H — 188, sliding scale adjusted."),
        ],
    },
]

ALL_PATIENT_NAMES = (
    [p["name"] for p in MICU_PATIENT_PAYLOADS]
    + [p["name"] for p in SICU_PATIENT_PAYLOADS]
    + [p["name"] for p in NICU_PATIENT_PAYLOADS]
)

password_service = PasswordService()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def utc_now() -> datetime:
    return datetime.now(UTC)


# ---------------------------------------------------------------------------
# Clear
# ---------------------------------------------------------------------------

def clear_seed_data(db: Session) -> None:
    seed_patients = (
        db.query(PatientModel)
        .filter(PatientModel.name.in_(ALL_PATIENT_NAMES))
        .all()
    )
    seed_patient_ids = [p.id for p in seed_patients]

    if seed_patient_ids:
        for model in [
            PatientStaffAssignmentModel, AlarmModel, LatestVitalModel,
            VitalModel, TimelineEventModel, ClinicalNoteModel,
            VentilatorSettingModel, LabResultModel, FluidBalanceModel,
            MedicationOrderModel,
        ]:
            db.query(model).filter(
                model.patient_id.in_(seed_patient_ids)
            ).delete(synchronize_session=False)

        db.query(PatientModel).filter(
            PatientModel.id.in_(seed_patient_ids)
        ).delete(synchronize_session=False)

    db.query(DeviceMasterModel).filter(
        DeviceMasterModel.serial.in_(ALL_DEVICE_SERIALS)
    ).delete(synchronize_session=False)

    db.query(BedMasterModel).filter(
        BedMasterModel.bed_id.in_(ALL_BED_IDS)
    ).delete(synchronize_session=False)

    db.query(ICUUnitMasterModel).filter(
        ICUUnitMasterModel.icu_name.in_(SEED_ICU_NAMES)
    ).delete(synchronize_session=False)

    db.query(UserModel).filter(
        UserModel.user_id.in_([u["user_id"] for u in SEED_USERS])
    ).delete(synchronize_session=False)

    db.query(RolePermissionModel).delete(synchronize_session=False)
    db.query(PermissionModel).delete(synchronize_session=False)
    db.query(RoleModel).filter(
        RoleModel.name.in_([r.value for r in UserRole])
    ).delete(synchronize_session=False)

    hospital = db.query(HospitalModel).filter(
        HospitalModel.code == HOSPITAL_CODE
    ).first()
    if hospital:
        db.query(HospitalUnitModel).filter(
            HospitalUnitModel.hospital_id == hospital.id
        ).delete(synchronize_session=False)
        db.query(HospitalModel).filter(
            HospitalModel.id == hospital.id
        ).delete(synchronize_session=False)

    db.commit()


# ---------------------------------------------------------------------------
# Auth / permissions
# ---------------------------------------------------------------------------

def seed_permissions(db: Session) -> list[PermissionModel]:
    permissions = []
    for module in PERMISSION_MODULES:
        for action in PERMISSION_ACTIONS:
            p = PermissionModel(module=module.value, action=action.value)
            db.add(p)
            db.flush()
            permissions.append(p)
    return permissions


def seed_roles(db: Session) -> dict[str, RoleModel]:
    roles = {}
    for role in UserRole:
        m = RoleModel(name=role.value, description=f"{role.value.title()} role")
        db.add(m)
        db.flush()
        roles[role.value] = m
    return roles


def seed_role_permissions(
    db: Session,
    roles: dict[str, RoleModel],
    permissions: list[PermissionModel],
) -> None:
    pmap = {(p.module, p.action): p for p in permissions}

    def perms_for(module, actions):
        return [pmap[(module.value, a.value)] for a in actions]

    all_p = permissions
    doc_p = (
        perms_for(PermissionModule.PATIENTS,   [PermissionAction.VIEW, PermissionAction.CREATE, PermissionAction.MODIFY])
        + perms_for(PermissionModule.VITALS,   [PermissionAction.VIEW, PermissionAction.CREATE])
        + perms_for(PermissionModule.TIMELINE, [PermissionAction.VIEW, PermissionAction.CREATE])
        + perms_for(PermissionModule.ALARMS,   [PermissionAction.VIEW, PermissionAction.MODIFY])
        + perms_for(PermissionModule.DASHBOARD,[PermissionAction.VIEW])
    )
    nur_p = (
        perms_for(PermissionModule.PATIENTS,   [PermissionAction.VIEW])
        + perms_for(PermissionModule.VITALS,   [PermissionAction.VIEW, PermissionAction.CREATE])
        + perms_for(PermissionModule.TIMELINE, [PermissionAction.VIEW, PermissionAction.CREATE])
        + perms_for(PermissionModule.ALARMS,   [PermissionAction.VIEW, PermissionAction.MODIFY])
        + perms_for(PermissionModule.DASHBOARD,[PermissionAction.VIEW])
    )

    mapping = {UserRole.ADMIN.value: all_p, UserRole.DOCTOR.value: doc_p, UserRole.NURSE.value: nur_p}
    for role_name, rperms in mapping.items():
        role = roles[role_name]
        for perm in rperms:
            db.add(RolePermissionModel(role_id=role.id, permission_id=perm.id))


# ---------------------------------------------------------------------------
# Hospital / ICU
# ---------------------------------------------------------------------------

def seed_hospital_and_units(db: Session) -> tuple[HospitalModel, list[HospitalUnitModel]]:
    hospital = HospitalModel(
        name=HOSPITAL_NAME, code=HOSPITAL_CODE,
        address="Bengaluru", city="Bengaluru", state="Karnataka",
        country="India", contact_number="9999999999", email="admin@apollo.example",
    )
    db.add(hospital)
    db.flush()

    units = []
    for unit_name in UNIT_NAMES:
        u = HospitalUnitModel(
            hospital_id=hospital.id,
            name=unit_name,
            code=f"{HOSPITAL_CODE}-{unit_name}",
            is_active=True,
        )
        db.add(u)
        db.flush()
        units.append(u)
    return hospital, units


def seed_icu_units(db: Session) -> list[ICUUnitMasterModel]:
    payloads = [
        {"icu_name": "MICU-1", "type": "Medical ICU",       "department": "Critical Care",  "beds": 10, "devices": 20, "gateway": "GW-MICU-001", "status": "ACTIVE"},
        {"icu_name": "SICU-1", "type": "Surgical ICU",      "department": "Surgery",         "beds": 8,  "devices": 16, "gateway": "GW-SICU-001", "status": "ACTIVE"},
        {"icu_name": "NICU-1", "type": "Neurological ICU",  "department": "Neurology",       "beds": 8,  "devices": 16, "gateway": "GW-NICU-001", "status": "ACTIVE"},
    ]
    icu_units = []
    for payload in payloads:
        m = ICUUnitMasterModel(**payload)
        db.add(m)
        db.flush()
        icu_units.append(m)
    return icu_units


# ---------------------------------------------------------------------------
# Beds / devices
# ---------------------------------------------------------------------------

def _make_beds(
    db: Session,
    bed_ids: list[str],
    icu_unit: ICUUnitMasterModel,
    ward: str,
    floor: str,
    serial_prefix: str,
) -> tuple[list[BedMasterModel], list[DeviceMasterModel]]:
    beds, devices = [], []
    for index, bed_id in enumerate(bed_ids, start=1):
        bed = BedMasterModel(
            bed_id=bed_id, icu_unit_id=icu_unit.id, bed_type="ICU",
            department="Critical Care", ward=ward, floor=floor,
            room=f"{floor}{index:02d}", cleaning_status="CLEAN",
            maintenance_status="OK", operational_status="OCCUPIED",
            last_sanitized=utc_now(),
        )
        db.add(bed)
        db.flush()
        beds.append(bed)

        device = DeviceMasterModel(
            device_type="MONITOR", manufacturer="Generic",
            model="Bedside Monitor",
            serial=f"{serial_prefix}-{index:03d}",
            bed_id=bed.id,
            ip_address=f"192.168.{floor}.{100 + index}",
            status="ONLINE",
        )
        db.add(device)
        db.flush()
        devices.append(device)

    return beds, devices


def seed_beds_and_devices(
    db: Session,
    icu_units: list[ICUUnitMasterModel],
) -> tuple[dict[str, list[BedMasterModel]], dict[str, list[DeviceMasterModel]]]:
    micu_beds, micu_devices = _make_beds(db, MICU_BED_IDS, icu_units[0], "MICU", "1", "MICU-MONITOR")
    sicu_beds, sicu_devices = _make_beds(db, SICU_BED_IDS, icu_units[1], "SICU", "2", "SICU-MONITOR")
    nicu_beds, nicu_devices = _make_beds(db, NICU_BED_IDS, icu_units[2], "NICU", "3", "NICU-MONITOR")
    return (
        {"micu": micu_beds, "sicu": sicu_beds, "nicu": nicu_beds},
        {"micu": micu_devices, "sicu": sicu_devices, "nicu": nicu_devices},
    )


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

def seed_users(
    db: Session,
    roles: dict[str, RoleModel],
    hospital: HospitalModel,
    unit: HospitalUnitModel,
) -> list[UserModel]:
    users = []
    for user_data in SEED_USERS:
        u = UserModel(
            user_id=user_data["user_id"],
            first_name=user_data["first_name"], last_name=user_data["last_name"],
            email=user_data["email"],
            password_hash=password_service.hash_password(user_data["password"]),
            role_id=roles[user_data["role"].value].id,
            hospital_id=hospital.id, unit_id=unit.id,
            shift=user_data["shift"].value, is_active=True,
        )
        db.add(u)
        db.flush()
        users.append(u)
    return users


# ---------------------------------------------------------------------------
# Patients (generic — used for all three units)
# ---------------------------------------------------------------------------

def _seed_patient_group(
    db: Session,
    payloads: list[dict],
    hospital: HospitalModel,
    beds: list[BedMasterModel],
    doctor: "UserModel",
    nurse: "UserModel",
    day_offset_start: int = 0,
) -> list[PatientModel]:
    patients = []
    for index, payload in enumerate(payloads):
        patient = PatientModel(
            mrn=payload["mrn"], cr_number=payload["cr_number"],
            contact_number=payload["contact_number"],
            name=payload["name"], age=payload["age"], gender=payload["gender"],
            bed_id=beds[index].id, diagnosis=payload["diagnosis"],
            weight=payload["weight"], height=payload["height"],
            blood_group=payload["blood_group"], doctor=payload["doctor"],
            admission_time=utc_now() - timedelta(days=day_offset_start + index),
            hospital_id=hospital.id, status="admitted",
            history=payload["history"], comorbidities=payload["comorbidities"],
        )
        db.add(patient)
        db.flush()
        patients.append(patient)

        # Staff assignments
        db.add(PatientStaffAssignmentModel(patient_id=patient.id, user_id=doctor.id,
            assignment_type="DOCTOR", assigned_at=utc_now(), is_active=True))
        db.add(PatientStaffAssignmentModel(patient_id=patient.id, user_id=nurse.id,
            assignment_type="NURSE",  assigned_at=utc_now(), is_active=True))

        # 24h hourly vitals
        base_hr = random.randint(75, 115)
        base_bp_sys = random.randint(100, 145)
        base_bp_dia = random.randint(62, 90)
        base_spo2 = random.randint(90, 99)
        base_temp = round(random.uniform(98.0, 101.5), 1)
        base_rr = random.randint(14, 26)
        now = utc_now()
        for hour in range(24):
            db.add(VitalModel(
                patient_id=patient.id,
                hr=base_hr + random.randint(-8, 8),
                bp_sys=base_bp_sys + random.randint(-10, 10),
                bp_dia=base_bp_dia + random.randint(-5, 5),
                spo2=min(100, base_spo2 + random.randint(-3, 2)),
                temp=round(base_temp + random.uniform(-0.4, 0.4), 1),
                rr=base_rr + random.randint(-3, 3),
                recorded_at=now - timedelta(hours=23 - hour),
            ))
        db.add(LatestVitalModel(
            patient_id=patient.id, bed_id=patient.bed_id, device_id=None,
            hr=base_hr, bp_sys=base_bp_sys, bp_dia=base_bp_dia,
            spo2=base_spo2, temp=base_temp, rr=base_rr,
            status="LIVE", recorded_at=utc_now(), updated_at=utc_now(),
        ))

        # Timeline
        db.add(TimelineEventModel(patient_id=patient.id, type=TimelineEventType.STATUS_CHANGED.value,
            event=f"{patient.name} admitted to ICU — {patient.diagnosis}", created_at=patient.admission_time))
        db.add(TimelineEventModel(patient_id=patient.id, type=TimelineEventType.DEVICE_ASSIGNED.value,
            event=f"Bedside monitor assigned to {patient.name}",
            created_at=patient.admission_time + timedelta(minutes=15)))
        db.add(TimelineEventModel(patient_id=patient.id, type=TimelineEventType.NOTE_ADDED.value,
            event=f"Initial ICU assessment documented for {patient.name}",
            created_at=patient.admission_time + timedelta(hours=1)))

        # Clinical notes
        for note_type, note_text in payload["notes"]:
            author = nurse if note_type == ClinicalNoteType.NURSING else doctor
            db.add(ClinicalNoteModel(
                patient_id=patient.id, author_id=author.id,
                author_name=f"{author.first_name} {author.last_name}",
                note_type=note_type, note_text=note_text,
                created_at=utc_now() - timedelta(hours=random.randint(1, 6)),
                updated_at=utc_now(),
            ))

        # Ventilator
        v = payload["ventilator"]
        db.add(VentilatorSettingModel(
            patient_id=patient.id, mode=v["mode"], fio2=v["fio2"],
            peep=v["peep"], set_rr=v["set_rr"], tidal_volume=v["tidal_volume"],
            recorded_at=utc_now() - timedelta(hours=1),
        ))

        # Lab results
        lab = payload["labs"]
        db.add(LabResultModel(
            patient_id=patient.id, ph=lab["ph"], pao2=lab["pao2"],
            paco2=lab["paco2"], hco3=lab["hco3"], rbs=lab["rbs"],
            recorded_at=utc_now() - timedelta(hours=2),
        ))

        # Fluid balance (5 records per patient)
        now_r = utc_now()
        for source, in_ml, out_ml, hour in [
            ("IV Fluids",       500.0,   0.0,  6),
            ("Oral / NG",       200.0,   0.0,  9),
            ("Urine",             0.0, 350.0, 12),
            ("IV Medications",  300.0,   0.0, 14),
            ("Drain / Other",     0.0, 200.0, 16),
        ]:
            db.add(FluidBalanceModel(
                patient_id=patient.id, in_ml=in_ml, out_ml=out_ml, source=source,
                recorded_at=now_r.replace(hour=hour, minute=0, second=0, microsecond=0),
            ))

        # Medications
        for order in payload["medications"]:
            db.add(MedicationOrderModel(
                patient_id=patient.id,
                drug_name=order["drug_name"], order_type=order["order_type"],
                dose=order["dose"], route=order["route"],
                schedule=order["schedule"], status=order["status"],
                rate_ml_hr=order.get("rate_ml_hr"),
                remaining_vol_ml=order.get("remaining_vol_ml"),
                est_end_time=(
                    utc_now() + timedelta(hours=random.randint(8, 20))
                    if order.get("rate_ml_hr") and order["status"] == "Running" else None
                ),
                created_at=utc_now() - timedelta(hours=random.randint(1, 8)),
                updated_at=utc_now(),
            ))

    return patients


# ---------------------------------------------------------------------------
# Alarms
# ---------------------------------------------------------------------------

def seed_alarms(
    db: Session,
    patients: list[PatientModel],
    beds_by_id: dict[int, BedMasterModel],
    devices_by_bed_id: dict[int, DeviceMasterModel],
) -> None:
    severities = ["Info", "Warning", "Critical"]
    for index, patient in enumerate(patients):
        severity = severities[index % len(severities)]
        bed = beds_by_id.get(patient.bed_id)
        device = devices_by_bed_id.get(patient.bed_id)
        db.add(AlarmModel(
            timestamp=utc_now(), patient_id=patient.id,
            patient_name=patient.name,
            bed_id=bed.bed_id if bed else "UNKNOWN",
            device=device.model if device else "Monitor",
            message=f"{severity} alert for {patient.name}",
            severity=severity,
            acknowledged=severity == "Info", silenced=False,
            escalated=severity == "Critical",
            acknowledged_by="nurse" if severity == "Info" else None,
            silenced_by=None, silence_until=None,
            escalated_by="system" if severity == "Critical" else None,
            escalate_to="doctor" if severity == "Critical" else None,
        ))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    db = SessionLocal()
    try:
        print("Clearing existing seed data...")
        clear_seed_data(db)

        print("Creating permissions and roles...")
        permissions = seed_permissions(db)
        roles = seed_roles(db)
        seed_role_permissions(db=db, roles=roles, permissions=permissions)

        print("Creating hospital...")
        hospital, units = seed_hospital_and_units(db)

        print("Creating ICU units...")
        icu_units = seed_icu_units(db)

        print("Creating beds and devices...")
        beds_map, devices_map = seed_beds_and_devices(db=db, icu_units=icu_units)

        print("Creating users...")
        users = seed_users(db=db, roles=roles, hospital=hospital, unit=units[0])
        doctor = next(u for u in users if u.user_id == "doctor")
        nurse  = next(u for u in users if u.user_id == "nurse")

        print("Seeding MICU-1 patients (10)...")
        micu_patients = _seed_patient_group(
            db, MICU_PATIENT_PAYLOADS, hospital, beds_map["micu"], doctor, nurse, day_offset_start=0)

        print("Seeding SICU-1 patients (8)...")
        sicu_patients = _seed_patient_group(
            db, SICU_PATIENT_PAYLOADS, hospital, beds_map["sicu"], doctor, nurse, day_offset_start=10)

        print("Seeding NICU-1 patients (8)...")
        nicu_patients = _seed_patient_group(
            db, NICU_PATIENT_PAYLOADS, hospital, beds_map["nicu"], doctor, nurse, day_offset_start=20)

        all_patients = micu_patients + sicu_patients + nicu_patients

        # Build lookup maps for alarm seeding
        all_beds   = beds_map["micu"] + beds_map["sicu"] + beds_map["nicu"]
        all_devices = devices_map["micu"] + devices_map["sicu"] + devices_map["nicu"]
        beds_by_id   = {b.id: b for b in all_beds}
        devices_by_bed_id = {d.bed_id: d for d in all_devices}

        print("Creating alarms...")
        seed_alarms(db=db, patients=all_patients,
                    beds_by_id=beds_by_id, devices_by_bed_id=devices_by_bed_id)

        db.commit()

        total_notes = (
            sum(len(p["notes"]) for p in MICU_PATIENT_PAYLOADS)
            + sum(len(p["notes"]) for p in SICU_PATIENT_PAYLOADS)
            + sum(len(p["notes"]) for p in NICU_PATIENT_PAYLOADS)
        )
        total_meds = (
            sum(len(p["medications"]) for p in MICU_PATIENT_PAYLOADS)
            + sum(len(p["medications"]) for p in SICU_PATIENT_PAYLOADS)
            + sum(len(p["medications"]) for p in NICU_PATIENT_PAYLOADS)
        )

        print("\nSeeding complete.")
        print(f"  MICU-1  : {len(micu_patients)} patients")
        print(f"  SICU-1  : {len(sicu_patients)} patients")
        print(f"  NICU-1  : {len(nicu_patients)} patients")
        print(f"  Total   : {len(all_patients)} patients")
        print(f"  Vitals  : {len(all_patients) * 24} readings (24h flowsheet per patient)")
        print(f"  Notes   : {total_notes}")
        print(f"  Meds    : {total_meds}")
        print("\nDev login users:")
        for u in SEED_USERS:
            print(f"  {u['email']} / {u['password']} ({u['role'].value})")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
