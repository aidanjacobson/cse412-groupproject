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
                

                <button class="edit-btn" onclick="editEvent()">Edit</button>
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
