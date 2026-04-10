# API Routes Documentation

This document outlines all API endpoints for the Event Manager application.

---

## IMPORTANT: HTTP Status Codes

**You MUST return the correct HTTP status code for every response.** The frontend will check these codes.

| Code | When to Use |
|------|-------------|
| **200** | Success — request worked (GET, POST, PUT, DELETE all return 200 on success) |
| **400** | Bad Request — missing required fields, invalid data, resource not found |

That's it. Only use 200 and 400.

---

## Base URL
```
http://localhost:8080/api
```
Meaning all api routes should be prefixed with `/api`.

---

## Departments (Read-Only for Frontend)

### GET /departments
Get all departments (for dropdown in event forms).

**Status Code:** `200` on success

**Response:**
```json
[
  {
    "departmentid": 1,
    "name": "W. P. Carey School of Business",
    "contactemail": "wpcadmissions@asu.edu",
    "phonenumber": "480-965-5187",
    "website": "https://wpcarey.asu.edu/"
  }
]
```

---

## Locations (Read-Only for Frontend)

### GET /locations
Get all locations (for dropdown in event forms).

**Status Code:** `200` on success

**Response:**
```json
[
  {
    "locationid": 1,
    "address": "400 E. Apache Blvd"
  }
]
```

---

## Categories (Read-Only for Frontend)

### GET /categories
Get all categories (for checkboxes in event forms).

**Status Code:** `200` on success

**Response:**
```json
[
  {
    "categoryid": 1,
    "categoryname": "Breakfast Mixer"
  }
]
```

---

## Events (Full CRUD)

### GET /events
Get all events.

**Status Code:** `200` on success

**Response:**
```json
[
  {
    "eventid": 1,
    "eventname": "Vintage Thrift",
    "description": "Come take a look at the great selection of vintage clothing at cheap prices",
    "starttime": "2025-04-01T09:00:00",
    "endtime": "2025-04-01T13:00:00",
    "departmentid": 1,
    "locationid": 1,
    "categories": [10]
  }
]
```

---

### GET /events/{id}
Get a specific event by ID.

**Parameters:**
- `id` (path, required): Event ID

**Status Code:** `200` on success, `400` if not found

**Response (200):**
```json
{
  "eventid": 1,
  "eventname": "Vintage Thrift",
  "description": "Come take a look at the great selection of vintage clothing at cheap prices",
  "starttime": "2025-04-01T09:00:00",
  "endtime": "2025-04-01T13:00:00",
  "departmentid": 1,
  "locationid": 1,
  "categories": [10]
}
```

**Response (400):** Event not found

---

### POST /events
Create a new event.

**Status Code:** `200` on success, `400` if validation fails

**Request Body:**
```json
{
  "eventname": "New Event",
  "description": "Event description here",
  "starttime": "2025-05-01T10:00:00",
  "endtime": "2025-05-01T12:00:00",
  "departmentid": 1,
  "locationid": 1,
  "categories": [1, 3]
}
```

**Response (201):**
```json
{
  "eventid": 21,
  "eventname": "New Event",
  "description": "Event description here",
  "starttime": "2025-05-01T10:00:00",
  "endtime": "2025-05-01T12:00:00",
  "departmentid": 1,
  "locationid": 1,
  "categories": [1, 3]
}
```

---

### PUT /events/{id}
Update an event.

**Status Code:** `200` on success, `400` if validation fails or event not found

**Parameters:**
- `id` (path, required): Event ID

**Request Body:** (all fields optional)
```json
{
  "eventname": "Updated Event Name",
  "description": "Updated description",
  "starttime": "2025-05-01T10:00:00",
  "endtime": "2025-05-01T13:00:00",
  "departmentid": 2,
  "locationid": 3,
  "categories": [1, 2]
}
```

**Response (200):**
```json
{
  "eventid": 1,
  "eventname": "Updated Event Name",
  "description": "Updated description",
  "starttime": "2025-05-01T10:00:00",
  "endtime": "2025-05-01T13:00:00",
  "departmentid": 2,
  "locationid": 3,
  "categories": [1, 2]
}
```

**Response (400):** Event not found

---

### DELETE /events/{id}
Delete an event.

**Status Code:** `200` on success, `400` if event not found

**Parameters:**
- `id` (path, required): Event ID

**Response (200):** Success

**Response (400):** Event not found

---

## Error Responses

All endpoints may return:

### 400 Bad Request
```json
{
  "error": "Invalid request data",
  "details": "Field 'eventname' is required"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Backend Checklist (Before Submitting)

Run `python test.py` and verify:

- [ ] GET /events returns `200` with event list
- [ ] GET /events/{id} returns `200` with event data, or `400` if not found
- [ ] POST /events returns `200` with created event data, or `400` on error
- [ ] PUT /events/{id} returns `200` with updated event data, or `400` on error
- [ ] DELETE /events/{id} returns `200` on success, or `400` if not found
- [ ] GET /categories returns `200` with category list
- [ ] GET /departments returns `200` with department list
- [ ] GET /locations returns `200` with location list
- [ ] No console errors when running test

**Only use status codes 200 and 400. Nothing else.**

---

## Notes

- All timestamps are in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
- Event IDs are auto-generated
- `categories` is a list of category IDs; passed in POST/PUT requests and returned in GET responses
