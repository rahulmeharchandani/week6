from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import StudentViewSet
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

schema_view = get_schema_view(
   openapi.Info(
      title="Student API",
      default_version='v1',
      description="Student management API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]