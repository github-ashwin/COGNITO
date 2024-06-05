# Generated by Django 5.0.6 on 2024-05-30 17:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_topic_room_host_message_room_topic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AlterField(
            model_name='room',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.topic'),
        ),
    ]
