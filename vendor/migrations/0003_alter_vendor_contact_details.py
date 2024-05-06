# Generated by Django 5.0 on 2024-05-06 11:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_purchaseorder_acknowledgment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='contact_details',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]