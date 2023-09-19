from django.contrib import admin

from jobs.models import Jobs

@admin.register(Jobs) 
class JobsAdmin(admin.ModelAdmin): 
    list_display = ('id', 'name', 'price', 'slug', 'description') 
    list_filter = ('name',) 
    search_fields = ('name',)