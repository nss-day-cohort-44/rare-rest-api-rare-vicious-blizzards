# Generated by Django 3.1.6 on 2021-02-19 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='ended_on',
            field=models.DateField(blank=True),
        ),
    ]
