from datetime import datetime, timedelta
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.database_service import DatabaseService


def test_database_service():
    """Test all DatabaseService methods"""
    db = DatabaseService()

    print("=" * 50)
    print("TESTING DATABASE SERVICE")
    print("=" * 50)

    try:
        # TEST DEPARTMENTS
        print("\n--- DEPARTMENTS ---")
        print("Creating departments...")
        dept1_id = db.create_department(
            name="Test Department 1",
            contactemail="test1@example.com",
            phonenumber="123-456-7890",
            website="https://test1.com"
        )
        print(f"Created department with ID: {dept1_id}")

        dept2_id = db.create_department(
            name="Test Department 2",
            contactemail="test2@example.com",
            phonenumber="098-765-4321"
        )
        print(f"Created department with ID: {dept2_id}")

        print("Getting all departments...")
        departments = db.get_all_departments()
        for dept in departments[:3]:  # Show first 3
            print(f"  - {dept.departmentid}: {dept.name}")

        print(f"Getting department by ID {dept1_id}...")
        dept = db.get_department_by_id(dept1_id)
        print(f"  Found: {dept}")

        print(f"Updating department {dept1_id}...")
        db.update_department(dept1_id, website="https://updated.com")
        updated_dept = db.get_department_by_id(dept1_id)
        print(f"  Updated: {updated_dept}")

        # TEST LOCATIONS
        print("\n--- LOCATIONS ---")
        print("Creating locations...")
        loc1_id = db.create_location(address="123 Main St, Suite 100")
        print(f"Created location with ID: {loc1_id}")

        loc2_id = db.create_location(address="456 Oak Ave, Building B")
        print(f"Created location with ID: {loc2_id}")

        print("Getting all locations...")
        locations = db.get_all_locations()
        for loc in locations[:3]:
            print(f"  - {loc.locationid}: {loc.address}")

        print(f"Getting location by ID {loc1_id}...")
        loc = db.get_location_by_id(loc1_id)
        print(f"  Found: {loc}")

        print(f"Updating location {loc1_id}...")
        db.update_location(loc1_id, address="123 Main St, Suite 200")
        updated_loc = db.get_location_by_id(loc1_id)
        print(f"  Updated: {updated_loc}")

        # TEST CATEGORIES
        print("\n--- CATEGORIES ---")
        print("Creating categories...")
        cat1_id = db.create_category(categoryname="Test Workshop")
        print(f"Created category with ID: {cat1_id}")

        cat2_id = db.create_category(categoryname="Test Seminar")
        print(f"Created category with ID: {cat2_id}")

        print("Getting all categories...")
        categories = db.get_all_categories()
        for cat in categories[:3]:
            print(f"  - {cat.categoryid}: {cat.categoryname}")

        print(f"Getting category by ID {cat1_id}...")
        cat = db.get_category_by_id(cat1_id)
        print(f"  Found: {cat}")

        print(f"Updating category {cat1_id}...")
        db.update_category(cat1_id, categoryname="Updated Workshop")
        updated_cat = db.get_category_by_id(cat1_id)
        print(f"  Updated: {updated_cat}")

        # TEST EVENTS
        print("\n--- EVENTS ---")
        print("Creating events...")
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=2)

        event1_id = db.create_event(
            eventname="Test Event 1",
            description="This is a test event",
            starttime=start_time,
            endtime=end_time,
            departmentid=dept1_id,
            locationid=loc1_id,
            categories=[cat1_id, cat2_id]
        )
        print(f"Created event with ID: {event1_id}")

        start_time2 = datetime.now() + timedelta(days=1)
        end_time2 = start_time2 + timedelta(hours=3)
        event2_id = db.create_event(
            eventname="Test Event 2",
            description="Another test event",
            starttime=start_time2,
            endtime=end_time2,
            departmentid=dept2_id,
            locationid=loc2_id,
            categories=[cat1_id]
        )
        print(f"Created event with ID: {event2_id}")

        print("Getting all events...")
        events = db.get_all_events()
        for event in events[:3]:
            print(f"  - {event.eventid}: {event.eventname} (categories: {event.categories})")

        print(f"Getting event by ID {event1_id}...")
        event = db.get_event_by_id(event1_id)
        print(f"  Found: {event}")

        print(f"Updating event {event1_id}...")
        db.update_event(event1_id, eventname="Updated Test Event 1", description="Updated description")
        updated_event = db.get_event_by_id(event1_id)
        print(f"  Updated: {updated_event}")

        # TEST EVENT-CATEGORY RELATIONSHIPS
        print("\n--- EVENT-CATEGORY RELATIONSHIPS ---")
        print(f"Getting categories for event {event1_id}...")
        categories = db.get_event_categories(event1_id)
        print(f"  Categories: {categories}")

        print(f"Adding category {cat2_id} to event {event2_id}...")
        db.add_event_category(event2_id, cat2_id)
        updated_cats = db.get_event_categories(event2_id)
        print(f"  Updated categories: {updated_cats}")

        print(f"Removing category {cat1_id} from event {event2_id}...")
        db.remove_event_category(event2_id, cat1_id)
        updated_cats = db.get_event_categories(event2_id)
        print(f"  Updated categories: {updated_cats}")

        print(f"Setting categories for event {event2_id} to [...]...")
        db.set_event_categories(event2_id, [cat1_id, cat2_id])
        updated_cats = db.get_event_categories(event2_id)
        print(f"  Categories: {updated_cats}")

        # TEST DELETES
        print("\n--- DELETIONS ---")
        print(f"Deleting event {event1_id}...")
        result = db.delete_event(event1_id)
        print(f"  Deleted: {result}")

        print(f"Deleting event {event2_id}...")
        result = db.delete_event(event2_id)
        print(f"  Deleted: {result}")

        print(f"Deleting category {cat1_id}...")
        result = db.delete_category(cat1_id)
        print(f"  Deleted: {result}")

        print(f"Deleting category {cat2_id}...")
        result = db.delete_category(cat2_id)
        print(f"  Deleted: {result}")

        print(f"Deleting location {loc1_id}...")
        result = db.delete_location(loc1_id)
        print(f"  Deleted: {result}")

        print(f"Deleting location {loc2_id}...")
        result = db.delete_location(loc2_id)
        print(f"  Deleted: {result}")

        print(f"Deleting department {dept1_id}...")
        result = db.delete_department(dept1_id)
        print(f"  Deleted: {result}")

        print(f"Deleting department {dept2_id}...")
        result = db.delete_department(dept2_id)
        print(f"  Deleted: {result}")

        print("\n" + "=" * 50)
        print("ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 50)

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_database_service()
