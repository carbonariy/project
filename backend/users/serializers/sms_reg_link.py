from django.conf import settings
from django.utils.translation import gettext as _
from phonenumbers import is_possible_number_string
from rest_framework import serializers


class RequestLinkSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)

    def validate_phone(self, phone):
        if not is_possible_number_string(phone, settings.PHONENUMBER_DEFAULT_REGION):
            raise serializers.ValidationError(detail=_('Wrong phone number format'))
        return phone
