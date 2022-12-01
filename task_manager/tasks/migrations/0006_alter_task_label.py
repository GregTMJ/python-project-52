# Generated by Django 4.1.3 on 2022-11-28 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0005_alter_task_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='label',
            field=models.ManyToManyField(
                blank=True,
                related_name='label',
                through='tasks.TaskLabelRelation',
                to='labels.label',
                verbose_name='label'),
        ),
    ]
