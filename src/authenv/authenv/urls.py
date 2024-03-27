from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Authantication API",
        # default_version='v1',
        # description="API for Authantication",
        # terms_of_service="https://www.example.com/terms/",
        # contact=openapi.Contact(email="contact@example.com"),
        # license=openapi.License(name="MIT License"),
    # ),
    # public=True,
    # permission_classes=(permissions.AllowAny,),
# )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('account.urls')),
    # path('swagger/', schema_view.with_ui('swagger',
        #  cache_timeout=0), name='schema-swagger-ui'),
]
