# Generated by Django 4.2.2 on 2023-07-18 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("server", "0010_alter_player_occupation"),
    ]

    operations = [
        migrations.AddField(
            model_name="razorpaytransaction",
            name="event",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="server.event",
            ),
        ),
    ]
