from django.urls import reverse
from rest_framework.test import APITestCase


class SMSRegistrationLinkApiViewTests(APITestCase):
    def execute(self, should_code=200, phone='+79999999999'):
        url = reverse('v1:sms_reg_link-list')
        client = self.client_class()

        response = client.post(url, data={'phone': phone}, format='json')
        self.assertEqual(response.status_code, should_code)

    def test_post(self):
        self.execute()

    def test_post_wrong_phone(self):
        self.execute(should_code=400, phone='THISISNOTANUMBER!')
