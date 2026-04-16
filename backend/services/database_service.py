import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
from datetime import datetime
import os

from models.department import Department
from models.location import Location
from models.category import Category
from models.event import Event


def _datetime_to_timestamp(dt: datetime) -> int:
    """Convert datetime to milliseconds since epoch (JavaScript compatible)"""
    if dt is None:
        return None
    return int(dt.timestamp() * 1000)


def _timestamp_to_datetime(timestamp_ms: int) -> datetime:
    """Convert milliseconds since epoch to datetime"""
    if timestamp_ms is None:
        return None
    return datetime.fromtimestamp(timestamp_ms / 1000)


class DatabaseService:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(
                host=os.environ.get("POSTGRES_HOST", "localhost"),
                database=os.environ.get("POSTGRES_DB", "eventdb"),
                user=os.environ.get("POSTGRES_USER", "postgres"),
                password=os.environ.get("POSTGRES_PASSWORD", "postgres"),
                port=os.environ.get("POSTGRES_PORT", "5432"),
            )
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def _execute_query(self, query: str, params: tuple = ()):
        """Execute a query and return results"""
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            raise

    def _execute_update(self, query: str, params: tuple = ()):
        """Execute an update/insert/delete query"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                self.conn.commit()
                return cursor.rowcount
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Database error: {e}")
            raise

    # DEPARTMENTS CRUD
    def get_all_departments(self) -> List[Department]:
        """Get all departments"""
        query = "SELECT * FROM Departments ORDER BY DepartmentID"
        results = self._execute_query(query)
        return [Department(**row) for row in results]

    def get_department_by_id(self, department_id: int) -> Optional[Department]:
        """Get a department by ID"""
        query = "SELECT * FROM Departments WHERE DepartmentID = %s"
        results = self._execute_query(query, (department_id,))
        return Department(**results[0]) if results else None

    def create_department(
        self, name: str, contactemail: str, phonenumber: Optional[str] = None, website: Optional[str] = None
    ) -> int:
        """Create a new department"""
        query = (
            "INSERT INTO Departments (Name, ContactEmail, PhoneNumber, Website) "
            "VALUES (%s, %s, %s, %s) RETURNING DepartmentID"
        )
        with self.conn.cursor() as cursor:
            cursor.execute(query, (name, contactemail, phonenumber, website))
            self.conn.commit()
            return cursor.fetchone()[0]

    def update_department(
        self,
        department_id: int,
        name: Optional[str] = None,
        contactemail: Optional[str] = None,
        phonenumber: Optional[str] = None,
        website: Optional[str] = None,
    ) -> bool:
        """Update a department"""
        updates = []
        params = []

        if name is not None:
            updates.append("Name = %s")
            params.append(name)
        if contactemail is not None:
            updates.append("ContactEmail = %s")
            params.append(contactemail)
        if phonenumber is not None:
            updates.append("PhoneNumber = %s")
            params.append(phonenumber)
        if website is not None:
            updates.append("Website = %s")
            params.append(website)

        if not updates:
            return False

        params.append(department_id)
        query = f"UPDATE Departments SET {', '.join(updates)} WHERE DepartmentID = %s"
        self._execute_update(query, tuple(params))
        return True

    def delete_department(self, department_id: int) -> bool:
        """Delete a department"""
        query = "DELETE FROM Departments WHERE DepartmentID = %s"
        rowcount = self._execute_update(query, (department_id,))
        return rowcount > 0

    # LOCATIONS CRUD
    def get_all_locations(self) -> List[Location]:
        """Get all locations"""
        query = "SELECT * FROM Locations ORDER BY LocationID"
        results = self._execute_query(query)
        return [Location(**row) for row in results]

    def get_location_by_id(self, location_id: int) -> Optional[Location]:
        """Get a location by ID"""
        query = "SELECT * FROM Locations WHERE LocationID = %s"
        results = self._execute_query(query, (location_id,))
        return Location(**results[0]) if results else None

    def create_location(self, address: str) -> int:
        """Create a new location"""
        query = "INSERT INTO Locations (Address) VALUES (%s) RETURNING LocationID"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (address,))
            self.conn.commit()
            return cursor.fetchone()[0]

    def update_location(self, location_id: int, address: str) -> bool:
        """Update a location"""
        query = "UPDATE Locations SET Address = %s WHERE LocationID = %s"
        rowcount = self._execute_update(query, (address, location_id))
        return rowcount > 0

    def delete_location(self, location_id: int) -> bool:
        """Delete a location"""
        query = "DELETE FROM Locations WHERE LocationID = %s"
        rowcount = self._execute_update(query, (location_id,))
        return rowcount > 0

    # CATEGORIES CRUD
    def get_all_categories(self) -> List[Category]:
        """Get all categories"""
        query = "SELECT * FROM Categories ORDER BY CategoryID"
        results = self._execute_query(query)
        return [Category(**row) for row in results]

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Get a category by ID"""
        query = "SELECT * FROM Categories WHERE CategoryID = %s"
        results = self._execute_query(query, (category_id,))
        return Category(**results[0]) if results else None

    def create_category(self, categoryname: str) -> int:
        """Create a new category"""
        query = "INSERT INTO Categories (CategoryName) VALUES (%s) RETURNING CategoryID"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (categoryname,))
            self.conn.commit()
            return cursor.fetchone()[0]

    def update_category(self, category_id: int, categoryname: str) -> bool:
        """Update a category"""
        query = "UPDATE Categories SET CategoryName = %s WHERE CategoryID = %s"
        rowcount = self._execute_update(query, (categoryname, category_id))
        return rowcount > 0

    def delete_category(self, category_id: int) -> bool:
        """Delete a category"""
        query = "DELETE FROM Categories WHERE CategoryID = %s"
        rowcount = self._execute_update(query, (category_id,))
        return rowcount > 0

    # EVENTS CRUD
    def get_all_events(self) -> List[Event]:
        """Get all events"""
        query = "SELECT * FROM Events ORDER BY EventID"
        results = self._execute_query(query)
        events = []
        for row in results:
            row['starttime'] = _datetime_to_timestamp(row['starttime'])
            row['endtime'] = _datetime_to_timestamp(row['endtime'])
            event = Event(**row)
            event.categories = self.get_event_categories(event.eventid)
            events.append(event)
        return events

    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        """Get an event by ID"""
        query = "SELECT * FROM Events WHERE EventID = %s"
        results = self._execute_query(query, (event_id,))
        if results:
            row = results[0]
            row['starttime'] = _datetime_to_timestamp(row['starttime'])
            row['endtime'] = _datetime_to_timestamp(row['endtime'])
            event = Event(**row)
            event.categories = self.get_event_categories(event_id)
            return event
        return None

    def create_event(
        self,
        eventname: str,
        description: Optional[str],
        starttime: int,
        endtime: int,
        departmentid: int,
        locationid: int,
        categories: Optional[List[int]] = None,
    ) -> int:
        """Create a new event"""
        try:
            # Convert timestamps to datetime for database storage
            starttime_dt = _timestamp_to_datetime(starttime)
            endtime_dt = _timestamp_to_datetime(endtime)
            
            if starttime_dt is None or endtime_dt is None:
                raise ValueError("Invalid timestamps provided")
            
            query = (
                "INSERT INTO Events (EventName, Description, StartTime, EndTime, DepartmentID, LocationID) "
                "VALUES (%s, %s, %s, %s, %s, %s) RETURNING EventID"
            )
            
            event_id = None
            with self.conn.cursor() as cursor:
                cursor.execute(query, (eventname, description, starttime_dt, endtime_dt, departmentid, locationid))
                result = cursor.fetchone()
                
                if not result:
                    raise RuntimeError("Failed to insert event")
                    
                event_id = result[0]

                # Add categories if provided
                if categories:
                    for category_id in categories:
                        category_query = "INSERT INTO EventCategories (EventID, CategoryID) VALUES (%s, %s)"
                        cursor.execute(category_query, (event_id, category_id))

            # Commit after cursor is closed
            self.conn.commit()
            return event_id
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Database error creating event: {e}")
            raise
        except Exception as e:
            self.conn.rollback()
            print(f"Error creating event: {e}")
            raise

    def update_event(
        self,
        event_id: int,
        eventname: Optional[str] = None,
        description: Optional[str] = None,
        starttime: Optional[int] = None,
        endtime: Optional[int] = None,
        departmentid: Optional[int] = None,
        locationid: Optional[int] = None,
    ) -> bool:
        """Update an event"""
        updates = []
        params = []

        if eventname is not None:
            updates.append("EventName = %s")
            params.append(eventname)
        if description is not None:
            updates.append("Description = %s")
            params.append(description)
        if starttime is not None:
            updates.append("StartTime = %s")
            params.append(_timestamp_to_datetime(starttime))
        if endtime is not None:
            updates.append("EndTime = %s")
            params.append(_timestamp_to_datetime(endtime))
        if departmentid is not None:
            updates.append("DepartmentID = %s")
            params.append(departmentid)
        if locationid is not None:
            updates.append("LocationID = %s")
            params.append(locationid)

        if not updates:
            return False

        params.append(event_id)
        query = f"UPDATE Events SET {', '.join(updates)} WHERE EventID = %s"
        rowcount = self._execute_update(query, tuple(params))
        return rowcount > 0

    def delete_event(self, event_id: int) -> bool:
        """Delete an event"""
        with self.conn.cursor() as cursor:
            # Delete related categories first
            cursor.execute("DELETE FROM EventCategories WHERE EventID = %s", (event_id,))
            # Delete event
            cursor.execute("DELETE FROM Events WHERE EventID = %s", (event_id,))
            self.conn.commit()
            return cursor.rowcount > 0

    # EVENT CATEGORIES CRUD
    def get_event_categories(self, event_id: int) -> List[int]:
        """Get all category IDs for an event"""
        query = "SELECT CategoryID FROM EventCategories WHERE EventID = %s ORDER BY CategoryID"
        results = self._execute_query(query, (event_id,))
        return [row["categoryid"] for row in results]

    def add_event_category(self, event_id: int, category_id: int) -> bool:
        """Add a category to an event"""
        query = "INSERT INTO EventCategories (EventID, CategoryID) VALUES (%s, %s)"
        try:
            self._execute_update(query, (event_id, category_id))
            return True
        except psycopg2.Error:
            return False

    def remove_event_category(self, event_id: int, category_id: int) -> bool:
        """Remove a category from an event"""
        query = "DELETE FROM EventCategories WHERE EventID = %s AND CategoryID = %s"
        rowcount = self._execute_update(query, (event_id, category_id))
        return rowcount > 0

    def set_event_categories(self, event_id: int, category_ids: List[int]) -> bool:
        """Set all categories for an event (replaces existing)"""
        with self.conn.cursor() as cursor:
            # Delete existing categories
            cursor.execute("DELETE FROM EventCategories WHERE EventID = %s", (event_id,))
            # Add new categories
            for category_id in category_ids:
                cursor.execute("INSERT INTO EventCategories (EventID, CategoryID) VALUES (%s, %s)", (event_id, category_id))
            self.conn.commit()
            return True
