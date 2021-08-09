# Generated by Django 3.2.5 on 2021-08-09 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Condos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_id', models.IntegerField()),
                ('condo_name', models.CharField(blank=True, max_length=64)),
                ('picture', models.CharField(blank=True, default=None, max_length=64)),
                ('location_id', models.IntegerField()),
                ('street_name', models.CharField(blank=True, max_length=64)),
                ('street_address', models.CharField(blank=True, max_length=64)),
                ('district', models.CharField(blank=True, default=None, max_length=64)),
                ('Province', models.CharField(blank=True, max_length=64)),
                ('zip_code', models.IntegerField()),
                ('note', models.CharField(blank=True, default=None, max_length=64)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('amenities', models.CharField(blank=True, default=None, max_length=64)),
                ('building_type_id', models.IntegerField(default=None)),
                ('condo_type_id', models.IntegerField()),
                ('condo_corp', models.CharField(blank=True, max_length=64)),
                ('floors', models.IntegerField()),
                ('units', models.IntegerField()),
                ('builder_id', models.IntegerField(default=None)),
                ('architect_id', models.IntegerField(default=None)),
                ('interior_designer_id', models.IntegerField(default=None)),
                ('date_completed', models.DateTimeField(default=None)),
                ('pm_id', models.IntegerField(default=None)),
                ('developer', models.CharField(blank=True, default=None, max_length=64)),
                ('send_email', models.CharField(blank=True, default=None, max_length=64)),
                ('view_floor_plans', models.CharField(blank=True, max_length=64)),
                ('created_date', models.DateTimeField(default=None)),
                ('modified_date', models.DateTimeField(default=None)),
                ('created_by_id', models.IntegerField(default=None)),
                ('modified_by_id', models.IntegerField(default=None)),
                ('eStatus', models.CharField(choices=[('a', 'Active'), ('i', 'Inactive'), ('d', 'Deleted')], default='Active', max_length=10)),
            ],
        ),
    ]
