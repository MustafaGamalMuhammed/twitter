# Generated by Django 3.1.3 on 2020-11-19 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0004_auto_20201116_1656'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ['-created_at']},
        ),
    ]
