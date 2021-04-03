# Generated by Django 3.1.7 on 2021-03-28 15:54

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
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=200, verbose_name='Имя')),
                ('second_name', models.CharField(blank=True, max_length=200, verbose_name='Фамилия')),
                ('bio', models.TextField(default='О себе. ', max_length=300, verbose_name='Биография')),
                ('email', models.EmailField(blank=True, max_length=200, verbose_name='Почта')),
                ('country', models.CharField(blank=True, max_length=200, verbose_name='Страна')),
                ('avatar', models.ImageField(default='avatar.png', upload_to='avatars/', verbose_name='Аватар')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Слог')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('friends', models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL, verbose_name='Друзья')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
