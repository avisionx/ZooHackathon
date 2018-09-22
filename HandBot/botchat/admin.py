from django.contrib import admin

from .models import MessageText, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class MessageTextAdmin(admin.ModelAdmin):
    list_display = ('message_text', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None,               {'fields': ['message_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(MessageText, MessageTextAdmin)
