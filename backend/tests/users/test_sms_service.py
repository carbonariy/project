from django.test import override_settings

import pytest

from users.services import sms


@override_settings(SMS_SENDING_ENABLE=True)
def test_users_sms_service_correct_input(mocker_send_sms):
    correct_phone = '1235678'
    sms.send(to_phones=[correct_phone], message='The app is awesome!')


@override_settings(SMS_SENDING_ENABLE=True)
def test_users_sms_service_incorrect_input(mocker_send_sms):
    incorrect_phone = 'blabla'

    def send_sms_error(phones, message, sender, query):
        return '0', '-100500'

    mocker_send_sms.side_effect = send_sms_error
    with pytest.raises(sms.SMSException) as exception_context:
        sms.send(to_phones=[incorrect_phone], message='The app is awesome!')
    assert str(exception_context.value) == 'sending SMS is failed'
