# Generated by Django 2.2.8 on 2021-06-05 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0002_auto_20210412_1006'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='limit',
            new_name='guest_limit',
        ),
    ]