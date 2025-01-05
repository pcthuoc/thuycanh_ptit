from django.contrib import admin
from .models import Auto

class AutoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('api_key', 'auto_name')
        }),
        ('Pump Configuration', {
            'fields': ('pump_choice', 'pump_pin')
        }),
        ('Valve Configuration', {
            'fields': ( 'vanph_min_pin', 'vanph_max_pin')
        }),
        ('pH Configuration', {
            'fields': ('min_ph', 'max_ph', 'ph_status')  # Xóa 'ph_pin' khỏi đây
        }),
        ('Light Configuration', {
            'fields': ('min_light', 'light_status', 'light_pin')
        }),
        ('Dưỡng chất Configuration', {
            'fields': ( 'van_status','duong_chat_1', 'duong_chat_2')
        }),
    )

admin.site.register(Auto, AutoAdmin)
