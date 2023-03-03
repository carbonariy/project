from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from users.serializers.sms_reg_link import RequestLinkSerializer
from users.tasks import send_sms


class SMSRegistrationLinkApiView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RequestLinkSerializer

    def create(self, request):
        serializer = RequestLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.data['phone']
        message = _('Download our awesome app {url},').format(url=settings.APP_URL)

        send_sms.delay(phone, message)

        return Response(status=status.HTTP_200_OK)
