"""
Background worker: pulls from the queue and dispatches notifications
through email (SendGrid), SMS (via legacy-app), and push (boto3/SNS).
"""

import requests
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import boto3
from jinja2 import Template

app = Celery("dispatcher", broker="redis://localhost:6379/0")
engine = create_engine("sqlite:///notifications.db")
Session = sessionmaker(bind=engine)

LEGACY_APP_URL = "http://localhost:3000"


@app.task
def send_email(to: str, subject: str, body: str):
    tmpl = Template("Hello {{ name }}, {{ body }}")
    rendered = tmpl.render(name=to, body=body)
    requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        json={"to": to, "subject": subject, "body": rendered},
        timeout=10,
    )


@app.task
def send_push(user_id: str, message: str):
    sns = boto3.client("sns")
    sns.publish(TopicArn="arn:aws:sns:us-east-1:000:notify", Message=message)


@app.task
def log_event(event_type: str, payload: dict):
    requests.post(f"{LEGACY_APP_URL}/api/events", json={"type": event_type, "data": payload}, timeout=5)
