# Generated by Django 3.2.8 on 2021-10-16 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("venues", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="venue",
            name="yelp_id",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
