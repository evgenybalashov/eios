from django.contrib import admin
from .models import Department


class HideModel(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


admin.site.register(Department)