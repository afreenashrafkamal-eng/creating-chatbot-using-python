CodeCraftHub — REST API Learning Tracker



Project Overview



CodeCraftHub is a beginner-friendly Flask REST API for tracking learning courses. Course information is stored in a JSON file instead of a database.



Features



\- Create a new course.

\- Retrieve all courses or a specific course.

\- Update existing courses.

\- Delete courses.

\- Automatically generate course IDs and creation timestamps.

\- Validate required fields, dates, and statuses.

\- Handle errors such as missing fields and nonexistent courses.



Technologies Used



\- Python 3

\- Flask

\- JSON file storage

\- REST API



Project Structure



\- "app.py" — Contains the Flask application and API endpoints.

\- "requirements.txt" — Lists the required Python packages.

\- "courses.json" — Stores course information and is created automatically.

\- "README.md" — Contains project documentation.



Installation



1\. Install Python 3.



2\. Open Command Prompt.



3\. Navigate to the project folder:

&#x20;  

&#x20;  "cd C:\\Users\\ukama\\codecrafthub"



4\. Install dependencies:

&#x20;  

&#x20;  "python -m pip install -r requirements.txt"



Running the Application



Run this command from the project folder:



"python app.py"



The API will be available at "http://127.0.0.1:5000".



Keep the Command Prompt running while testing.



API Endpoints



Method| Endpoint| Purpose

POST| "/api/courses"| Create a course

GET| "/api/courses"| Retrieve all courses

GET| "/api/courses/1"| Retrieve course ID 1

PUT| "/api/courses/1"| Update course ID 1

DELETE| "/api/courses/1"| Delete course ID 1



Course Fields



\- "id" — Automatically generated ID.

\- "name" — Course name.

\- "description" — Course description.

\- "target\_date" — Completion date in YYYY-MM-DD format.

\- "status" — Not Started, In Progress, or Completed.

\- "created\_at" — Automatically generated timestamp.



Testing



The API was tested locally using Command Prompt and curl.



Tests included:



\- Creating, retrieving, updating, and deleting courses.

\- Checking missing required fields.

\- Checking invalid date formats.

\- Checking invalid status values.

\- Checking nonexistent course IDs.



Error Handling



\- HTTP 400: Invalid input or missing fields.

\- HTTP 404: Course not found.

\- HTTP 500: Server-side or file errors.



Troubleshooting



\- If Python is not recognized, check that Python is installed and available from Command Prompt.

\- If Flask is missing, run "python -m pip install -r requirements.txt".

\- If the API cannot be reached, make sure "python app.py" is still running.

\- If a course is not found, check the course ID.



Learning Outcomes



This project demonstrates REST API endpoints, HTTP methods, CRUD operations, JSON file storage, input validation, and error handling.



Future Improvements



\- Add PATCH for partial updates.

\- Add a web interface.

\- Add automated tests with pytest.

\- Add search and pagination.



Project: CodeCraftHub

Purpose: Learning Python Flask REST API development.

