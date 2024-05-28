from django.urls import reverse

import pytest
from rest_framework import status


@pytest.mark.parametrize('phone, status_expected', [
    ('+79999999999', status.HTTP_200_OK),
    ('THISISNOTANUMBER!', status.HTTP_400_BAD_REQUEST),
])
def test_sms_registration_api_view(api_client, mocker_send_sms, phone, status_expected):
    url = reverse('v1:sms_reg_link-list')

    response = api_client.post(url, data={'phone': phone}, format='json')
    assert response.status_code == status_expected
