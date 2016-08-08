#coding: UTF-8
from django.contrib import admin
from django.contrib.auth.hashers import make_password, is_password_usable
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


def generate_pass_action(modeladmin, request, queryset):
    for user in queryset:
        if is_password_usable(user.password):
            print "Passed!"
        else:
            user.password = make_password(user.password, None, 'md5')
            user.save()
generate_pass_action.short_description = "Generate MD5 hash for selected users"


class UserAdmin(ImportExportModelAdmin):
    actions = [generate_pass_action,]


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