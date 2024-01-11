# Generated by Django 5.0 on 2024-01-07 12:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0002_alter_link_qrcode"),
    ]

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("email", models.EmailField(max_length=254)),
                ("message", models.TextField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name="link",
            name="qrcode",
            field=models.ImageField(null=True, upload_to="qrcodes"),
        ),
    ]
