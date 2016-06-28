from django.contrib import admin
from django.contrib.auth.models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Application, LangLevel, Language, UserDetail
from core.models import Document


class HideModel(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}
        

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1


class LangLevelInline(admin.TabularInline):
    model = LangLevel
    extra = 1


class UserResource(resources.ModelResource):

    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin):
    pass


class UserDetailResource(resources.ModelResource):

    class Meta:
        model = UserDetail


class UserDetailAdmin(ImportExportModelAdmin):
    inlines = [
        LangLevelInline, DocumentInline
    ]


admin.site.register(Application)
admin.site.register(LangLevel, HideModel)
admin.site.register(Language)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserDetail, UserDetailAdmin)