from django.contrib.auth import get_user_model 
from rest_framework import serializers 
 
from autoservice.models import Job
 
User = get_user_model() 

class JobsSerializer(serializers.ModelSerializer): 
    """Сериализатор для списка работ""" 
    class Meta: 
        model = Job
        fields = "__all__"
