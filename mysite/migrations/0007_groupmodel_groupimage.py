# Generated by Django 3.2.9 on 2021-11-23 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_activitymodel_activity_added_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmodel',
            name='groupImage',
            field=models.ImageField(max_length=144, null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
    ]