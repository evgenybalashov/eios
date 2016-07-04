#coding: UTF-8
from __future__ import unicode_literals

import os
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from locations.models import Department
from profiles.models import UserDetail


EDUCATION_TYPE_CHOICES = (
    ('',''),
    ('G', u'Аспирант'),
    ('B', u'Бакалавр'),
    ('M', u'Магистр'),
    ('S', u'Специалист'),
)

EDUCATION_FORM_CHOICES = (
    ('',''),
    ('F', u'Очная'),
    ('E', u'Вечерняя'),
    ('C', u'Заочная'),
)

END_REASON_CHOICES = (
    ('',''),
    (u'Успешно завершил обучение','Успешно завершил обучение'),
    (u'Отчислен за неуспеваемость','Отчислен за неуспеваемость'),
)

GRADE_CHOICES = (
    (u'Отлично', 'Отлично'),
    (u'Хорошо', 'Хорошо'),
    (u'Удовл.', 'Удовл.'),
    (u'Зачет', 'Зачет'),
    (u'Незачет', 'Незачет'),
)

POSITION_CHOICES = (
    ('D', u'Декан факультета'),
    ('H', u'Заведующий кафедрой'),
    ('P', u'Профессор'),
    ('AP', u'Доцент'),
    ('A', u'Ассистент'),
)

SEMESTER_CHOICES = (
    (u'Осенний', 'Осенний'),
    (u'Весенний', 'Весенний'),
)

STATUS_CHOICES = (
    ('IN', u'Зачислен в ВУЗ'),
    ('OUT', u'Отчислен из ВУЗа'),
)

STUDIES_PROFILES = (
    (0, u'Технология и переработка полимеров'),
    (1, u'Химическая технология неорганических веществ'),
    (2, u'Технология защиты от коррозии'),
    (3, u'Химическая технология органических веществ'),
    (4, u'Технология электрохимических производств'),
    (5, u'Технология тугоплавких неметаллических и силикатных материалов'),
    (6, u'Химическая технология природных энергоносителей и углеродных материалов'),
    (7, u'Химическая технология материалов и приборов электронной техники и наноэлектроники'),
    (8, u'''Технология синтетических биологически активных веществ,
        химико-фармацевтических препаратов и косметических средств'''),
    (9, u'Химическая технология органических соединений азота'),
    (10, u'Химическая технология полимерных композиций, порохов и твердых ракетных топлив'),
    (11, u'Химическая технология материалов ЯТЦ'),
    (12, u'Технология разделения и применения изотопов'),
    (13, u'Технология теплоносителей и радиоэкология ядерных энергетических установок'),
    (14, u'Радиационная химия и радиационное материаловедение')
)


class TrainingField(models.Model):
    name = models.CharField(u'Название', max_length = 255)
    code = models.CharField(u'Код', max_length = 20, blank=True)
    
    class Meta:
        verbose_name = u'Направление подготовки'
        verbose_name_plural = u'Направления подготовки'

    def __unicode__(self):
        return "%s %s" % (self.code, self.name)


class Speciality(models.Model):
    name = models.CharField(u'Название', max_length = 255)
    code = models.CharField(u'Код', max_length = 20, blank=True)
    
    class Meta:
        verbose_name = u'Специальность'
        verbose_name_plural = u'Специальности'

    def __unicode__(self):
        return "%s %s" % (self.code, self.name)


