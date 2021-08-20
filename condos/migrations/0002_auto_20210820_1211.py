# Generated by Django 3.2.5 on 2021-08-20 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('condos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='condos',
            old_name='architect_id',
            new_name='architect',
        ),
        migrations.RenameField(
            model_name='condos',
            old_name='builder_id',
            new_name='builder',
        ),
        migrations.RenameField(
            model_name='condos',
            old_name='building_type_id',
            new_name='building_type',
        ),
        migrations.RenameField(
            model_name='condos',
            old_name='condo_type_id',
            new_name='condo_type',
        ),
        migrations.RenameField(
            model_name='condos',
            old_name='created_by_id',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='condos',
            old_name='interior_designer_id',
            new_name='interior_designer',
        ),
        migrations.RenameField(
            model_name='condos',
            old_name='location_id',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='condos',
            old_name='modified_by_id',
            new_name='modified_by',
        ),
        migrations.RenameField(
            model_name='condos',
            old_name='pm_id',
            new_name='pm',
        ),
    ]
