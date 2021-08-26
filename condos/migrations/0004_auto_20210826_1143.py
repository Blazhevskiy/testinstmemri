# Generated by Django 3.2.5 on 2021-08-26 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('condos', '0003_condo_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='condo',
            name='groups',
        ),
        migrations.AlterField(
            model_name='condo',
            name='amenities',
            field=models.ManyToManyField(related_name='condo', to='condos.Amenity'),
        ),
    ]
