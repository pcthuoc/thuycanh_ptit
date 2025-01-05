from django.apps import AppConfig

class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'
    path = '/site/jobs'  # Chỉ định đường dẫn chính xác
