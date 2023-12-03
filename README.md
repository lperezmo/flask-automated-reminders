# Remind Me App

## Overview
The Remind Me App is a Flask-based application designed to schedule reminders via text or email at specific times. It leverages APScheduler for scheduling and can be integrated with function-calling LLM assistants.

> ## Note
> **For some reason, now the scheduler only works if it's deployed on AWS Elastic Beanstalk. The only difference from a regular deployment is that you have to create an app instance on AWS and upload your code as a .zip file (it's covered under free tier). After that you can use Vercel as a redirect to be able to use with a custom endpoint to put on custom endpoint/use HTTPS to use alongside GPTs**

## Features
- Schedule reminders at specific times.
- Send reminders via text message or email.
- Flask API for easy integration.
- Use with any function-calling LLMs

## How to run for free
Change the `send_email_aws_ses` function for any other email sending function. Many open source alternatives exist (for example see https://github.com/lperezmo/email-sender). I haven't yet found a phone call alternative to Twilio, but let me know if you know of any.

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
Use the `/schedule_single_reminder` endpoint to set up reminders. Use `/schedule_reminder_aws` to use the redirect to ElasticBeanstalk AWS flask app.

## API Reference
API Endpoints
* POST /schedule_single_reminder
* POST /schedule_reminder_aws

Schedules a single reminder based on provided details.
Request Parameters

* time: String (required) - The time for the reminder in HH:MM format.
* day: String (required) - The date for the reminder in YYYY-MM-DD format.
* message_body: String (required) - The message content for the reminder.
* twilio: String (optional) - Whether to use Twilio for sending a text message. Defaults to "False".
* call: String (optional) - Whether to initiate a call for the reminder. Defaults to "False".
* to_number: String (optional) - The recipient's phone number.
* to_email: String (optional) - The recipient's email address.

Response
* 200 OK: Reminder scheduled successfully. Returns JSON object with the status of the reminder scheduling.
```
{
    "status": "Reminder scheduled successfully (email + zap)"
}
```

## Contributing
Contributions are welcome, just submit a pull request and I'll take a look at it. If someone figures out how to make it work using only Vercel, let me know. So far it works great on AWS.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.
