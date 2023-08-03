# Generated by Django 3.2 on 2023-08-02 18:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0002_remove_title_name_year_unique_relationships"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ("id",)},
        ),
        migrations.AlterModelOptions(
            name="genre",
            options={"ordering": ("id",)},
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="genre",
            name="name",
            field=models.CharField(max_length=256),
        ),
    ]
