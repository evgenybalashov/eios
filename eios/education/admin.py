from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Education, Professor, Speciality, Studies, Subject, TrainingField, Work


class HideModel(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class StudiesInline(admin.StackedInline):
    model = Studies


class WorkInline(admin.TabularInline):
    model = Work
    extra = 1


class EducationResource(resources.ModelResource):

    class Meta:
        model = Education


class EducationAdmin(ImportExportModelAdmin):
    inlines = [
        StudiesInline, WorkInline
    ]


class SubjectResource(resources.ModelResource):

    class Meta:
        model = Subject


class SubjectAdmin(ImportExportModelAdmin):
    pass


class SpecialityResource(resources.ModelResource):

    class Meta:
        model = Speciality


class SpecialityAdmin(ImportExportModelAdmin):
    pass


class TrainingFieldResource(resources.ModelResource):

    class Meta:
        model = TrainingField


class TrainingFieldAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Education, EducationAdmin)
admin.site.register(Professor)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Studies, HideModel)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(TrainingField, TrainingFieldAdmin)
admin.site.register(Work, HideModel)