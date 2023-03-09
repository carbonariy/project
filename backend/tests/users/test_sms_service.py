import pytest
from django.test import override_settings

from users.services import sms
from util.smsc import SMSC


@override_settings(SMS_SENDING_ENABLE=True)
def test_users_sms_service_correct_input(mocker):
    correct_phone = '1235678'

    def send_sms_correct(phones, message, sender, query):
        return '1', '1', '1', '1'

    mock_send_sms = mocker.patch.object(SMSC, 'send_sms')
    mock_send_sms.side_effect = send_sms_correct
    sms.send(to_phones=[correct_phone], message='The app is awesome!')


@override_settings(SMS_SENDING_ENABLE=True)
def test_users_sms_service_incorrect_input(mocker):
    incorrect_phone = 'blabla'

    def send_sms_error(phones, message, sender, query):
        return '0', '-100500'

    mock_send_sms = mocker.patch.object(SMSC, 'send_sms')
    mock_send_sms.side_effect = send_sms_error
    with pytest.raises(sms.SMSException) as exception_context:
        sms.send(to_phones=[incorrect_phone], message='The app is awesome!')
    assert str(exception_context.value) == 'sending SMS is failed'