class Subject(models.Model):
    name = models.CharField(u'Название', max_length = 255)
    code = models.CharField(u'Код', max_length = 20, blank=True)
    prk = models.CharField(u'ПрК', max_length = 20, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = u'Дисциплина'
        verbose_name_plural = u'Дисциплины'


class Professor(models.Model):
    user = models.OneToOneField(UserDetail, verbose_name=u"Пользователь")
    dept = models.ForeignKey(Department, verbose_name = u'Подразделение')
    position = models.CharField(u'Должность', choices = POSITION_CHOICES,  max_length = 200)

    def __unicode__(self):
        return "%s %s.%s." %   (self.user.last_name, 
                                self.user.first_name[:1],
                                self.user.middle_name[:1])

    class Meta:
        ordering = ['user__last_name',]
        verbose_name = u'Преподавательская деятельность'
        verbose_name_plural = u'Преподавательская деятельность'


class Education(models.Model):
    user = models.ForeignKey(User, verbose_name=u"Пользователь")
    type = models.CharField(u'Квалификация/степень', choices = EDUCATION_TYPE_CHOICES,  max_length = 50)
    form = models.CharField(u'Форма обучения', choices = EDUCATION_FORM_CHOICES,  max_length = 50)
    enter_date = models.DateField(u'Дата зачисления', null=True)
    speciality = models.ForeignKey(Speciality, verbose_name = u'Специальность')
    dept = models.ForeignKey(Department, verbose_name = u'Подразделение (Кафедра)', blank=True, null=True)
    record_book_number = models.CharField(u'Номер зачетки', max_length=7, default = 00000)
    group = models.CharField(u'Группа', max_length = 10, blank=True)
    study_profile = models.CharField(u"Профиль обучения", max_length=50, choices=STUDIES_PROFILES, blank=True)
    scientific_work = models.CharField(u'Научная деятельность', max_length = 300, blank=True)
    supervisor = models.CharField(u'Руководитель', max_length = 200)
    status = models.CharField(u'Статус', choices = STATUS_CHOICES,  max_length = 200)
    end_date = models.DateField(u'Дата отчисления',null=True)
    end_reason = models.CharField(u'Причина отчисления', choices = END_REASON_CHOICES,  max_length = 50, blank=True)
    notes = models.TextField(u'Примечания', blank=True)

    class Meta:
        verbose_name = u'Образование'
        verbose_name_plural = u'Образование'
        ordering = ['user__userdetail__last_name',]

    def __unicode__(self):
        return "%s (%s %s.%s.)" %  (self.get_type_display(), 
                                    self.user.userdetail.last_name, 
                                    self.user.userdetail.first_name[:1],
                                    self.user.userdetail.middle_name[:1])

    def get_graduation_work(self):
        return Work.objects.get(author=self, is_graduation=True).theme

    def get_full_name(self):
        return "%s %s %s" %    (self.user.userdetail.last_name, 
                                self.user.userdetail.first_name,
                                self.user.userdetail.middle_name)


class Studies(models.Model):
    leaner = models.ForeignKey(Education)
    subject = models.ForeignKey(Subject, verbose_name=u"Дисциплина")
    course = models.IntegerField(u'Курс', validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ], help_text='Введите число от 1 до 5')
    semester = models.CharField(u'Семестр', max_length = 100, choices=SEMESTER_CHOICES)
    hour_sem = models.CharField(u'Час/Сем', max_length = 40, blank=True)
    rating = models.IntegerField(u'Рейтинг', 
            validators=[
                MaxValueValidator(100),
                MinValueValidator(0)
            ], 
            help_text='Введите число от 0 до 100', blank=True, null=True)
    grade = models.CharField(u'Оценка', max_length = 40, choices=GRADE_CHOICES, blank=True)

    class Meta:
        verbose_name = u'Успеваемость'
        verbose_name_plural = u'Успеваемость'
        ordering = ['course', '-semester', 'subject__name'] 

    def __unicode__(self):
        return self.subject.name


def work_path(instance, filename):
    return os.path.join("users", u"%s_%s%s"%(instance.author.user.userdetail.last_name, 
        instance.author.user.userdetail.first_name[0], 
        instance.author.user.userdetail.middle_name[0]), "works", filename)


class Work(models.Model):
    author = models.ForeignKey(Education)
    name = models.CharField(u'Название', max_length = 255,
        help_text='Например: Квалификационная работа бакалавра')
    is_graduation = models.BooleanField(u"Работа является выпускной", default=False, blank=True)
    theme = models.CharField(u'Тема работы', max_length = 255, 
        help_text='Укажите тему БЕЗ кавычек')
    file = models.FileField(u'Файл', upload_to=work_path, 
            help_text='Загрузите скан документа в формате pdf, jpg или png')
    date = models.DateTimeField(u'Дата написания', max_length = 20)
    place = models.CharField(u'Где написана', max_length = 20, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Работа'
        verbose_name_plural = u'Работы'
        ordering = ['-date']