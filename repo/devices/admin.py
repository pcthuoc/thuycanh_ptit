from django.contrib import admin
from .models import Device
from apikey.models import APIKey
from import_export.admin import ImportExportModelAdmin

class DeviceAdmin(ImportExportModelAdmin):
    """
    Custom admin for Device model.  api_key_demo
    """
    list_display = ('name', 'api_key', 'get_device_type', 'pin', 'unit', 'value', 'created_at')
    search_fields = ['name', 'pin']
    list_filter = ['api_key', 'type']
    readonly_fields = ['created_at']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'api_key_demo':
            try:
                kwargs["queryset"] = APIKey.objects.all()
            except Exception as e:
                self.message_user(request, "There was an error retrieving API keys. Please try again later.", level='ERROR')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'pin':
            # Lấy danh sách các pin đã sử dụng
            used_pins = Device.objects.values_list('pin', flat=True).distinct()
            
            # Nếu đang chỉnh sửa một bản ghi, lấy giá trị pin hiện tại
            if request.resolver_match.kwargs.get('object_id'):
                current_device_id = request.resolver_match.kwargs['object_id']
                current_pin = Device.objects.filter(id=current_device_id).values_list('pin', flat=True).first()
            else:
                current_pin = None
            
            # Tạo danh sách các lựa chọn
            choices = [
                (f'V{i}', f'V{i}')
                for i in range(51)
                if f'V{i}' not in used_pins or f'V{i}' == current_pin
            ]
            
            # Gán danh sách choices vào kwargs
            kwargs['choices'] = choices

        return super().formfield_for_choice_field(db_field, request, **kwargs)


    def get_device_type(self, obj):
        return 'Relay' if obj.type == 1 else 'Sensor'

    get_device_type.short_description = 'Type'

admin.site.register(Device, DeviceAdmin)
