# AWS Elastic Beanstalk Flask App

This repository contains the code and instructions to deploy a Flask app on AWS Elastic Beanstalk.

## Creation (Web)

This is the easiest way.
1. Create AWS account
2. On search go over to `Elastic Beanstalk`
3. Create environment
4. Select all defaults and choose "deploy from file"
5. Upload a .zip file with all the files on this folder, `application.py`, `requirements.txt`, and `static` folder.
6. Done, copy your url and send POST requests to schedule things.

## Creation (CLI)

Before you begin, make sure you have the following:

- Python installed on your local machine
- AWS account credentials
- AWS CLI installed and configured

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/your-username/flask-automated-reminders.git
    ```

2. Navigate to the project directory:

    ```bash
    cd flask-automated-reminders/AWS Elastic Beanstalk
    ```

3. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate  # For Windows
    ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Configure AWS Elastic Beanstalk:

    ```bash
    eb init
    ```

    Follow the prompts to select your region, application, and environment.

6. Create the AWS Elastic Beanstalk environment:

    ```bash
    eb create
    ```

    This will create the environment and deploy your Flask app.

7. Access your app

    Once the deployment is complete, you can access your app by running:

    ```bash
    eb open
    ```

    This will open your app in a web browser.

## Customization

Feel free to customize the Flask app according to your needs. You can modify the `application.py` file to add your own routes and functionality.

## Deployment

To deploy any changes to your app, simply commit your changes and run:
