# Generated by Django 4.1 on 2022-08-25 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_rename_received_from_the_group_message_received_from_the_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='link',
            field=models.CharField(default='ZlFWOHcojj8eeODPAutS', max_length=50, unique=True),
        ),
    ]
