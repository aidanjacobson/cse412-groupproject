const API = "/api";

function formatTime(ts) {
    if (!ts) return "";
    return new Date(ts).toLocaleString();
}

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
