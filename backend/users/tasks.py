import logging

from backend.celery import app as celery_app
from users.services import sms


logger = logging.getLogger(__name__)


@celery_app.task
def send_sms(phone, message):
    sms.send([phone], message)
