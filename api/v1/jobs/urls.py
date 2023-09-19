from django.urls import path 
 
 
from .views import JobsList, JobsDetail

urlpatterns = [
    path('jobs/', JobsList.as_view(), name='jobs-list'),
    path('jobs/<int:pk>/', JobsDetail.as_view(), name='jobs-detail'),
]