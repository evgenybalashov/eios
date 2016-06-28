 #coding: utf-8
import datetime, os
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from profiles.models import UserDetail


DOC_TYPE_CHOICES = (
	(u'Документ об образовании', 'Документ об образовании'),
	(u'Приказ', 'Приказ'),
	(u'Распоряжение ректора', 'Распоряжение ректора'),
	(u'Сертификат', 'Сертификат'),
)


class FlatPage(models.Model):
	url = models.CharField(u'URL', max_length=100)
	title = models.CharField(u'Заголовок', max_length=100)
	title_icon_name = models.CharField(u'Название иконки FontAwesome', max_length=100)
	content = models.TextField(u'Текст')

	class Meta:
		verbose_name = u'Простая страница'
		verbose_name_plural = u'Простые сраницы'

	def __unicode__(self):
		return self.title


class Publication(models.Model):
	title = models.CharField(u'Название', max_length = 500)
	authors = models.ManyToManyField(User, verbose_name = u'Автор')
	issue = models.CharField(u'Издание', max_length = 100)
	is_recommended = models.BooleanField(u'В издании, рекомендованном ВАК', default=False)

	class Meta:
		verbose_name = u'Публикация'
		verbose_name_plural = u'Публикации'

	def __unicode__(self):
		return "%s"[:60] % self.title


def doc_path(instance, filename):
	today = datetime.datetime.now()
	today_path = today.strftime("%Y/%m/%d")
	return os.path.join("docs", today_path, filename)


class Document(models.Model):
	user = models.ForeignKey(UserDetail, verbose_name=u"Пользователи")
	type = models.CharField(u'Тип', max_length = 25, choices=DOC_TYPE_CHOICES)
	file = models.FileField(u'Файл', upload_to=doc_path, 
			help_text='Загрузите скан документа в формате pdf, jpg или png')
	name = models.CharField(u'Название', max_length = 255)
	code = models.CharField(u'Код', max_length = 20, blank=True)
	series = models.CharField(u'Серия', max_length = 20, blank=True)
	number = models.CharField(u'Номер', max_length = 20)
	issued_by = models.CharField(u'Кем выдан', max_length = 100)
	issue_date = models.DateTimeField(u'Когда выдан', max_length = 20)
	issue_place = models.CharField(u'Где выдан', max_length = 20, blank=True)
	guideline = models.CharField(u'Директива', max_length=255, blank=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = u'Документ'
		verbose_name_plural = u'Документы'
		ordering = ['-issue_date']
