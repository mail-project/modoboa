from django.db import migrations


def move_transport_entries(apps, schema_editor):
    """Move old transport entries to new model."""
    pf_Transport = apps.get_model("autoreply", "Transport")
    Transport = apps.get_model("transport", "Transport")
    to_create = []
    for old_transport in pf_Transport.objects.all():
        to_create.append(Transport(pattern=old_transport.domain, service="autoreply"))
    Transport.objects.bulk_create(to_create)


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("transport", "0002_auto_20180928_1520"),
        ("autoreply", "0006_auto_20160329_1501"),
    ]

    operations = [
        migrations.RunPython(move_transport_entries, backward),
    ]
