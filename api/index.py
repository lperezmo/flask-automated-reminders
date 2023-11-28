import os
import json
import boto3
import logging
import datetime
from time import sleep
from flask_cors import CORS
from twilio.rest import Client
from botocore.exceptions import ClientError
from flask import Flask, request, jsonify, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler

#-----------------------------#
# Logging config
#-----------------------------#
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

#-----------------------------#
# App config
#-----------------------------#
app = Flask(__name__)
CORS(app)
scheduler = BackgroundScheduler()
scheduler.start()

#-----------------------------#
# Twilio config
#-----------------------------#
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
twilio_number = os.environ['TWILIO_NUMBER']
client = Client(account_sid, auth_token)

#-----------------------------#
# Index page
#-----------------------------#
# Main welcome page
index_page ="""
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Embeddings Context Generator v2</title>
	<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">

	<style>
		body {
			font-family: 'Roboto', sans-serif;
			margin: 0;
			padding: 0;
			background-color: #f7f9fc;
			color: #333;
		}

		.container {
			display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;
			min-height: 90vh;
			padding: 2rem;
		}

		h1 {
			font-size: 3rem;
			margin-bottom: 1rem;
			text-align: center;
			color: #2c3e50;
		}

		h4 {
			font-size: 1.8rem;
			margin-bottom: 1rem;
			color: #34495e;
		}

		p {
			font-size: 1.2rem;
			margin-bottom: 2rem;
			text-align: center;
			line-height: 1.6;
			max-width: 800px;
		}

		a {
			font-size: 1.2rem;
			padding: 0.8rem 1.5rem;
			border-radius: 2rem;
			background-color: #3498db;
			color: #fff;
			text-decoration: none;
			transition: background-color 0.3s ease, transform 0.3s ease;
			display: inline-block;
		}

		a:hover {
			background-color: #2980b9;
			transform: translateY(-3px);
			box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
		}

		footer {
			text-align: center;
			padding: 1rem 0;
			background-color: #2c3e50;
			color: #ecf0f1;
			font-size: 0.9rem;
		}
	</style>
</head>

<body>
	<div class="container">
		<h1>Remind Me App</h1>
		<h4>A way to get text/email reminders at specific times using an API</h4>
		<p>This is a Flask app that uses APScheduler to send text and emails at a specific times
		The API can in turn be used alongside LLM function-calling assistants to create a reminder assistant</p>
		<a href="https://github.com/lperezmo/flask-automated-reminders">Learn More</a>
	</div>

	<footer>
		© 2023 Luis Perez Morales. All rights reserved.
	</footer>
</body>

</html>"""


def send_twilio_message(to_number, message_body):
	message = client.messages.create(
		body=message_body,
		from_=twilio_number,
		to=to_number
	)
	print(f"Message sent: {message.sid}")
	logger.info(f"Message sent: {message.sid}")


def place_twilio_call(to_number, reminder, date, time):
    try:
        call = client.calls.create(
            twiml=f'<Response><Say>Hi, Luis! You have a reminder for: {reminder}. Scheduled for today {date} at {time}.</Say></Response>',
            to=to_number,
            from_=twilio_number
        )
        print(f"Call initiated: {call.sid}")
        logger.info(f"Call initiated: {call.sid}")
    except Exception as e:
        print(f"Error: {e}")
        logger.error(f"Error: {e}")


def send_email_aws_ses(to_email, subject, body_text, from_email):
	# Create a new SES resource
	ses_client = boto3.client('ses', region_name='us-east-1')

	try:
		# Provide the contents of the email.
		response = ses_client.send_email(
			Destination={
				'ToAddresses': [to_email]
			},
			Message={
				'Body': {
					'Text': {
						'Charset': 'UTF-8',
						'Data': body_text,
					},
				},
				'Subject': {
					'Charset': 'UTF-8',
					'Data': subject,
				},
			},
			Source=from_email,
			# Uncomment the following line if you are not using a configuration set
			# ConfigurationSetName='ConfigSet'
		)
		logger.info(response)
	except ClientError as e:
		print(e.response['Error']['Message'])
		# add logging 
		logger.error(e.response['Error']['Message'])
		return False
	else:
		print("Email sent! Message ID:"),
		print(response['MessageId'])
		logger.info("Email sent! Message ID:"),
		logger.info(response['MessageId'])
		return True


@app.route('/schedule_single_reminder', methods=['POST'])
def schedule_single_reminder():
	content = request.json
	time = content['time']
	day = content['day']
	message_body = content['message_body']

	# Whether or not to use Twilio. Default to False
	try:
		twilio = content['twilio']
	except KeyError:
		twilio = "False"
  
	# Whether or not to call. Default to False
	try:
		call = content['call']
	except KeyError:
		call = "False"

	# Get the destination twilio number or set default to my number
	try:
		to_number = content['to_number']
	except KeyError:
 		to_number = "+15419722223"

	# Get to_email or set default to remindme.h2i034@zapiermail.com
	try:
  		to_email = content['to_email']
	except KeyError:
		to_email = 'remindme.h2i034@zapiermail.com'

	# Time of the reminder
	reminder_time = datetime.datetime.strptime(f"{day} {time}", "%Y-%m-%d %H:%M")

	if twilio == "False" and call == "False":
		# Schedule the email sending job
		scheduler.add_job(
			func=send_email_aws_ses,
			args=[
				to_email,
				message_body,
				message_body,
				"muffins@luisperez.link"
			],
			run_date=reminder_time  # The specific time to run the job
		)
		return jsonify({"status": "Reminder scheduled successfully (email + zap)"})

	if twilio == "True" and call == "False":
		# Schedule the Twilio message
		scheduler.add_job(
			send_twilio_message,
			'date',
			run_date=reminder_time,
			args=[to_number, message_body]
		)

		return jsonify({"status": "Reminder scheduled successfully (twilio)"})

	if twilio == "True" and call == "True":
		# Schedule the Twilio message
		scheduler.add_job(
			send_twilio_message,
			'date',
			run_date=reminder_time,
			args=[to_number, message_body]
		)

		# Schedule the Twilio call
		scheduler.add_job(
			place_twilio_call,
			'date',
			run_date=reminder_time,
			args=[to_number, message_body, day, time]
		)

		return jsonify({"status": "Reminder scheduled successfully (twilio + call)"})

	# Send email for zap and twilio call
	if twilio == "False" and call == "True":
		# Schedule the Twilio call
		scheduler.add_job(
			place_twilio_call,
			'date',
			run_date=reminder_time,
			args=[to_number, message_body, day, time]
		)

		return jsonify({"status": "Reminder scheduled successfully (call + email + zap)"})
	
#-----------------------------#
# API docs
#-----------------------------#
@app.route("/openapi.yml")
def serve_openapi():
    return send_from_directory("static", "openapi.yml", mimetype="text/plain")

#-----------------------------#
# Index page
#-----------------------------#
app.add_url_rule('/', 'index', (lambda: index_page))

if __name__ == '__main__':
	app.debug = True
	app.run()