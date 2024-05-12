# Generated by Django 4.1.13 on 2024-05-08 18:39

from django.db import migrations, models
from datetime import timedelta


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_purchaseorder_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='address',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='contact_details',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='vendor_code',
        ),
        migrations.AddField(
            model_name='vendor',
            name='fulfilment_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='vendor',
            name='on_time_delivery_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='vendor',
            name='quality_rating',
            field=models.FloatField(default=0),
        ),
           migrations.AddField(
        model_name='vendor',
        name='response_time',
        field=models.DurationField(default=timedelta(seconds=0)),
    ),

        migrations.AlterField(
            model_name='historicalperformance',
            name='date',
            field=models.DateTimeField(),
        ),
    ]