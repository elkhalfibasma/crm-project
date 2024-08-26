# Generated by Django 5.0.7 on 2024-07-18 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('source', models.CharField(choices=[('website', 'Site Web'), ('advertisement', 'Publicité'), ('referral', 'Référence'), ('other', 'Autre')], max_length=20)),
                ('status', models.CharField(choices=[('new', 'Nouveau'), ('contacted', 'Contacté'), ('converted', 'Converti'), ('lost', 'Perdu')], default='new', max_length=20)),
                ('note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
