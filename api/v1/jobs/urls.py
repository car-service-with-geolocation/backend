from django.urls import path 
 
 
from .views import JobsList, JobsDetail

urlpatterns = [
    path('', JobsList.as_view(), name='jobs-list'),
    path('<int:pk>/', JobsDetail.as_view(), name='jobs-detail'),
]