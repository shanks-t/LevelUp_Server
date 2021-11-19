from django.urls import path
from .views import UserGameList, UserEventList

urlpatterns = [
    path('reports/usergames', UserGameList.as_view()),
    path('reports/userevents', UserEventList.as_view()),
]
