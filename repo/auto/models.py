from django.db import models
from multiselectfield import MultiSelectField
from django.core.cache import cache
class Auto(models.Model):
    ON = 1
    OFF = 0
    VALUE_TYPE_CHOICES = (
        (ON, 'On'),
        (OFF, 'Off'),
    )
    CONTINUOUS = 1
    INTERVAL = 2
    OFF_PUMP = 2
    PUMP_TYPE_CHOICES = (
        (CONTINUOUS, 'Cozantinuous Mode (Always On)'),
        (INTERVAL, 'Interval Mode (On for 5s, Off for 5s)'),
    )
    VAN_TYPE_CHOICES = (
        (1, 'Tu dong'),
        (2, 'thu cong'),
    )
    api_key = models.CharField(max_length=30,default="TEY8OO5iafAV96gRKcZohbO6ED", help_text="Device API Key")
    auto_name = models.CharField(max_length=100, help_text="Tên cây trồng")
    auto_status = models.IntegerField(choices=VALUE_TYPE_CHOICES, default=OFF, help_text="Type")

    pump_choice = models.IntegerField(choices=PUMP_TYPE_CHOICES, default=CONTINUOUS, help_text="Type")
    pump_pin = models.CharField(max_length=3,default='V0' ,help_text="PIN value from V0 to V50")
    
    van_status = models.IntegerField(choices=VAN_TYPE_CHOICES, help_text="Type")
    van_pin = models.CharField(max_length=3, default='Vx', help_text="PIN value from V0 to V50")
    

    vanph_min_pin = models.CharField(max_length=3, default='V2', help_text="PIN value from V0 to V50")
    vanph_max_pin = models.CharField(max_length=3, default='V1', help_text="PIN value from V0 to V50")
    min_ph =models.CharField(max_length=100, help_text="ph min")
    max_ph =models.CharField(max_length=100, help_text="ph max")
    ph_status = models.IntegerField(choices=VALUE_TYPE_CHOICES, default=ON, help_text="Type")
    vanph_pin = models.CharField(max_length=3, default='V9', help_text="PIN value from V0 to V50")
    
    min_light =models.CharField(max_length=100, help_text="light min")
    light_status = models.IntegerField(choices=VALUE_TYPE_CHOICES, default=ON, help_text="Type")
    light_pin = models.CharField(max_length=3, default='V6', help_text="PIN value from V0 to V50")
    light_relay = models.CharField(max_length=3, default='V11', help_text="PIN value from V0 to V50")

    
    duong_chat_1 = models.CharField(max_length=3, default='V3', help_text="PIN for dưỡng chất 1 (V0 to V50)")
    duong_chat_2 = models.CharField(max_length=3, default='V4', help_text="PIN for dưỡng chất 2 (V0 to V50)")
    def save(self, *args, **kwargs):
        if self.auto_status == self.ON:
            # Tắt tất cả các bản ghi khác trước khi bật cái này
            Auto.objects.filter(auto_status=self.ON).update(auto_status=self.OFF)
        
        # Lưu bản ghi hiện tại
        super().save(*args, **kwargs)

        # Cập nhật cache
        if self.auto_status == self.ON:
            cache.set('active_auto', self)
        else:
            cache.delete('active_auto')

    def __str__(self):
        return self.auto_name