# Generated by Django 3.2.5 on 2021-07-28 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_follow_like_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='editdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='edited',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]