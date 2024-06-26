# Generated by Django 1.9.5 on 2016-11-04 18:00
from django.db import migrations, models
import django.utils.timezone


def move_dates(apps, schema_editor):
    """Move dates to models."""
    Domain = apps.get_model("admin", "Domain")
    DomainAlias = apps.get_model("admin", "DomainAlias")
    Mailbox = apps.get_model("admin", "Mailbox")
    Alias = apps.get_model("admin", "Alias")
    for model in [Domain, DomainAlias, Mailbox, Alias]:
        for instance in model.objects.all():
            instance.creation = instance.dates.creation
            instance.last_modification = instance.dates.last_modification
            instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ("admin", "0005_auto_20161026_1003"),
    ]

    operations = [
        migrations.AddField(
            model_name="alias",
            name="creation",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="alias",
            name="last_modification",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="domain",
            name="creation",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="domain",
            name="last_modification",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="domainalias",
            name="creation",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="domainalias",
            name="last_modification",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="mailbox",
            name="creation",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="mailbox",
            name="last_modification",
            field=models.DateTimeField(null=True),
        ),
        migrations.RunPython(move_dates),
    ]
