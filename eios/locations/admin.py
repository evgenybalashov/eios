from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Department


class HideModel(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class DepartmentResource(resources.ModelResource):

    class Meta:
        model = Department


class DepartmentAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Department, DepartmentAdmin)