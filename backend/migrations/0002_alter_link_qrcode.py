# Generated by Django 5.0 on 2024-01-07 08:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="link",
            name="qrcode",
            field=models.ImageField(null=True, upload_to="media"),
        ),
    ]