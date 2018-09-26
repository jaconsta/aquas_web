from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Pomelo API",
      default_version='v1',
      description="Water your live",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@pomelo.com"),
      license=openapi.License(name="BSD License"),
   ),
   validators=[],  # 'flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)
