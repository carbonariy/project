from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework import routers

from users import viewset as users_viewset


router = routers.DefaultRouter()
router.register(
    r'user/request_link', users_viewset.SMSRegistrationLinkApiView, basename='sms_reg_link')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((router.urls, 'backend'), namespace='v1')),
]
