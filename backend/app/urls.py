from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from users import viewset as users_viewset

router = routers.DefaultRouter()
router.register(
    r'user/request_link', users_viewset.SMSRegistrationLinkApiView, basename='sms_reg_link')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((router.urls, 'backend'), namespace='v1')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
