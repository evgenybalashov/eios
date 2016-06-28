# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-26 23:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_auto_20160626_1243'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='professor',
            options={'ordering': ['user__last_name'], 'verbose_name': '\u041f\u0440\u0435\u043f\u043e\u0434\u0430\u0432\u0430\u0442\u0435\u043b\u044c\u0441\u043a\u0430\u044f \u0434\u0435\u044f\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c', 'verbose_name_plural': '\u041f\u0440\u0435\u043f\u043e\u0434\u0430\u0432\u0430\u0442\u0435\u043b\u044c\u0441\u043a\u0430\u044f \u0434\u0435\u044f\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c'},
        ),
        migrations.RenameField(
            model_name='education',
            old_name='chair',
            new_name='dept',
        ),
        migrations.RemoveField(
            model_name='education',
            name='faculty',
        ),
        migrations.AlterField(
            model_name='education',
            name='group',
            field=models.CharField(blank=True, max_length=10, verbose_name='\u0413\u0440\u0443\u043f\u043f\u0430'),
        ),
    ]
