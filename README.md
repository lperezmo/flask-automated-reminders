# Remind Me App

## Overview
The Remind Me App is a Flask-based application designed to schedule reminders via text or email at specific times. It leverages APScheduler for scheduling and can be integrated with function-calling LLM assistants.

## Features
- Schedule reminders at specific times.
- Send reminders via text message or email.
- Flask API for easy integration.
- Use with any function-calling LLMs

## Getting Started
To get started with the Remind Me App, clone the repository and install the necessary dependencies.

### Prerequisites
- Python
- Flask
- APScheduler
- Boto3 for Amazon SES emails
- Twilio for text messaging & calls (optional)

### Installation
1. Clone the repository:
```
git clone https://github.com/lperezmo/automated-reminders.git
```
2. Install the dependencies:
```
pip install -r requirements.txt
```

### Usage
Run the Flask application:
```
python app.py
```
Use the `/schedule_single_reminder` endpoint to set up reminders.

## API Reference
Refer to the OpenAPI documentation for detailed API usage.

## Contributing
Contributions to the Remind Me App are welcome. Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.
