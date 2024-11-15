# Survey Application

This project is a high-performance Survey Application that enables users to fill out surveys, stores the results in MongoDB, and performs robust data analysis. Built using the Sanic framework, it is designed to handle requests efficiently and provides secure data management.

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Running the Application](#running-the-application)
6. [Running Tests](#running-tests)
7. [Environment Variables](#environment-variables)
8. [Usage Guide](#usage-guide)
9. [Deployment on Render](#deployment-on-render)
10. [Error Handling and Logging](#error-handling-and-logging)
13. [License](#license)

---

## Overview

This Survey Application allows users to submit survey responses that are stored and analyzed. The app uses the Sanic framework for fast API responses and MongoDB as the database. It also integrates with OpenAI to process and analyze survey data intelligently.

---

## Features

- **Survey Form Handling**: Allows users to submit surveys and stores them securely.
- **Data Analysis**: Performs analysis on survey data for reporting purposes.
- **Error Handling**: Includes graceful error handling for unknown routes and data validation.
- **Testing and Coverage**: Tests for key functionalities, achieving over 90% coverage.


## Installation

### Prerequisites

- **Python 3.8+**
- **Docker**
- **Sanic**
- **MongoDB** (Running instance)

### Clone the Repository

```bash
git clone https://github.com/your-username/survey-app.git
cd survey-app
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

### With Docker

To run the application in Docker:

1. **Build the Docker Image**:

   ```bash
   docker build -t survey-app .
   ```

2. **Run the Docker Container**:

   ```bash
   docker run -p 8000:8000 --env-file .env survey-app
   ```

3. **Verify**: Visit `http://localhost:8000` to access the application.

### Without Docker

```bash
python -m src.main
```

---

## Running Tests

To execute tests and generate coverage reports:

```bash
pytest --cov=src tests/
```

This generates a coverage report in `tests/coverage-report`.

---

## Environment Variables

Set environment variables in a `.env` file in the root directory:

```plaintext
DATABASE_URL=mongodb://localhost:27017/surveyapp
OPENAI_API_KEY=your_openai_api_key
DEBUG=True
PORT=8000
```

---

## Usage Guide

1. **Access the Survey Form**: `http://localhost:8000/`
2. **Submit the Form**: User fills out and submits the survey.
3. **View Results**: Access results on thesame page.

### API Endpoints

- **POST /process-survey**: Submits survey responses.

---

## Deployment on Render

The Survey Application is deployed on Render for live access. [https://survey-app-1aq9.onrender.com](https://survey-app-1aq9.onrender.com/).

---

## Error Handling and Logging

Error handling includes:

- **404 Errors**: Returned for unknown routes.
- **API Failures**: Graceful fallbacks for failed OpenAI calls.

---

## License

This project is licensed under the MIT License.

---

```
