from django.urls import path
from .views import TrialQueryAPI

urlpatterns = [
    path("api/trials/query/", TrialQueryAPI.as_view()),
]
