# Cortex ICU API Overview

This document summarises the primary REST and WebSocket endpoints exposed by the Cortex ICU platform. All requests are prefixed with `/api` and return JSON responses. Authentication uses JWT Bearer tokens unless otherwise noted.

## Authentication

### `POST /api/auth/register`
Register a new user. Only an initial setup script or an administrator should call this. Requires `username`, `password`, `full_name`, `email` and `role_id`.

### `POST /api/auth/login`
Authenticate a user using the OAuth2 password flow. Send `username` and `password` in form fields.  
If multi‑factor authentication (MFA) is enabled for the user, include a valid TOTP code as an extra `scopes` field.  
Returns an access token and refresh token.

```
Request (form-encoded):
username=john&password=secret&scope=123456
```

Response (JSON):
```json
{
  "access_token": "eyJhbGciOi...",
  "refresh_token": "eyJhbGciOi..."
}
```

### `POST /api/auth/refresh`
Exchange a refresh token for a new access token.

### `GET /api/auth/mfa/setup`
Return a new TOTP secret and otpauth URI for the current user. Use this to enrol a user into MFA. Requires an authenticated user.

### `POST /api/auth/mfa/enable`
Enable MFA for the current user after verifying the provided TOTP code.

## Users

These endpoints are restricted to administrators or the user themselves depending on the operation.

| Method & Path           | Description                                      |
|-------------------------|--------------------------------------------------|
| `GET /api/users/`       | List all users (admin only).                     |
| `GET /api/users/{id}`   | Retrieve a user by ID. Users can see themselves. |
| `PATCH /api/users/{id}` | Update a user’s profile, password, role or activation status. |

## Patients

| Method & Path           | Description                                       |
|-------------------------|---------------------------------------------------|
| `GET /api/patients/`    | List patients (paginated via `skip` and `limit`). |
| `POST /api/patients/`   | Admit a new patient to a bed. Provide `bed_id`, `first_name`, `last_name`, `date_of_birth`, `gender`, and `mrn`. |
| `GET /api/patients/{id}` | Get details for a specific patient. |
| `PATCH /api/patients/{id}` | Update patient information or discharge time. |

## Lines & Tubes

Lines and tubes (e.g. central venous catheters, arterial lines, drains) are tracked per patient. Managing these devices helps reduce infection risk and ensures timely replacement.

| Method & Path | Description |
|---------------|-------------|
| `GET /api/patients/{patient_id}/lines` | List all lines/tubes for a specific patient. Returns an array of line objects with type, insertion time, expected removal time, status and notes. |
| `POST /api/patients/{patient_id}/lines` | Create a new line or tube record for the patient. Provide `type`, `insertion_time` (ISO‑8601), optional `expected_removal_time` and `notes`. Only users with roles Nurse, Doctor or ICU Admin may call this endpoint. |
| `PATCH /api/lines/{id}` | Update an existing line/tube. All fields are optional: `type`, `expected_removal_time`, `removed_time`, `notes`, `status`. Setting `removed_time` marks the line as removed. |

## AI Suggestions

These endpoints surface AI‑driven insights about a patient. In the MVP the response is stubbed but the contract is defined to enable integration with a real AI engine later.

| Method & Path | Description |
|---------------|-------------|
| `GET /api/patients/{patient_id}/ai-suggestions` | Returns a JSON object containing a `risk_score` between 0 and 1, a list of `recommendations` (strings) and a free‑text `summary`. Only clinicians (Doctor, Nurse, ICU Admin) should call this endpoint. |

## Devices

| Method & Path             | Description                                     |
|---------------------------|-------------------------------------------------|
| `GET /api/devices/`       | List devices (paginated). The response includes `device_type_id` and `device_type_name`. |
| `POST /api/devices/`      | Create a new device attached to a bed. Provide `bed_id` and either `device_type_id` (preferred) or `device_type_name`; optionally `serial_number`. |
| `GET /api/devices/{id}`   | Get details of a device.                     |
| `PATCH /api/devices/{id}` | Update device fields such as `bed_id`, `device_type_id`/`device_type_name`, `serial_number` or `status`. |

## Vitals

| Method & Path                  | Description                                                                                                        |
|--------------------------------|--------------------------------------------------------------------------------------------------------------------|
| `POST /api/vitals/`            | Create a new vital measurement. Provide `patient_id`, `device_id`, `vital_type`, `value`, and `recorded_at` (ISO8601). The server stores the measurement and broadcasts it via WebSocket to subscribed clients. |
| `GET /api/vitals/{patient_id}` | Return the most recent vital measurements for a patient. Accepts `limit` to restrict how many records to return.  |

## Alerts

| Method & Path                      | Description                                                                                                           |
|------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| `GET /api/alerts/`                 | List recent alerts in descending order of creation time.                                                              |
| `POST /api/alerts/`                | Create a new alert. Provide `patient_id`, `bed_id`, `device_id`, `vital_type`, `value`, `severity`, `category`, and `message`. |
| `POST /api/alerts/{id}/acknowledge` | Acknowledge an alert by ID. Supply an `ack_message` describing why you are acknowledging it. Only unacknowledged alerts can be acknowledged. |

## Real‑time WebSocket

### `GET /ws`

Clients can connect to the WebSocket endpoint at `/ws`. Once connected, the server pushes any new vital measurements to all connected clients. The client should send ping messages periodically to keep the connection alive.

Example using JavaScript:
```js
const socket = new WebSocket("ws://localhost:8000/ws");
socket.onmessage = (event) => {
  const vital = JSON.parse(event.data);
  console.log("Received vital:", vital);
};
socket.onopen = () => {
  // Optionally send a ping every 30 seconds
  setInterval(() => socket.send("ping"), 30000);
};
```

## Errors

Responses use conventional HTTP status codes. If a request fails due to authentication or permission issues the API returns `401` or `403`. Validation errors return `422` and include details in the response body.

For a full Swagger/OpenAPI specification, run the backend and navigate to `/docs` or `/redoc` in your browser. FastAPI automatically generates interactive documentation for all endpoints.

## Admin Endpoints

Only users with appropriate administrative roles (e.g. Super Admin, Hospital Admin) may call these endpoints. They enable management of master data, roles/permissions, users and audit logs.

### Device Types

| Method & Path | Description |
|---------------|-------------|
| `GET /api/admin/device-types` | List all device type masters. |
| `POST /api/admin/device-types` | Create a new device type. Provide `name`, `company`, optional `output_spec` and `adapter_name`. |
| `PATCH /api/admin/device-types/{id}` | Update an existing device type. |

### Roles & Permissions

| Method & Path | Description |
|---------------|-------------|
| `GET /api/admin/permissions` | Return a list of all permission names. |
| `GET /api/admin/roles` | List all roles with their assigned permissions. |
| `POST /api/admin/roles` | Create a new role. Provide `name`, optional `description` and `permission_names` (list of permission names to assign). |
| `PATCH /api/admin/roles/{id}` | Update an existing role’s name, description or permissions. |

### Users

| Method & Path | Description |
|---------------|-------------|
| `POST /api/users` | Create a new user. Requires `username`, `password`, `full_name`, `email` and `role_id`. Only administrators can call this endpoint. |

### Audit Logs

| Method & Path | Description |
|---------------|-------------|
| `GET /api/admin/audit-logs` | Retrieve audit log entries. Supports optional query parameters `model`, `action`, `user_id`, `start_time` and `end_time` to filter results. |

