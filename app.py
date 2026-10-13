from flask import Flask, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

# JSON file used as the "database"
COURSES_FILE = "courses.json"

# Allowed course statuses
ALLOWED_STATUSES = {"Not Started", "In Progress", "Completed"}
DATE_FORMAT = "%Y-%m-%d"  # Expected format for target_date


# ----------------------------
# File handling helpers
# ----------------------------
def ensure_courses_file_exists():
    """
    Make sure courses.json exists.
    If it doesn't, create it with an empty list.
    """
    if not os.path.exists(COURSES_FILE):
        try:
            with open(COURSES_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)
        except OSError as e:
            # If we can't write the file, return a clear error
            raise RuntimeError(f"Could not create {COURSES_FILE}: {e}")


def load_courses():
    """
    Load courses from courses.json.
    Returns a list of course objects.
    """
    ensure_courses_file_exists()
    try:
        with open(COURSES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # We expect a list at the top-level
        return data if isinstance(data, list) else []
    except OSError as e:
        raise RuntimeError(f"Could not read {COURSES_FILE}: {e}")
    except json.JSONDecodeError as e:
        # If the JSON is corrupted, treat as error (safer than silently continuing)
        raise RuntimeError(f"Invalid JSON in {COURSES_FILE}: {e}")


def save_courses(courses):
    """
    Save the given list of courses back into courses.json.
    """
    try:
        with open(COURSES_FILE, "w", encoding="utf-8") as f:
            json.dump(courses, f, indent=2, ensure_ascii=False)
    except OSError as e:
        raise RuntimeError(f"Could not write {COURSES_FILE}: {e}")


# ----------------------------
# Utility helpers
# ----------------------------
def get_next_id(courses):
    """
    Generate the next auto-incrementing integer id starting at 1.
    """
    if not courses:
        return 1
    # Find max existing id; assumes stored courses have correct format
    max_id = max(course.get("id", 0) for course in courses)
    return max_id + 1


def find_course_index(courses, course_id):
    """
    Find the index of a course with a matching id.
    Returns index if found, else None.
    """
    for i, course in enumerate(courses):
        if course.get("id") == course_id:
            return i
    return None


def validate_date(date_str):
    """
    Validate that date_str matches YYYY-MM-DD.
    Returns True if valid; raises ValueError if invalid.
    """
    datetime.strptime(date_str, DATE_FORMAT)  # will raise ValueError if invalid
    return True


def get_json_or_400():
    """
    Ensures request content type is JSON and returns parsed JSON.
    """
    if not request.is_json:
        return None
    return request.get_json(silent=True)


def error_response(status_code, message):
    """
    Standard helper for error responses.
    """
    return jsonify({"error": message}), status_code


# ----------------------------
# Global error handlers
# ----------------------------
@app.errorhandler(RuntimeError)
def handle_runtime_error(err):
    # Used for file read/write issues and other runtime problems
    return error_response(500, str(err))


@app.errorhandler(400)
def handle_400(err):
    return error_response(400, str(err.description) if hasattr(err, "description") else "Bad Request")


@app.errorhandler(404)
def handle_404(err):
    return error_response(404, str(err.description) if hasattr(err, "description") else "Not Found")


# ----------------------------
# API Endpoints
# ----------------------------

# POST /api/courses — Add a new course
@app.post("/api/courses")
def create_course():
    # Read JSON payload
    data = get_json_or_400()
    if data is None:
        return error_response(400, "Request body must be valid JSON.")

    # Required fields
    required_fields = ["name", "description", "target_date", "status"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return error_response(400, f"Missing required fields: {', '.join(missing)}")

    # Validate name/description types (basic checks)
    if not isinstance(data["name"], str) or not data["name"].strip():
        return error_response(400, "Field 'name' must be a non-empty string.")
    if not isinstance(data["description"], str) or not data["description"].strip():
        return error_response(400, "Field 'description' must be a non-empty string.")

    # Validate target_date format
    try:
        validate_date(data["target_date"])
    except ValueError:
        return error_response(400, "Field 'target_date' must be in format YYYY-MM-DD.")

    # Validate status value
    status = data["status"]
    if status not in ALLOWED_STATUSES:
        return error_response(
            400,
            f"Invalid status. Must be one of: {', '.join(sorted(ALLOWED_STATUSES))}"
        )

    # Load existing courses
    courses = load_courses()

    # Create the new course object
    new_course = {
        "id": get_next_id(courses),  # auto-generated
        "name": data["name"].strip(),
        "description": data["description"].strip(),
        "target_date": data["target_date"],
        "status": status,
        "created_at": datetime.utcnow().isoformat() + "Z"  # auto-generated timestamp (UTC)
    }

    # Save it
    courses.append(new_course)
    save_courses(courses)

    return jsonify(new_course), 201


# GET /api/courses — Get all courses
@app.get("/api/courses")
def get_all_courses():
    courses = load_courses()
    return jsonify(courses), 200


# GET /api/courses/<course_id> — Get a specific course
@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    courses = load_courses()
    idx = find_course_index(courses, course_id)

    if idx is None:
        return error_response(404, "Course not found.")

    return jsonify(courses[idx]), 200


# PUT /api/courses/<course_id> — Update a course
@app.put("/api/courses/<int:course_id>")
def update_course(course_id):
    data = get_json_or_400()
    if data is None:
        return error_response(400, "Request body must be valid JSON.")

    # For simplicity (beginner-friendly), require all fields on PUT
    required_fields = ["name", "description", "target_date", "status"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return error_response(400, f"Missing required fields: {', '.join(missing)}")

    # Validate name/description
    if not isinstance(data["name"], str) or not data["name"].strip():
        return error_response(400, "Field 'name' must be a non-empty string.")
    if not isinstance(data["description"], str) or not data["description"].strip():
        return error_response(400, "Field 'description' must be a non-empty string.")

    # Validate target_date
    try:
        validate_date(data["target_date"])
    except ValueError:
        return error_response(400, "Field 'target_date' must be in format YYYY-MM-DD.")

    # Validate status
    status = data["status"]
    if status not in ALLOWED_STATUSES:
        return error_response(
            400,
            f"Invalid status. Must be one of: {', '.join(sorted(ALLOWED_STATUSES))}"
        )

    courses = load_courses()
    idx = find_course_index(courses, course_id)

    if idx is None:
        return error_response(404, "Course not found.")

    # Update course (keep created_at and id unchanged)
    created_at = courses[idx].get("created_at")
    courses[idx] = {
        "id": course_id,
        "name": data["name"].strip(),
        "description": data["description"].strip(),
        "target_date": data["target_date"],
        "status": status,
        "created_at": created_at
    }

    save_courses(courses)
    return jsonify(courses[idx]), 200


# DELETE /api/courses/<course_id> — Delete a course
@app.delete("/api/courses/<int:course_id>")
def delete_course(course_id):
    courses = load_courses()
    idx = find_course_index(courses, course_id)

    if idx is None:
        return error_response(404, "Course not found.")

    removed = courses.pop(idx)
    save_courses(courses)

    # Return a helpful message + the deleted object
    return jsonify({"message": "Course deleted.", "deleted": removed}), 200


# ----------------------------
# Run the server
# ----------------------------
if __name__ == "__main__":
    # This ensures courses.json is created immediately on startup.
    ensure_courses_file_exists()
    app.run(host="127.0.0.1", port=5000, debug=True)