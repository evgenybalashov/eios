#coding: UTF-8
from __future__ import unicode_literals

from django.db import models


class Department(models.Model):
    parentId = models.ForeignKey('self', verbose_name='Родительское подразделение', null=True, blank=True)
    name = models.CharField(u'Название', max_length = 255)
    abbr = models.CharField(u'Аббревиатура', max_length = 20, blank=True)
    code = models.CharField(u'Код', max_length = 20, blank=True)
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Подразделение'
        verbose_name_plural = u'Подразделения'
