from apps.core.models import Message, AppConfig
from django.contrib import admin


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(AppConfig)
class AppConfigAdmin(admin.ModelAdmin):
    pass
