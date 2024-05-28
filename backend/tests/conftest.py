import pytest

from util.smsc import SMSC  # type: ignore[attr-defined]


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def mocker_send_sms(mocker):
    def send_sms_correct(phones, message, sender, query):
        return '1', '1', '1', '1'

    mocker_send_sms = mocker.patch.object(SMSC, 'send_sms')
    mocker_send_sms.side_effect = send_sms_correct

    return mocker_send_sms
