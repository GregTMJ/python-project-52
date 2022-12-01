# Generated by Django 4.1.3 on 2022-11-28 06:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('name', models.CharField(max_length=75,
                                          unique=True,
                                          verbose_name='name')),
                ('created_at', models.DateTimeField(
                    default=django.utils.timezone.now,
                    verbose_name='created_at')),
            ],
        ),
    ]
