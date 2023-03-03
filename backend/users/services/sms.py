import logging
import re

from django.conf import settings
from rest_framework.exceptions import APIException

from util.smsc import SMSC


logger = logging.getLogger('sms')


ERROR_CODES = {
    1: 'wrong request parameters',
    2: 'wrong login or password',
    3: 'insufficient funds',
    4: 'IP is blocked',
    5: 'wrong datetime format',
    6: 'message is blocked',
    7: 'wrong phone number format',
    8: 'message could not be delivered',
    9: 'too many requests',
}


REGEX_PHONE_DEV = re.compile(r'\+?7777\d{7}')


class SMSException(APIException):
    pass


def send(to_phones, message):
    concatenated_phones = ','.join(to_phones)
    if settings.SMS_SENDING_ENABLE:
        if settings.DEBUG and REGEX_PHONE_DEV.fullmatch(to_phones[0]):
            logger.info(
                f'SMS not sending, because DEBUG is True and phone number starts with +7777.\n'
                f'Phones: {concatenated_phones};\n'
                f'message:\n'
                f'{message}'
            )
            return
        result = SMSC().send_sms(
            phones=concatenated_phones, message=message, sender='sender', query='valid=00:05')
        if result[1] <= '0':
            error_code = int(result[1][1:])
            error_message = ERROR_CODES.get(error_code)
            logger.error('smsc.ru error: code = %d, error = %s, phones = %s',
                         error_code, error_message, concatenated_phones)
            raise SMSException('sending SMS is failed')
        logger.debug(f'SMS message has just been sent to {concatenated_phones}')  # noqa E501
    else:
        logger.info(
            f'SMS not sending, because SMS_SENDING_ENABLE is False.\n'
            f'Phones: {concatenated_phones};\n'
            f'message:\n'
            f'{message}'
        )
