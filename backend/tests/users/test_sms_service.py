from unittest import mock

from django.test import TestCase
from django.test import override_settings

from users.services import sms
from util.smsc import SMSC


@override_settings(SMS_SENDING_ENABLE=True)
class SmsServiceTests(TestCase):
    correct_phone = '1235678'
    incorrect_phone = 'blabla'

    def send_sms_correct(self, phones, message, sender, query):
        return '1', '1', '1', '1'

    def send_sms_error(self, phones, message, sender, query):
        return '0', '-100500'

    @mock.patch.object(SMSC, 'send_sms')
    def test__send_sms_with_correct_input__exceptions_should_not_be_raised(self, mock_send_sms):
        mock_send_sms.side_effect = self.send_sms_correct
        sms.send(to_phones=[self.correct_phone], message='The app is awesome!')

    @mock.patch.object(SMSC, 'send_sms')
    def test__send_sms_to_incorrect_number__exceptions_should_be_raised(self, mock_send_sms):
        mock_send_sms.side_effect = self.send_sms_error
        with self.assertRaises(sms.SMSException) as exception_context:
            sms.send(to_phones=[self.incorrect_phone], message='The app is awesome!')
        self.assertEqual('sending SMS is failed', str(exception_context.exception))
