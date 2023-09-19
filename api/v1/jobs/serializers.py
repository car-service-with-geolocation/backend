from django.contrib.auth import get_user_model 
from rest_framework import serializers 
 
from jobs.models import Jobs
 
User = get_user_model() 

class JobsSerializer(serializers.ModelSerializer): 
    """Сериализатор для списка работ""" 
    class Meta: 
        model = Jobs 
        fields = ('id', 'name', 'slug', 'price', 'description') 
