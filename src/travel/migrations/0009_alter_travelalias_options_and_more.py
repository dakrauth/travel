# Generated by Django 4.2.8 on 2024-01-19 07:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("travel", "0008_auto_20230711_0701"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="travelalias",
            options={"verbose_name_plural": "aliases"},
        ),
        migrations.AlterModelOptions(
            name="travelaliascategory",
            options={"verbose_name_plural": "Alias Categories"},
        ),
        migrations.AlterModelOptions(
            name="travelbucketlist",
            options={"verbose_name_plural": "bucket lists"},
        ),
        migrations.AlterModelOptions(
            name="travelclassification",
            options={"verbose_name_plural": "classifications"},
        ),
        migrations.AlterModelOptions(
            name="travelcurrency",
            options={"ordering": ["iso"], "verbose_name_plural": "currencies"},
        ),
        migrations.AlterModelOptions(
            name="travelentity",
            options={"ordering": ("name",), "verbose_name_plural": "entities"},
        ),
        migrations.AlterModelOptions(
            name="travelentityinfo",
            options={"ordering": ["entity"], "verbose_name_plural": "entity info"},
        ),
        migrations.AlterModelOptions(
            name="travelentitytype",
            options={"verbose_name_plural": "entity types"},
        ),
        migrations.AlterModelOptions(
            name="travelflag",
            options={"verbose_name_plural": "flags"},
        ),
        migrations.AlterModelOptions(
            name="travellanguage",
            options={"ordering": ["name"], "verbose_name_plural": "languages"},
        ),
        migrations.AlterModelOptions(
            name="travellog",
            options={
                "get_latest_by": "arrival",
                "ordering": ("-arrival",),
                "verbose_name_plural": "logs",
            },
        ),
        migrations.AlterModelOptions(
            name="travelprofile",
            options={"verbose_name_plural": "profile"},
        ),
        migrations.RemoveField(
            model_name="travelentityinfo",
            name="region",
        ),
        migrations.AlterField(
            model_name="externalreference",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="externalsource",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="travelalias",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="travelbucketlist",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="travelclassification",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="travelentity",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="travelentityinfo",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="travelentitytype",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="travelflag",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="travellanguage",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="travellog",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="travelprofile",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.DeleteModel(
            name="TravelRegion",
        ),
    ]