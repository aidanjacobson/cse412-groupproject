/*
async function doHealthCheck() {
    // hit /api/health and log the response
    try {
        const response = await fetch("/api/health");
        const data = await response.json();

        // if {status: "ok"} then log "Backend is connected"
        if (data.status === "ok") {
            console.log("Backend is connected and healthy");
        } else {
            console.log("Backend is connected but not healthy:", data);
        }

    } catch (error) {
        console.log("Could not connect to backend:", error);
    }
}

console.log("Hello from script.js!");
doHealthCheck(); */

const API = "/api";

function formatTime(ts) {
    if (!ts) return "";
    return new Date(ts).toLocaleString();
}

//events page
async function loadEvents() {
    const loading = document.getElementById("loading");
    loading.style.display = "block";

    try {
        const res = await fetch(`${API}/events`);
        const data = await res.json();

        const table = document.getElementById("eventsTable");
        table.innerHTML = "";

        data.forEach(event => {
            table.innerHTML += `
                <tr>
                    <td>${event.eventname}</td>
                    <td>${formatTime(event.starttime)}</td>
                    <td>${formatTime(event.endtime)}</td>
                    <td>
                        <button onclick="viewEvent(${event.eventid})">View</button>
                        <button onclick="editEvent(${event.eventid})">Edit</button>
                        <button onclick="deleteEvent(${event.eventid})">Delete</button>
                    </td>
                </tr>
            `;
        });

    } catch (err) {
        alert("Error loading events");
        console.error(err);
    }

    loading.style.display = "none";
}

function viewEvent(id) {
    window.location.href = `event-details.html?id=${id}`;
}

function editEvent(id) {
    window.location.href = `update-event.html?id=${id}`;
}

function goToCreate() {
    window.location.href = "create-event.html";
}

async function deleteEvent(id) {
    if (!confirm("Are you sure you want to delete this event?")) return;

    try {
        await fetch(`${API}/events/${id}`, {
            method: "DELETE"
        });

        loadEvents(); //refresh list

    } catch (err) {
        alert("Delete failed");
        console.error(err);
    }
}

//event details page

async function loadEventDetails() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    const loading = document.getElementById("loading");
    loading.style.display = "block";

    try {
        const res = await fetch(`${API}/events/${id}`);
        const event = await res.json();

        if (event.error) {
            document.getElementById("details").innerHTML = "<p>Event not found</p>";
            return;
        }

        const depRes = await fetch(`${API}/departments`); 
        const departments = await depRes.json();
        const locRes = await fetch(`${API}/locations`);
        const locations = await locRes.json();
        //matching 
        const department = departments.find(d => d.departmentid === event.departmentid);
        const location = locations.find(l => l.locationid === event.locationid);


        document.getElementById("details").innerHTML = `
            <div class="ed">
                <h1>${event.eventname}</h1>
                <p>${event.description || ""}</p>

                <p><strong>Start:</strong> ${formatTime(event.starttime)}</p>
                <p><strong>End:</strong> ${formatTime(event.endtime)}</p>
                <p><strong>Department:</strong> ${department ? department.name : "Unknown"}</p>
                <p><strong>Location:</strong> ${location ? location.address : "Unknown"}</p>
                

                <button class="edit-btn" onclick="editEvent(${event.eventid})">Edit</button>
                <button class="delete-btn" onclick="deleteEventDisplay(${event.eventid})">Delete</button> 
            </div>
        `;

    } catch (err) {
        alert("Error loading event");
        console.error(err);
    }

    loading.style.display = "none";
}
//delete event-details redirects to events list page
async function deleteEventDisplay(id) {
    if (!confirm("Are you sure you want to delete this event?")) return;

    try {
        await fetch(`${API}/events/${id}`, {
            method: "DELETE"
        });

        //redirect after delete
        window.location.href = "events.html";

    } catch (err) {
        alert("Delete failed");
        console.error(err);
    }
}

//create event 
function setupCreate() {
    const form = document.getElementById("createForm");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        //build event object from input data
        const data = {
            eventname: document.getElementById("eventname").value,
            description: document.getElementById("description").value,
            starttime: document.getElementById("starttime").value,
            endtime: document.getElementById("endtime").value,
            departmentid: Number(document.getElementById("departmentid").value),
            locationid: Number(document.getElementById("locationid").value)
        };

        try {
            await fetch(`${API}/events`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            //redirect user back to events list
            document.getElementById("message").textContent = "Event created!";
            window.location.href = "events.html";

        } catch (err) {
            alert("Create failed");
            console.error(err);
        }
    });
}

async function loadExistingEvent(id) {
    try {
        const res = await fetch(`${API}/events/${id}`);
        if (!res.ok) {
            throw new Error(`Failed to load event: ${res.status}`);
        }
        const event = await res.json();
        const start = event.starttime ? new Date(event.starttime) : null;
        const end = event.endtime ? new Date(event.endtime) : null;
        const startOffset = start ? start.getTimezoneOffset() : 0;
        const endOffset = end ? end.getTimezoneOffset() : 0;

        document.getElementById("eventname").value = event.eventname;
        document.getElementById("description").value = event.description;
        document.getElementById("starttime").value = start
            ? new Date(start.getTime() - startOffset * 60000).toISOString().slice(0, 16)
            : "";
        document.getElementById("endtime").value = end
            ? new Date(end.getTime() - endOffset * 60000).toISOString().slice(0, 16)
            : "";
        document.getElementById("departmentid").value = event.departmentid;
        document.getElementById("locationid").value = event.locationid;

    } catch (err) {
        alert("Failed to load event");
        console.error(err);
    }
}

//update
function setupUpdate() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    if (!id) {
        alert("Missing event id");
        window.location.href = "events.html";
        return;
    }

    loadExistingEvent(id);

    const form = document.getElementById("updateForm");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const startValue = document.getElementById("starttime").value;
        const endValue = document.getElementById("endtime").value;

        const data = {
            eventname: document.getElementById("eventname").value,
            description: document.getElementById("description").value,
            starttime: startValue ? new Date(startValue).getTime() : null,
            endtime: endValue ? new Date(endValue).getTime() : null,
            departmentid: Number(document.getElementById("departmentid").value),
            locationid: Number(document.getElementById("locationid").value)
        };

        try {
            const res = await fetch(`${API}/events/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (!res.ok) {
                throw new Error(`Update failed: ${res.status}`);
            }

            document.getElementById("message").textContent = "Event updated!";
            window.location.href = "events.html";

        } catch (err) {
            alert("Update failed");
            console.error(err);
        }
    });
}
