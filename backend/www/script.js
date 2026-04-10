
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
doHealthCheck();