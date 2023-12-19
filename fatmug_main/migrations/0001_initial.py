# Generated by Django 4.2.8 on 2023-12-19 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Vendor",
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
                ("name", models.CharField(max_length=255)),
                (
                    "contact_details",
                    models.TextField(db_comment="Preferably an email address"),
                ),
                ("address", models.TextField()),
                ("vendor_code", models.CharField(max_length=50, unique=True)),
                ("on_time_delivery_rate", models.FloatField(default=None)),
                ("quality_rating_avg", models.FloatField(default=None)),
                ("average_response_time", models.FloatField(default=None)),
                ("fulfillment_rate", models.FloatField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name="PurchaseOrder",
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
                ("po_number", models.CharField(max_length=50, unique=True)),
                ("order_date", models.DateTimeField()),
                ("delivery_date", models.DateTimeField()),
                ("items", models.JSONField()),
                ("quantity", models.IntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("completed", "Completed"),
                            ("canceled", "Canceled"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("quality_rating", models.FloatField(blank=True, null=True)),
                ("issue_date", models.DateTimeField()),
                ("acknowledgment_date", models.DateTimeField(null=True)),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fatmug_main.vendor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HistoricalPerformance",
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
                ("date", models.DateTimeField()),
                ("on_time_delivery_rate", models.FloatField()),
                ("quality_rating_avg", models.FloatField()),
                ("average_response_time", models.FloatField()),
                ("fulfillment_rate", models.FloatField()),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fatmug_main.vendor",
                    ),
                ),
            ],
        ),
    ]
