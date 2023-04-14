from django.contrib import admin
from django.urls import path
from app_email.views import SuggestionEmailView

urlpatterns = [
    path('admin/', admin.site.urls),
    # 8- add the route.
    path('suggestions/', SuggestionEmailView.as_view(), name="suggestions"),
]
