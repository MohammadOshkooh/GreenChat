# Generated by Django 4.1 on 2022-08-29 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, default='../static/img/group_profile.png', null=True, upload_to='profile/group/%y/%m/%d/')),
                ('link', models.CharField(default='tcCUzk0fgx88ZaRetj9g', max_length=25, unique=True)),
                ('members', models.ManyToManyField(related_name='member_set', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, default='body', null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=2)),
                ('image', models.ImageField(blank=True, default='../static/img/index.png', null=True, upload_to='chat/image/%y/%m/%d/')),
                ('contain_image', models.BooleanField(default=False)),
                ('received_from_the_group', models.BooleanField()),
                ('related_chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chat')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContactList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.ManyToManyField(related_name='contact_list', to=settings.AUTH_USER_MODEL)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
