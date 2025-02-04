 
Firewall Test Tool
==================

This application provides a web-based interface to manage and test operations using the Caldera platform. It supports running operations, checking their status, and generating reports.


This project sets up a Flask application served by Gunicorn and proxied by Nginx. The setup uses Docker for containerization, enabling easy deployment and scalability. Environment variables configure the application at runtime.

### Project Structure

* app.py: The main Flask application file.
* requirements.txt: Lists the Python dependencies.
* Dockerfile: Builds the Docker image for the Flask app.
* nginx.conf: Nginx configuration file for reverse proxy setup.
* docker-compose.yml: Defines the multi-container setup for the Flask app and Nginx.
* .env: A file to store environment variables.


### Prerequisites

    Docker: Ensure Docker is installed on your system. You can download it from Docker's official site.
    Docker Compose: Make sure Docker Compose is installed. It's included with Docker Desktop for Windows and Mac.


### Setup Instructions

**Clone the Repository**

* git clone <repository-url> cd <repository-folder>

**Create an .env File**

Create a .env file in the root directory of the project with the following content:

    API_TOKEN=CALDERA_API_TOKEN
    CALDERA_SERVER=http://CALDERA_SERVER_IP_OR_HOSTNAME
    ADVERSARY_ID=ADVERSARY_ID

**Build and Run the Docker Containers**

Use Docker Compose to build and start the services:

* docker-compose up --build

This command starts the containers and maps port 80 on the host to Nginx.


### Accessing the Application

Once the containers are running, you can access the application by navigating to http://localhost in your web browser.

* API Endpoints: Requests are proxied to the Flask application by Nginx.
* Static Content: Nginx serves static content as configured in nginx.conf.


### Key Components

    Flask: A micro web framework for Python, used to create the application.
    Gunicorn: A Python WSGI HTTP server, used to serve the Flask app.
    Nginx: A high-performance HTTP server and reverse proxy, used to handle incoming requests and proxy them to Gunicorn.
    Docker: Containerization platform to bundle and run the application.
    Docker Compose: Tool for defining and running multi-container Docker applications.


### Customization

    Nginx Configuration: Modify nginx.conf to change proxy settings or add new rules.
    Environment Variables: Update the .env file to change application configurations.


### Troubleshooting

* Check Logs: Use docker-compose logs to view logs from the running services.
* Health Checks: Ensure the Flask app is healthy and responding to requests.
* Network Issues: Confirm that Docker Compose services are correctly networked.


### License

This project is licensed under the MIT License. See the LICENSE file for details.