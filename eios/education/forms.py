#encoding: UTF-8
from django import forms
from django.forms import formset_factory, modelformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from .models import Education, Professor, Studies, Work


class DisciplineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DisciplineForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Studies
        exclude = ['leaner', 'rating']

    def clean(self):
        cleaned_data = super(DisciplineForm, self).clean()
        if self.request:
            subject = cleaned_data.get("subject")
            course = cleaned_data.get("course")
            semester = cleaned_data.get("semester")
            try:
                discipline_already_exist = Studies.objects.get(leaner__user=self.request.user, subject=subject,
                    course=course, semester=semester)
                raise forms.ValidationError(u"""Сведения о данной дисциплине за указанный период уже 
                    предоставлены""")
            except Studies.DoesNotExist:
                pass
        return cleaned_data


DisciplineFormset = modelformset_factory(Studies, form=DisciplineForm, 
    exclude = ['leaner', 'rating'], extra=0, can_delete=True)


class DisciplineFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(DisciplineFormHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Div(
                Div(
                    Div('subject',css_class='col-md-3',),
                    Div('course',css_class='col-md-2',),
                    Div('semester',css_class='col-md-2',),
                    Div('hour_sem',css_class='col-md-1',),
                    Div('grade',css_class='col-md-2',),
                    Div('DELETE',css_class='col-md-1',),
                    css_class='row',
                ),
            css_class='subject-item',
            ),
        )
        self.add_input(Submit("submit", u"Сохранить изменения"))


class EducationForm(forms.ModelForm):

    class Meta:
        model = Education
        exclude = ['user', 'subjects']

    def clean(self):
        cleaned_data = super(EducationForm, self).clean()
        status = cleaned_data.get("status")
        end_reason = cleaned_data.get("end_reason")
        if status == u"Отчислен":
            if not end_reason:
                raise forms.ValidationError(u"""При смене статуса образования на "Отчислен из ВУЗа" 
                    необходимо указать причину отчисления.""")
            if end_reason == u"Успешно завершил обучение":  
                try: 
                    self.instance.get_graduation_work()
                except Work.DoesNotExist:
                    raise forms.ValidationError(u""" Необходимо загрузить выпускную работу.""")
        return cleaned_data


class ProfessorForm(forms.ModelForm):

    class Meta:
        model = Professor
        exclude = ['user']


class WorkForm(forms.ModelForm):

    class Meta:
        model = Work
        exclude = ['author']
