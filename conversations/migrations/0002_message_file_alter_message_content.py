# Generated by Django 5.0.7 on 2024-08-20 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("conversations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="uploads/"),
        ),
        migrations.AlterField(
            model_name="message",
            name="content",
            field=models.TextField(blank=True),
        ),
    ]
