# 📘 Cortex ICU Backend – API Reference

## 🔹 Base URL
/api/v1

---

## 🔹 Overview
This API manages ICU patients, vitals, timeline events, devices, and assignments.

---

## 🔹 Modules
- Patients
- Vitals
- Timeline
- Devices

---

## 🔹 Endpoints Summary
Total: 17 endpoints

---

## 🧑‍⚕️ Patients
POST /patients  
GET /patients  
GET /patients/{patient_id}  
PUT /patients/{patient_id}  
POST /patients/{patient_id}/discharge  

---

## 🫀 Vitals
POST /patients/{patient_id}/vitals  
GET /patients/{patient_id}/vitals  
GET /patients/{patient_id}/vitals/{vital_id}  

---

## 📜 Timeline
POST /patients/{patient_id}/timeline  
GET /patients/{patient_id}/timeline  

---

## 🖥️ Devices
POST /devices  
GET /devices  
GET /devices/{device_id}  
PUT /devices/{device_id}  

---

## 🔗 Patient-Device Assignment
POST /patients/{patient_id}/devices/{device_id}  
DELETE /patients/{patient_id}/devices/{device_id}  
GET /patients/{patient_id}/devices  

---

## 🔹 Error Handling

| Code | Meaning |
|------|--------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Error |

---

## 🔹 Standard Error Response
```json
{
  "detail": "Error message"
}