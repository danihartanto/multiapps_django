from django.contrib import admin
from .models import ChatRule

@admin.register(ChatRule)
class ChatRuleAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'response']
    search_fields = ['keyword']
