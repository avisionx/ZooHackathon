from django.contrib import admin
from .models import *

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'date', 'location_published')
    
admin.site.register(Animal, AnimalAdmin)

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact')

admin.site.register(Owner, OwnerAdmin)
