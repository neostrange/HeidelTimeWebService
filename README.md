# HeidelTimeWebService
HeidelTimeWebService is a Flask-based web application that processes plain text inputs and annotates them with TIMEX annotations using the HeidelTime engine. The web service provides a clean, XML-based output format that includes the annotated text spans' starting and ending indexes, making it easy to integrate into other workflows. This repository also includes a Docker configuration for easy deployment.

**Features**
TIMEX Annotation: The web service leverages the HeidelTime engine to perform temporal expression (TIMEX) annotation on the input text.
XML Output: The service converts the native HeidelTime output into standalone XML-based annotations, which include the annotated text spans and their corresponding indexes (start and end positions).
Dockerized Deployment: A Dockerfile is included to allow easy deployment and encapsulation of the service.

**Docker Setup**
To deploy the service using Docker:

1. Build the Docker image:
   ```bash
   docker build -t heideltime-web-service .
3. Run the Docker container:
   ```bash
   docker run -p 5000:5000 heideltime-web-service

This will expose the application at http://localhost:5000.


**Usage**
Once the service is running (either locally or via Docker), you can interact with it via the /annotate API endpoint. This endpoint accepts a POST request with the input text, and it returns the TIMEX annotations in XML format.

Example request using curl:
  ```bash
  curl -X POST http://localhost:5000/annotate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I will meet you on January 1st, 2024."
  }'
```
**Contribution**
We welcome contributions to the HeidelTimeWebService project. If you have feature suggestions, bug reports, or would like to contribute improvements, feel free to open an issue or submit a pull request.

**License**
This project is licensed under the MIT License.
