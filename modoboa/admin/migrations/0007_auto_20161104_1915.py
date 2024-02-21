# Generated by Django 1.9.5 on 2016-11-04 18:15
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin", "0006_auto_20161104_1900"),
        ("relaydomains", "0005_auto_20161105_1426"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="alias",
            name="dates",
        ),
        migrations.RemoveField(
            model_name="domain",
            name="dates",
        ),
        migrations.RemoveField(
            model_name="domainalias",
            name="dates",
        ),
        migrations.RemoveField(
            model_name="mailbox",
            name="dates",
        ),
        migrations.AlterField(
            model_name="alias",
            name="last_modification",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="domain",
            name="last_modification",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="domainalias",
            name="last_modification",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="mailbox",
            name="last_modification",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.DeleteModel(
            name="ObjectDates",
        ),
    ]
