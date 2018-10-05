# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-06 17:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import opal.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('opal', '0035_auto_20180806_1150'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('datetime_received', models.DateTimeField(blank=True, null=True)),
                ('result', models.CharField(blank=True, default=b'', max_length=256)),
                ('result_number', models.FloatField(blank=True, null=True)),
                ('name', models.CharField(blank=True, default=b'', max_length=256)),
                ('code', models.CharField(blank=True, default=b'', max_length=256)),
                ('reference_range_min', models.FloatField(blank=True, null=True)),
                ('reference_range_max', models.FloatField(blank=True, null=True)),
                ('units', models.CharField(blank=True, default=b'', max_length=256)),
                ('data_absent_reason', models.TextField(blank=True, default=b'')),
                ('comment', models.TextField(blank=True, default=b'')),
                ('consistency_token', models.CharField(max_length=8)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_pathology_observation_subrecords', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datetime_received'],
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PathologyTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('category_name', models.CharField(default=b'default', max_length=256)),
                ('name', models.CharField(default=b'default', max_length=256)),
                ('datetime_ordered', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=256, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_pathology_pathologytest_subrecords', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opal.Patient')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_pathology_pathologytest_subrecords', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.AddField(
            model_name='observation',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pathology.PathologyTest'),
        ),
        migrations.AddField(
            model_name='observation',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_pathology_observation_subrecords', to=settings.AUTH_USER_MODEL),
        ),
    ]
