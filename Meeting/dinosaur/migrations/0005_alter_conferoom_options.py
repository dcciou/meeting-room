# Generated by Django 4.2.5 on 2023-10-02 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dinosaur', '0004_conferoom_close_time_conferoom_open_time_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conferoom',
            options={'ordering': ['num']},
        ),
    ]
