# Generated by Django 4.2 on 2024-12-03 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestApp', '0004_alter_photo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='team_logos/'),
        ),
    ]
