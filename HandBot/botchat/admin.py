from django.contrib import admin
from .models import *

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'date')

admin.site.register(Animal, AnimalAdmin)

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact')
    
admin.site.register(Owner, OwnerAdmin)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document', 'uploaded_at')

admin.site.register(Document, DocumentAdmin)
