# Generated by Django 5.0.6 on 2024-05-27 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_historicalperformance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalperformance',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
