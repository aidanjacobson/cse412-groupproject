# Front-End Development Guide

**Deadline:** 4/22/2026  
**Tech Stack:** HTML5, CSS3, JavaScript (vanilla or framework)  
**Location:** `backend/www/`  
**Base API URL:** `http://localhost:8080/api`

---

## Scope: Events Only

This project focuses on **Events** as the primary entity. Departments, Locations, and Categories are read-only (for dropdowns/display).

---

## Developer 1: CREATE and UPDATE

Build forms for creating and updating events.

### Pages to Create

1. **create-event.html** — Form to create new events
2. **update-event.html** — Form to update existing events

### Requirements

- All required fields must be validated before submission
- Use `POST /api/events` for create
- Use `PUT /api/events/{id}` for update
- Dropdowns must fetch fresh data:
  - GET `/api/departments` → populate Department dropdown
  - GET `/api/locations` → populate Location dropdown
  - GET `/api/categories` → populate Categories multi-select/checkboxes
- Show success/error messages
- On success, redirect to `events.html`

### Form Fields

- Event Name (required)
- Description (optional)
- Start Time (required, datetime)
- End Time (required, datetime)
- Department (required, dropdown)
- Location (required, dropdown)
- Categories (optional, multi-select/checkboxes)

---

## Developer 2: READ and DELETE

Build pages for listing, viewing, and deleting events.

### Pages to Create

1. **index.html** — Home page with navigation
2. **events.html** — List all events (table or cards)
3. **event-details.html** — Show details for a single event

### Requirements

**events.html:**
- Fetch `GET /api/events` on page load
- Display events in a table or card layout
- Columns: Event Name, Start Time, End Time, Department, Location, Actions
- Include "View Details" link (→ event-details.html?id=X)
- Include "Edit" button (→ update-event.html?id=X)
- Include "Delete" button with confirmation dialog
- Delete uses `DELETE /api/events/{id}`
- Include "New Event" button (→ create-event.html)
- Show loading state while fetching

**event-details.html?id=X:**
- Fetch `GET /api/events/{id}` on load
- Display all event information (name, description, times, department, location, categories)
- Include "Edit" button (→ update-event.html?id=X)
- Include "Delete" button with confirmation
- Include "Back to Events" link

**index.html:**
- Navigation bar with link to events.html
- Simple home page with link to "View All Events"

---

## Page Navigation

```
index.html
  └─ Link to → events.html

events.html
  ├─ "New Event" button → create-event.html
  ├─ Event row → click to event-details.html?id=X
  ├─ "Edit" button → update-event.html?id=X
  └─ "Delete" button → confirmation → DELETE /api/events/{id}

event-details.html?id=X
  ├─ "Edit" button → update-event.html?id=X
  ├─ "Back to Events" → events.html
  └─ "Delete" button → confirmation → DELETE /api/events/{id}

create-event.html
  └─ Form submits → POST /api/events → redirect to events.html

update-event.html?id=X
  ├─ Fetch GET /api/events/{id} to pre-populate form
  └─ Form submits → PUT /api/events/{id} → redirect to event-details.html?id=X
```

---

## Shared Responsibilities

Both developers implement:

- **Navigation bar** — At top of all pages, links to index.html and events.html
- **Loading state** — Show while fetching data
- **Error handling** — Display API error messages
- **Delete confirmation** — "Are you sure?" dialog before deleting

---

## Testing

Before submitting:
- [ ] All pages load without console errors
- [ ] Forms validate required fields
- [ ] Create event inserts into database
- [ ] Update event modifies database
- [ ] Delete event removes from database
- [ ] List pages refresh after create/update/delete
- [ ] All navigation links work

---

## Reference

- API routes: `ROUTES.md`
- Database schema: `db_init.sql`
- Test backend: `python test.py`
