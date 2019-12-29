# Careers at
A simple Flask API application for applying to career openings.

This application provides three API endpoints:
* Submit Application
* List Candidates
* Install Candidate Resume

See the API [documentation](https://documenter.getpostman.com/view/2456151/SWLb9UsJ?version=latest) for further information.

### Setup and Installation

This application is delivered using Docker, Docker containers wrap up software and its dependencies into a standardized unit for software development and delivery that includes everything it needs to run.

* Install Docker from the following [link](https://www.docker.com/get-started). 


* Install the application.

```shell script
git clone git@github.com:saadaltabari/careers-at.git && cd careers-at
```

* Run the application with `docker-compose`.

```shell script
docker-compose -f docker-compose.local.yml up --build
```
The previous command will:

1. Install and run `mariadb` instance.

2. Create database tables.

3. Setup web application, install all requirements and run the api

The application should now be running on http://127.0.0.1:5000/ . see API [documentation](https://documenter.getpostman.com/view/2456151/SWLb9UsJ?version=latest) for endpoint details.
