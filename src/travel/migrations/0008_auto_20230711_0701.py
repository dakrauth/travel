# Generated by Django 3.2.11 on 2023-07-11 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0007_auto_20200225_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='TravelAliasCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='travelcurrency',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='travelcurrency',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True),
        ),
        migrations.CreateModel(
            name='Electrical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voltage', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('frequency', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('plugs', models.CharField(max_length=8)),
                ('entity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='electrical_info', to='travel.travelentity')),
            ],
        ),
        migrations.AlterField(
            model_name='travelalias',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='travel.travelaliascategory'),
        ),
    ]