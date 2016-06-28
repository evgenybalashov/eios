#coding: UTF-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
import os

from locations.models import Department


LEVEL_CHOICES = (
    (u'Свободно', 'Свободно'),
    (u'Уверенно', 'Уверенно'),
    (u'Средний', 'Средний'),
    (u'Технический', 'Технический'),
    (u'Базовый', 'Базовый'),
)


MARITAL_STATUS_CHOICES = (
    ('', ''),
    (u'Не женат', 'Не женат'),
    (u'Не замужем', 'Не замужем'),
    (u'Женат', 'Женат'),
    (u'Замужем', 'Замужем'),
)

SEX_CHOICES = (
    ('', ''),
    (u'М', 'Мужской'),
    (u'Ж', 'Женский'),
)


def photo_path(instance, filename):
    return os.path.join("users", u"%s_%s%s"%(instance.last_name, instance.first_name[0], 
        instance.middle_name[0]), "photo", filename)


class UserDetail(models.Model):
    user = models.OneToOneField(User, verbose_name=u"Пользователь")
    last_name = models.CharField(u"Фамилия", max_length=100)
    first_name = models.CharField(u"Имя", max_length=100)
    middle_name = models.CharField(u'Отчество', max_length=100, blank=True)
    birthday = models.DateField(u'Дата рождения', blank=True, null=True)
    place_birth = models.CharField(u'Место рождения', max_length = 200, blank=True)
    sex = models.CharField(u"Пол", max_length=10, choices=SEX_CHOICES, blank=True)
    photo = models.FileField(u'Фотография', upload_to=photo_path, blank=True)
    address = models.CharField(u"Адрес", max_length=300, blank=True)
    phone = models.CharField(u"Телефон", max_length=30, blank=True)
    # languages = models.ManyToManyField(Language, through='LangLevel', verbose_name=u"Иностранные языки", blank=True, null=True)
    social_work = models.TextField(u'Общественная работа', blank=True)
    marital_status = models.CharField(u"Семейное положение", max_length=10, 
        choices=MARITAL_STATUS_CHOICES, blank=True)
    is_professor = models.NullBooleanField(u'Преподаватель')
    notes = models.TextField(u'Примечания', blank=True)

    class Meta:
        verbose_name = u'Сведения о пользователе'
        verbose_name_plural = u'Сведения о пользователях'

    def __unicode__(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.middle_name)

    def get_education(self):
        return self.user.education_set.filter(status="IN").first()


class Application(models.Model):
    user = models.OneToOneField(UserDetail, verbose_name=u"Пользователь")
    dept = models.ForeignKey(Department, verbose_name = u'Подразделение (Кафедра)')

    class Meta:
        verbose_name = u'Запрос в подразделение'
        verbose_name_plural = u'Запросы в подразделение'

    def __unicode__(self):
        return 'Запрос (%s %s %s)' % (self.user.last_name, self.user.first_name, self.user.middle_name)


class Language(models.Model):
    language = models.CharField(u'Язык', max_length = 100)

    def __unicode__(self):
        return self.language

    class Meta:
        verbose_name = u'Язык'
        verbose_name_plural = u'Языки'
        ordering = ['language']


class LangLevel(models.Model):
    user = models.ForeignKey(UserDetail, verbose_name=u'Пользователь')
    lang = models.ForeignKey(Language, verbose_name=u'Язык')
    level = models.CharField(u'Уровень владения', max_length = 100, choices=LEVEL_CHOICES)

    class Meta:
        verbose_name = u'Владение иностранным языком'
        verbose_name_plural = u'Владение иностранными языками'

    def __unicode__(self):
        return "%s (%s)" % (self.lang.language, self.level)