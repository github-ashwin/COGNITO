# Generated by Django 5.0.6 on 2024-06-11 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_room_participants'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
    ]
