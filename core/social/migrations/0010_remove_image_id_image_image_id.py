# Generated by Django 4.1.3 on 2022-12-07 15:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("social", "0009_remove_post_image_image_post"),
    ]

    operations = [
        migrations.RemoveField(model_name="image", name="id",),
        migrations.AddField(
            model_name="image",
            name="image_id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]