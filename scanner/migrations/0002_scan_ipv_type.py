# Generated by Django 3.2.12 on 2023-02-26 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='ipv_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
