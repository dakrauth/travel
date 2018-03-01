# Generated by Django 2.0 on 2018-02-16 18:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_auto_20170628_2212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelflag',
            name='large',
        ),
        migrations.RemoveField(
            model_name='travelflag',
            name='thumb',
        ),
        migrations.AddField(
            model_name='travelflag',
            name='emoji',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AlterField(
            model_name='travelbucketlist',
            name='owner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
