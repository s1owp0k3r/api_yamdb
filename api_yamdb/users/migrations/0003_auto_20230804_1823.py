# Generated by Django 3.2 on 2023-08-04 11:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "ordering": ("id",),
                "verbose_name": "user",
                "verbose_name_plural": "Users",
            },
        ),
        migrations.AlterField(
            model_name="user",
            name="bio",
            field=models.TextField(blank=True, verbose_name="Biography"),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("user", "User"),
                    ("moderator", "Moderator"),
                    ("admin", "Administrator"),
                ],
                default="user",
                max_length=9,
                verbose_name="Role",
            ),
        ),
    ]
