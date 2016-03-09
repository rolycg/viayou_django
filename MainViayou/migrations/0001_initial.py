# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-09 03:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook_img', sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='/facebook', verbose_name='Facebook Image')),
                ('is_index', models.BooleanField(default=False, help_text='Check if the keyword belongs to the homepage', verbose_name='Is index?')),
                ('twitter_img', sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='/twitter', verbose_name='Twitter Image')),
            ],
            options={
                'verbose_name_plural': 'Keywords',
                'verbose_name': 'Keyword',
            },
        ),
        migrations.CreateModel(
            name='KeyWordTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('keywords', models.CharField(blank=True, help_text='keywords split by ;', max_length=200, null=True, verbose_name='Keywords')),
                ('description', models.CharField(blank=True, help_text='What goes inside the description metadata', max_length=400, null=True, verbose_name="Google's description")),
                ('facebook_msg', models.CharField(blank=True, help_text='What goes inside og:title metadata', max_length=300, null=True, verbose_name='Facebook message')),
                ('twitter_msg', models.CharField(blank=True, help_text='What goes inside twitter:title metadata', max_length=300, null=True, verbose_name='Twitter message')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='MainViayou.KeyWord')),
            ],
            options={
                'verbose_name': 'Keyword Translation',
                'default_permissions': (),
                'managed': True,
                'db_tablespace': '',
                'db_table': 'MainViayou_keyword_translation',
            },
        ),
        migrations.CreateModel(
            name='Travels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(help_text="Travel's Date", verbose_name='Date')),
                ('grade', models.IntegerField(blank=True, help_text='Evaluation for the travel', null=True, verbose_name='Grade')),
                ('origin_code', models.IntegerField(help_text='The origin of the travel, city code is saved', verbose_name='Origin')),
                ('destination_code', models.IntegerField(help_text='The destination of the travel, city code is saved', verbose_name='Destination')),
            ],
            options={
                'verbose_name_plural': 'Travels',
                'verbose_name': 'Travel',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Users',
                'verbose_name': 'User',
            },
        ),
        migrations.AddField(
            model_name='travels',
            name='users',
            field=models.ManyToManyField(help_text='Users in the travel', related_name='travels', to='MainViayou.User', verbose_name='Users'),
        ),
        migrations.AlterUniqueTogether(
            name='keywordtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
