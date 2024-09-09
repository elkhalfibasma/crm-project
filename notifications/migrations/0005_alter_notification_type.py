# Generated by Django 5.0.7 on 2024-09-06 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_notification_redirect_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('lead', 'Lead'), ('message', 'Message'), ('announcement', 'annonce')], max_length=20),
        ),
    ]
