# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-26 23:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_userdetail_is_professor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='address',
            field=models.CharField(blank=True, max_length=300, verbose_name='\u0410\u0434\u0440\u0435\u0441'),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='phone',
            field=models.CharField(blank=True, max_length=30, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d'),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='sex',
            field=models.CharField(blank=True, choices=[('', ''), ('\u041c', '\u041c\u0443\u0436\u0441\u043a\u043e\u0439'), ('\u0416', '\u0416\u0435\u043d\u0441\u043a\u0438\u0439')], max_length=10, verbose_name='\u041f\u043e\u043b'),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='social_work',
            field=models.TextField(blank=True, verbose_name='\u041e\u0431\u0449\u0435\u0441\u0442\u0432\u0435\u043d\u043d\u0430\u044f \u0440\u0430\u0431\u043e\u0442\u0430'),
        ),
    ]
