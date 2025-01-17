 
Firewall Test Tool
==================

This application provides a web-based interface to manage and test operations using the Caldera platform. It supports running operations, checking their status, and generating reports.

Features
--------

*   Run and manage operations against a Caldera server.
*   Generate HTML reports of operations.
*   Reset the application state by removing test files.

Requirements
------------

*   Python 3.x
*   Flask
*   pydantic
*   requests
*   flask-cors
*   dotenv
*   json2html

Installation
------------

    pip install flask pydantic requests flask-cors python-dotenv json2html

Setup
-----

1.  Create a `.env` file in the root directory and add your configuration variables:

    API_TOKEN=your_api_token_here
    DEBUG=True

3.  Ensure your Caldera server base URL and API token are correctly set in `py_caldera.py`.

Running the Application
-----------------------

    python app.py

This will start the Flask server on `http://localhost:5005`.

Usage
-----

Access the application via your browser at `http://localhost:5005`. From the interface, you can initiate new operations, check their status, and view reports.

API Endpoints
-------------

*   `GET /api/operation/<operation_id>` - Retrieve the status of a specific operation.
*   `POST /api/operation` - Start a new operation.
*   `GET /api/operation` - List all operations.
*   `GET /api/reset` - Reset the application state.

Project Structure
-----------------

*   `app.py` - Main Flask application file.
*   `py_caldera.py` - Module for interacting with the Caldera API.
*   `static/` - Directory containing static files served by Flask.

Contributing
------------

Contributions are welcome. Please fork the repository and submit a pull request for any improvements.

License
-------

This project is licensed under the MIT License.