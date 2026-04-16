from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from services.database_service import DatabaseService


class Server:
    def __init__(self):
        self.app = FastAPI()
        self.db = DatabaseService()

        self._setup_routes()
        self._ensure_www()
        self._setup_static()

    def _ensure_www(self):
        os.makedirs("backend/www", exist_ok=True)

    def _setup_static(self):
        self.app.mount("/", StaticFiles(directory="backend/www", html=True), name="static")

    def _setup_routes(self):
        """Setup all API routes"""

        @self.app.get("/api/health")
        async def health_check():
            return JSONResponse(content={"status": "ok"})
        

        @self.app.get("/api/departments")
        async def get_departments():
            data = self.db.get_all_departments()
            return JSONResponse(content=[d.__dict__ for d in data])
        
        
        @self.app.get("/api/locations")
        def get_locations():
            data = self.db.get_all_locations()
            return JSONResponse(content=[l.__dict__ for l in data])
        

        @self.app.get("/api/categories")
        def get_categories():
            data = self.db.get_all_categories()
            return JSONResponse(content=[c.__dict__ for c in data])
        

        @self.app.get("/api/events")
        def get_events():
            data = self.db.get_all_events()
            return JSONResponse(content=[e.__dict__ for e in data])
        

        @self.app.get("/api/events/{event_id}")
        def get_event(event_id: int):
            event = self.db.get_event_by_id(event_id)
            if not event:
                return JSONResponse(content={"error": "Event not found"})
            return JSONResponse(status_code=200, content=event.__dict__)
        

        @self.app.post("/api/events")
        async def create_event(request: Request):
            body = await request.json()
            try:
                event_id = self.db.create_event(
                    eventname=body["eventname"],
                    description=body.get("description"),
                    starttime=body["starttime"],
                    endtime=body["endtime"],
                    departmentid=body["departmentid"],
                    locationid=body["locationid"],
                    categories=body.get("categories", [])
                )
            except Exception:
                return JSONResponse(content={"error": "Invalid request data"})

            created = self.db.get_event_by_id(event_id)
            return JSONResponse(content=created.__dict__)
        

        @self.app.put("/api/events/{event_id}")
        async def update_event(event_id: int, request: Request):
            body = await request.json()
            event = self.db.get_event_by_id(event_id)
            if not event:
                return JSONResponse(content={"error": "Event not found"})

            self.db.update_event(
                event_id=event_id,
                eventname=body.get("eventname"),
                description=body.get("description"),
                starttime=body.get("starttime"),
                endtime=body.get("endtime"),
                departmentid=body.get("departmentid"),
                locationid=body.get("locationid"),
            )

            updated = self.db.get_event_by_id(event_id)
            return JSONResponse(content=updated.__dict__)
        

        @self.app.delete("/api/events/{event_id}")
        def delete_event(event_id: int):
            event = self.db.get_event_by_id(event_id)
            if not event:
                return JSONResponse(content={"error": "Event not found"})

            self.db.delete_event(event_id)
            return JSONResponse(content={"success": True})


        # MORE ROUTES GO HERE
        # @self.app.get("/api/some_endpoint")
        # async def some_endpoint():
        #     return JSONResponse(content={"message": "This is some endpoint"})

    def run(self):
        port = int(os.environ.get("PORT", 8080))

        uvicorn.run(
            self.app,
            host="0.0.0.0",
            port=port,
            log_level="info",
        )