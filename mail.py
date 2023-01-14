import smtplib

from typing import Dict, List
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from environment import EnvironmentManager


def send_mail(
        data: Dict,
        _to: List = []) -> None:
    config: Dict[str, str] = EnvironmentManager()
    with smtplib.SMTP(config.get('EMAIL_SERVER'), 587) as session:
        session.starttls()
        session.login('help@martroo.com', config.get('EMAIL_PASSWORD'))
        message = MIMEMultipart()
        message['From'] = 'help@martroo.com'
        message['Subject'] = data.get('subject')
        message.attach(MIMEText(data.get('body')))
        message['To'] = ','.join(_to)
        session.sendmail('help@martroo.com', _to, message.as_string())
    del config
